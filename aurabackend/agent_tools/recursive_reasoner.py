"""
Recursive Reasoner Tool
Implements recursive reasoning for AI agents using tiny recursive models
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ReasoningStep(Enum):
    """Types of reasoning steps"""
    ANALYZE = "analyze"
    DECOMPOSE = "decompose"
    SOLVE = "solve"
    VERIFY = "verify"
    SYNTHESIZE = "synthesize"


@dataclass
class ReasoningNode:
    """Node in the reasoning tree"""
    step_type: ReasoningStep
    question: str
    answer: Optional[str] = None
    confidence: float = 0.0
    sub_questions: List['ReasoningNode'] = None
    depth: int = 0
    
    def __post_init__(self):
        if self.sub_questions is None:
            self.sub_questions = []


class RecursiveReasoner:
    """
    Tool for recursive reasoning using tiny recursive models
    Breaks down complex problems into smaller sub-problems
    """
    
    def __init__(self, max_depth: int = 3):
        self.tool_name = "recursive_reasoner"
        self.tool_description = "Recursive reasoning tool that breaks complex problems into smaller sub-problems"
        self.max_depth = max_depth
        self.reasoning_history: List[ReasoningNode] = []
    
    def reason(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
        max_depth: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Apply recursive reasoning to a problem
        
        Args:
            problem: The problem to solve
            context: Additional context information
            max_depth: Maximum recursion depth
        
        Returns:
            Reasoning results with solution
        """
        if max_depth is None:
            max_depth = self.max_depth
        
        # Create root reasoning node
        root_node = ReasoningNode(
            step_type=ReasoningStep.ANALYZE,
            question=problem,
            depth=0
        )
        
        # Apply recursive reasoning
        self._recursive_solve(root_node, context or {}, max_depth)
        
        # Store in history
        self.reasoning_history.append(root_node)
        
        # Extract solution
        solution = self._extract_solution(root_node)
        
        return {
            "problem": problem,
            "solution": solution,
            "confidence": root_node.confidence,
            "reasoning_tree": self._serialize_tree(root_node),
            "steps_taken": self._count_steps(root_node),
            "max_depth_reached": self._get_max_depth(root_node)
        }
    
    def _recursive_solve(
        self,
        node: ReasoningNode,
        context: Dict[str, Any],
        max_depth: int
    ):
        """
        Recursively solve a problem by breaking it down
        """
        # Base case: reached max depth or simple enough to solve
        if node.depth >= max_depth or self._is_simple_enough(node.question):
            node.answer = self._solve_directly(node.question, context)
            node.confidence = 0.8  # Direct solutions have good confidence
            return
        
        # Decompose into sub-problems
        sub_problems = self._decompose_problem(node.question, context)
        
        if not sub_problems:
            # Cannot decompose further, solve directly
            node.answer = self._solve_directly(node.question, context)
            node.confidence = 0.6  # Lower confidence for complex direct solutions
            return
        
        # Create sub-nodes and solve recursively
        for sub_problem in sub_problems:
            sub_node = ReasoningNode(
                step_type=ReasoningStep.SOLVE,
                question=sub_problem,
                depth=node.depth + 1
            )
            node.sub_questions.append(sub_node)
            self._recursive_solve(sub_node, context, max_depth)
        
        # Synthesize answers from sub-problems
        node.answer = self._synthesize_answers(node)
        node.confidence = self._calculate_confidence(node)
    
    def _is_simple_enough(self, question: str) -> bool:
        """
        Determine if a question is simple enough to solve directly
        """
        # Simple heuristics
        word_count = len(question.split())
        
        # Simple questions are typically short and contain specific keywords
        if word_count < 10:
            return True
        
        # Questions about specific fields or simple comparisons
        simple_keywords = ['what is', 'show', 'list', 'get', 'find', 'count']
        if any(keyword in question.lower() for keyword in simple_keywords):
            return True
        
        return False
    
    def _decompose_problem(
        self,
        problem: str,
        context: Dict[str, Any]
    ) -> List[str]:
        """
        Decompose a complex problem into sub-problems
        """
        sub_problems = []
        problem_lower = problem.lower()
        
        # Pattern 1: Questions with "and" can be split
        if ' and ' in problem_lower:
            parts = problem.split(' and ')
            if len(parts) > 1:
                return [part.strip() for part in parts]
        
        # Pattern 2: Multi-step database queries
        if 'database' in problem_lower or 'query' in problem_lower:
            # Check if it involves multiple tables or operations
            if 'join' in problem_lower or 'multiple tables' in problem_lower:
                sub_problems.extend([
                    "Identify the tables involved",
                    "Determine the join conditions",
                    "Construct the SELECT statement"
                ])
            elif 'aggregate' in problem_lower or 'group by' in problem_lower:
                sub_problems.extend([
                    "Identify the aggregation columns",
                    "Determine the grouping criteria",
                    "Apply the aggregation function"
                ])
        
        # Pattern 3: Analysis questions
        if 'analyze' in problem_lower or 'compare' in problem_lower:
            sub_problems.extend([
                "Extract the data",
                "Calculate relevant metrics",
                "Compare and interpret results"
            ])
        
        # Pattern 4: Questions with multiple criteria
        if 'where' in problem_lower and ('and' in problem_lower or 'or' in problem_lower):
            sub_problems.extend([
                "Identify primary filter criteria",
                "Identify secondary filter criteria",
                "Combine filters logically"
            ])
        
        return sub_problems
    
    def _solve_directly(self, question: str, context: Dict[str, Any]) -> str:
        """
        Solve a simple question directly
        """
        question_lower = question.lower()
        
        # Database-related questions
        if 'database' in question_lower or 'table' in question_lower:
            schema = context.get('schema', {})
            if 'identify' in question_lower and 'tables' in question_lower:
                tables = schema.get('tables', [])
                if tables:
                    table_names = [t.get('name', 'unknown') for t in tables]
                    return f"Tables involved: {', '.join(table_names[:5])}"
            
            if 'columns' in question_lower:
                tables = schema.get('tables', [])
                if tables:
                    columns = tables[0].get('columns', [])
                    col_names = [c.get('name', 'unknown') for c in columns[:5]]
                    return f"Columns: {', '.join(col_names)}"
        
        # Query construction questions
        if 'select' in question_lower or 'query' in question_lower:
            return "Construct a SELECT query with appropriate columns and conditions"
        
        if 'join' in question_lower:
            return "Use JOIN clause to combine data from multiple tables"
        
        if 'group' in question_lower or 'aggregate' in question_lower:
            return "Apply GROUP BY with appropriate aggregation function (SUM, COUNT, AVG, etc.)"
        
        # Default response
        return f"Solution for: {question}"
    
    def _synthesize_answers(self, node: ReasoningNode) -> str:
        """
        Synthesize answers from sub-problems into a complete solution
        """
        if not node.sub_questions:
            return node.answer or "No answer available"
        
        # Collect all sub-answers
        sub_answers = [
            f"{i+1}. {sq.answer}"
            for i, sq in enumerate(node.sub_questions)
            if sq.answer
        ]
        
        # Combine into a coherent solution
        synthesized = f"To solve '{node.question}':\n" + "\n".join(sub_answers)
        
        return synthesized
    
    def _calculate_confidence(self, node: ReasoningNode) -> float:
        """
        Calculate confidence based on sub-problem solutions
        """
        if not node.sub_questions:
            return node.confidence
        
        # Average confidence of sub-problems
        sub_confidences = [sq.confidence for sq in node.sub_questions if sq.confidence > 0]
        
        if sub_confidences:
            avg_confidence = sum(sub_confidences) / len(sub_confidences)
            # Slightly reduce confidence when synthesizing (uncertainty in combination)
            return avg_confidence * 0.95
        
        return 0.5  # Default moderate confidence
    
    def _extract_solution(self, node: ReasoningNode) -> str:
        """
        Extract the final solution from the reasoning tree
        """
        return node.answer or "Unable to determine solution"
    
    def _serialize_tree(self, node: ReasoningNode) -> Dict[str, Any]:
        """
        Serialize reasoning tree for visualization
        """
        return {
            "step_type": node.step_type.value,
            "question": node.question,
            "answer": node.answer,
            "confidence": node.confidence,
            "depth": node.depth,
            "sub_questions": [
                self._serialize_tree(sq) for sq in node.sub_questions
            ]
        }
    
    def _count_steps(self, node: ReasoningNode) -> int:
        """
        Count total reasoning steps in the tree
        """
        count = 1  # Current node
        for sq in node.sub_questions:
            count += self._count_steps(sq)
        return count
    
    def _get_max_depth(self, node: ReasoningNode) -> int:
        """
        Get maximum depth reached in reasoning tree
        """
        if not node.sub_questions:
            return node.depth
        
        return max(self._get_max_depth(sq) for sq in node.sub_questions)
    
    def explain_reasoning(self, reasoning_result: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of reasoning process
        """
        tree = reasoning_result.get("reasoning_tree", {})
        
        explanation = [
            f"Problem: {reasoning_result.get('problem', 'Unknown')}",
            f"Solution: {reasoning_result.get('solution', 'Not found')}",
            f"Confidence: {reasoning_result.get('confidence', 0):.2%}",
            f"Steps taken: {reasoning_result.get('steps_taken', 0)}",
            f"Maximum depth: {reasoning_result.get('max_depth_reached', 0)}",
            "",
            "Reasoning process:"
        ]
        
        self._explain_node(tree, explanation, indent=0)
        
        return "\n".join(explanation)
    
    def _explain_node(
        self,
        node: Dict[str, Any],
        explanation: List[str],
        indent: int = 0
    ):
        """
        Recursively explain reasoning nodes
        """
        prefix = "  " * indent
        question = node.get("question", "")
        answer = node.get("answer", "")
        confidence = node.get("confidence", 0)
        
        explanation.append(f"{prefix}Q: {question}")
        if answer:
            explanation.append(f"{prefix}A: {answer} (confidence: {confidence:.2%})")
        
        sub_questions = node.get("sub_questions", [])
        if sub_questions:
            explanation.append(f"{prefix}Sub-problems:")
            for sq in sub_questions:
                self._explain_node(sq, explanation, indent + 1)
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for agent use"""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "operations": [
                {
                    "name": "reason",
                    "description": "Apply recursive reasoning to solve a problem",
                    "parameters": {
                        "problem": "string (required) - The problem to solve",
                        "context": "object (optional) - Additional context",
                        "max_depth": "integer (optional) - Maximum recursion depth"
                    }
                },
                {
                    "name": "explain_reasoning",
                    "description": "Generate explanation of reasoning process",
                    "parameters": {
                        "reasoning_result": "object (required) - Result from reason() call"
                    }
                }
            ]
        }
