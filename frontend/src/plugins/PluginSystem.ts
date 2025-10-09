// Plugin System Architecture for AURA
// This demonstrates the "Platform Moat" - building AURA like VS Code with extensibility

export interface AuraPlugin {
  id: string;
  name: string;
  version: string;
  description: string;
  author: string;
  category: 'connector' | 'transformer' | 'analyzer' | 'visualizer' | 'template';
  icon?: string;
  homepage?: string;
  repository?: string;
}

export interface ConnectorPlugin extends AuraPlugin {
  category: 'connector';
  connectionConfig: {
    fields: ConfigField[];
    testConnection: (config: Record<string, any>) => Promise<boolean>;
  };
  dataExtractor: (config: Record<string, any>, query: string) => Promise<any>;
  schemaIntrospector: (config: Record<string, any>) => Promise<DatabaseSchema>;
}

export interface TransformerPlugin extends AuraPlugin {
  category: 'transformer';
  supportedInputs: string[];
  outputFormat: string;
  transform: (data: any, options: Record<string, any>) => Promise<any>;
  configSchema: ConfigField[];
}

export interface AnalyzerPlugin extends AuraPlugin {
  category: 'analyzer';
  analysisType: 'statistical' | 'ml' | 'business_logic' | 'custom';
  analyze: (data: any, parameters: Record<string, any>) => Promise<AnalysisResult>;
  parameterSchema: ConfigField[];
}

export interface VisualizerPlugin extends AuraPlugin {
  category: 'visualizer';
  chartTypes: string[];
  renderChart: (data: any, config: ChartConfig) => Promise<string | React.ComponentType>;
  configOptions: ConfigField[];
}

export interface TemplatePlugin extends AuraPlugin {
  category: 'template';
  vertical: string;
  useCase: string;
  sqlTemplate: string;
  parameterMapping: Record<string, string>;
  expectedSchema: DatabaseSchema;
}

export interface ConfigField {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'select' | 'multiselect' | 'password';
  label: string;
  description?: string;
  required: boolean;
  defaultValue?: any;
  options?: { value: any; label: string }[];
  validation?: {
    pattern?: string;
    min?: number;
    max?: number;
    minLength?: number;
    maxLength?: number;
  };
}

export interface DatabaseSchema {
  tables: TableSchema[];
  relationships: Relationship[];
}

export interface TableSchema {
  name: string;
  columns: ColumnSchema[];
  primaryKey?: string[];
  description?: string;
}

export interface ColumnSchema {
  name: string;
  type: string;
  nullable: boolean;
  description?: string;
  foreignKey?: {
    table: string;
    column: string;
  };
}

export interface Relationship {
  fromTable: string;
  fromColumn: string;
  toTable: string;
  toColumn: string;
  type: 'one-to-one' | 'one-to-many' | 'many-to-many';
}

export interface AnalysisResult {
  type: string;
  summary: string;
  insights: Insight[];
  visualizations?: ChartConfig[];
  recommendations?: string[];
  confidence: number;
}

export interface Insight {
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high';
  category: string;
  data?: any;
}

export interface ChartConfig {
  type: string;
  title: string;
  data: any;
  options: Record<string, any>;
}

// Plugin Registry and Management
export class PluginRegistry {
  private plugins: Map<string, AuraPlugin> = new Map();
  private enabledPlugins: Set<string> = new Set();

  async installPlugin(plugin: AuraPlugin): Promise<void> {
    // Validate plugin structure
    if (!this.validatePlugin(plugin)) {
      throw new Error(`Invalid plugin structure: ${plugin.id}`);
    }

    // Check for conflicts
    if (this.plugins.has(plugin.id)) {
      throw new Error(`Plugin ${plugin.id} is already installed`);
    }

    // Install the plugin
    this.plugins.set(plugin.id, plugin);
    console.log(`Installed plugin: ${plugin.name} v${plugin.version}`);
  }

  enablePlugin(pluginId: string): void {
    if (!this.plugins.has(pluginId)) {
      throw new Error(`Plugin ${pluginId} is not installed`);
    }
    
    this.enabledPlugins.add(pluginId);
    console.log(`Enabled plugin: ${pluginId}`);
  }

  disablePlugin(pluginId: string): void {
    this.enabledPlugins.delete(pluginId);
    console.log(`Disabled plugin: ${pluginId}`);
  }

  getPlugin<T extends AuraPlugin>(pluginId: string): T | undefined {
    return this.plugins.get(pluginId) as T;
  }

  getPluginsByCategory<T extends AuraPlugin>(category: string): T[] {
    return Array.from(this.plugins.values())
      .filter(plugin => plugin.category === category && this.enabledPlugins.has(plugin.id)) as T[];
  }

  getAllPlugins(): AuraPlugin[] {
    return Array.from(this.plugins.values());
  }

  getEnabledPlugins(): AuraPlugin[] {
    return Array.from(this.plugins.values())
      .filter(plugin => this.enabledPlugins.has(plugin.id));
  }

  private validatePlugin(plugin: AuraPlugin): boolean {
    return !!(
      plugin.id &&
      plugin.name &&
      plugin.version &&
      plugin.category &&
      ['connector', 'transformer', 'analyzer', 'visualizer', 'template'].includes(plugin.category)
    );
  }
}

// Example Plugin Implementations
export const shopifyConnectorPlugin: ConnectorPlugin = {
  id: 'shopify-connector',
  name: 'Shopify Connector',
  version: '1.0.0',
  description: 'Connect to Shopify stores and extract e-commerce data',
  author: 'AURA Team',
  category: 'connector',
  icon: '🛒',
  connectionConfig: {
    fields: [
      {
        name: 'shopUrl',
        type: 'string',
        label: 'Shop URL',
        description: 'Your Shopify store URL (e.g., mystore.myshopify.com)',
        required: true,
        validation: {
          pattern: '^[a-zA-Z0-9-]+\\.myshopify\\.com$'
        }
      },
      {
        name: 'accessToken',
        type: 'password',
        label: 'Access Token',
        description: 'Shopify Admin API access token',
        required: true
      }
    ],
    testConnection: async (_config) => {
      // Implementation would test actual Shopify connection
      return true;
    }
  },
  dataExtractor: async (_config, _query) => {
    // Implementation would use Shopify Admin API
    return { data: [], status: 'success' };
  },
  schemaIntrospector: async (_config) => {
    return {
      tables: [
        {
          name: 'orders',
          columns: [
            { name: 'id', type: 'bigint', nullable: false },
            { name: 'email', type: 'varchar', nullable: true },
            { name: 'total_price', type: 'decimal', nullable: false },
            { name: 'created_at', type: 'timestamp', nullable: false }
          ],
          primaryKey: ['id']
        },
        {
          name: 'customers',
          columns: [
            { name: 'id', type: 'bigint', nullable: false },
            { name: 'email', type: 'varchar', nullable: false },
            { name: 'first_name', type: 'varchar', nullable: true },
            { name: 'last_name', type: 'varchar', nullable: true }
          ],
          primaryKey: ['id']
        }
      ],
      relationships: [
        {
          fromTable: 'orders',
          fromColumn: 'customer_id',
          toTable: 'customers',
          toColumn: 'id',
          type: 'one-to-many'
        }
      ]
    };
  }
};

export const cohortAnalysisTemplate: TemplatePlugin = {
  id: 'cohort-analysis-template',
  name: 'Cohort Analysis Template',
  version: '1.0.0',
  description: 'Pre-built cohort analysis for SaaS retention metrics',
  author: 'AURA Team',
  category: 'template',
  vertical: 'saas',
  useCase: 'retention_analysis',
  sqlTemplate: `
    WITH user_cohorts AS (
      SELECT 
        user_id,
        DATE_TRUNC('month', signup_date) as cohort_month
      FROM users
      WHERE signup_date >= '{{start_date}}'
    ),
    user_activities AS (
      SELECT 
        uc.user_id,
        uc.cohort_month,
        DATE_TRUNC('month', activity_date) as activity_month,
        ROW_NUMBER() OVER (PARTITION BY uc.user_id, DATE_TRUNC('month', activity_date) ORDER BY activity_date) as rn
      FROM user_cohorts uc
      JOIN user_activities ua ON uc.user_id = ua.user_id
      WHERE ua.activity_date >= uc.cohort_month
    )
    SELECT 
      cohort_month,
      activity_month,
      COUNT(DISTINCT user_id) as active_users,
      EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) as period_number
    FROM user_activities
    WHERE rn = 1
    GROUP BY cohort_month, activity_month
    ORDER BY cohort_month, activity_month;
  `,
  parameterMapping: {
    'start_date': 'Analysis start date'
  },
  expectedSchema: {
    tables: [
      {
        name: 'users',
        columns: [
          { name: 'user_id', type: 'bigint', nullable: false },
          { name: 'signup_date', type: 'timestamp', nullable: false }
        ]
      },
      {
        name: 'user_activities',
        columns: [
          { name: 'user_id', type: 'bigint', nullable: false },
          { name: 'activity_date', type: 'timestamp', nullable: false }
        ]
      }
    ],
    relationships: []
  }
};

// Global plugin registry instance
export const pluginRegistry = new PluginRegistry();