import os
import uuid
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
import pandas as pd
import json
from fastapi import UploadFile, HTTPException
import aiofiles

class FileService:
    """Service for handling file uploads, storage, and processing"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / "data"
        self.uploads_path = self.base_path / "uploads"
        self.processed_path = self.base_path / "processed"
        self.temp_path = self.base_path / "temp"
        
        # Ensure directories exist
        self.uploads_path.mkdir(parents=True, exist_ok=True)
        self.processed_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)
        
        # Supported file types
        self.supported_types = {
            'text/csv': ['.csv'],
            'application/json': ['.json'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/vnd.ms-excel': ['.xls'],
            'text/plain': ['.txt'],
            'application/octet-stream': ['.parquet'],  # Parquet files
            'application/x-parquet': ['.parquet'],     # Alternative MIME type
        }
        
        # Maximum file size (25MB - increased for Parquet files)
        self.max_file_size = 25 * 1024 * 1024
    
    def generate_file_id(self) -> str:
        """Generate unique file ID"""
        return str(uuid.uuid4())
    
    def calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA256 hash of file content"""
        return hashlib.sha256(content).hexdigest()
    
    def validate_file(self, file: UploadFile) -> Dict[str, Any]:
        """Validate uploaded file"""
        # Check file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 25MB.")
        
        # Check file type
        file_ext = Path(file.filename).suffix.lower()
        content_type = file.content_type
        
        supported = False
        for mime_type, extensions in self.supported_types.items():
            if content_type == mime_type or file_ext in extensions:
                supported = True
                break
        
        if not supported:
            supported_extensions = []
            for extensions in self.supported_types.values():
                supported_extensions.extend(extensions)
            raise HTTPException(
                status_code=415, 
                detail=f"Unsupported file type. Supported formats: {', '.join(supported_extensions)}"
            )
        
        return {
            'filename': file.filename,
            'content_type': content_type,
            'file_extension': file_ext,
            'file_size': file.size
        }
    
    async def save_file(self, file: UploadFile) -> Dict[str, Any]:
        """Save uploaded file to storage"""
        # Validate file
        file_info = self.validate_file(file)
        
        # Generate unique file ID and path
        file_id = self.generate_file_id()
        original_filename = file_info['filename']
        file_extension = file_info['file_extension']
        
        # Create unique filename
        stored_filename = f"{file_id}{file_extension}"
        file_path = self.uploads_path / stored_filename
        
        # Read file content
        content = await file.read()
        file_hash = self.calculate_file_hash(content)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Create metadata
        metadata = {
            'file_id': file_id,
            'original_filename': original_filename,
            'stored_filename': stored_filename,
            'file_path': str(file_path),
            'content_type': file_info['content_type'],
            'file_extension': file_extension,
            'file_size': len(content),
            'file_hash': file_hash,
            'upload_time': datetime.utcnow().isoformat(),
            'status': 'uploaded'
        }
        
        return metadata
    
    async def process_file(self, file_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Process uploaded file and extract data"""
        file_path = Path(file_metadata['file_path'])
        file_extension = file_metadata['file_extension']
        
        try:
            processed_data = None
            rows_count = 0
            columns_count = 0
            
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
                processed_data = df.to_dict('records')
                rows_count = len(df)
                columns_count = len(df.columns)
                
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
                processed_data = df.to_dict('records')
                rows_count = len(df)
                columns_count = len(df.columns)
                
            elif file_extension == '.parquet':
                import pyarrow.parquet as pq
                # Read parquet file with pandas for data processing
                df = pd.read_parquet(file_path)
                processed_data = df.to_dict('records')
                rows_count = len(df)
                columns_count = len(df.columns)
                
                # Get additional Parquet metadata
                parquet_file = pq.ParquetFile(file_path)
                parquet_metadata = {
                    'num_row_groups': parquet_file.num_row_groups,
                    'schema': str(parquet_file.schema),
                    'compression': str(parquet_file.metadata.row_group(0).column(0).compression) if parquet_file.num_row_groups > 0 else 'unknown'
                }
                file_metadata['parquet_info'] = parquet_metadata
                
            elif file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    processed_data = json.load(f)
                
                if isinstance(processed_data, list):
                    rows_count = len(processed_data)
                    columns_count = len(processed_data[0].keys()) if processed_data else 0
                else:
                    rows_count = 1
                    columns_count = len(processed_data.keys()) if isinstance(processed_data, dict) else 0
                    
            elif file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to parse as JSON first, then as CSV
                try:
                    processed_data = json.loads(content)
                    if isinstance(processed_data, list):
                        rows_count = len(processed_data)
                        columns_count = len(processed_data[0].keys()) if processed_data else 0
                except json.JSONDecodeError:
                    # Try as CSV
                    lines = content.strip().split('\n')
                    if len(lines) > 1:
                        headers = [h.strip() for h in lines[0].split(',')]
                        processed_data = []
                        for line in lines[1:]:
                            values = [v.strip() for v in line.split(',')]
                            row = {}
                            for i, header in enumerate(headers):
                                if i < len(values):
                                    value = values[i]
                                    # Try to convert to number
                                    try:
                                        row[header] = float(value) if '.' in value else int(value)
                                    except ValueError:
                                        row[header] = value
                                else:
                                    row[header] = None
                            processed_data.append(row)
                        rows_count = len(processed_data)
                        columns_count = len(headers)
            
            # Save processed data
            processed_filename = f"{file_metadata['file_id']}_processed.json"
            processed_path = self.processed_path / processed_filename
            
            with open(processed_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, indent=2, default=str)
            
            # Update metadata
            file_metadata.update({
                'status': 'processed',
                'processed_path': str(processed_path),
                'processed_filename': processed_filename,
                'rows_count': rows_count,
                'columns_count': columns_count,
                'processed_time': datetime.utcnow().isoformat(),
                'preview_data': processed_data[:5] if isinstance(processed_data, list) else processed_data
            })
            
            return file_metadata
            
        except Exception as e:
            file_metadata['status'] = 'error'
            file_metadata['error'] = str(e)
            file_metadata['error_time'] = datetime.utcnow().isoformat()
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file information by ID"""
        # This would typically query the database
        # For now, we'll implement a simple file-based lookup
        pass
    
    def list_files(self) -> List[Dict[str, Any]]:
        """List all uploaded files"""
        files = []
        for file_path in self.uploads_path.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        return files
    
    def delete_file(self, file_id: str) -> bool:
        """Delete file by ID"""
        # Find and delete both original and processed files
        try:
            for file_path in self.uploads_path.glob(f"{file_id}.*"):
                file_path.unlink()
            
            for file_path in self.processed_path.glob(f"{file_id}_processed.*"):
                file_path.unlink()
            
            return True
        except Exception:
            return False

# Global file service instance
file_service = FileService()