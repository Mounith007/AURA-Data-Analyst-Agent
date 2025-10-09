import React, { useState } from 'react';

interface VerticalConfig {
  id: string;
  name: string;
  description: string;
  icon: string;
  metrics: string[];
  connectors: string[];
  templates: string[];
  sampleQueries: string[];
}

const verticalConfigs: VerticalConfig[] = [
  {
    id: 'ecommerce',
    name: 'E-commerce',
    description: 'Complete analytics for online retail businesses',
    icon: '🛒',
    metrics: ['Conversion Rate', 'AOV', 'LTV:CAC', 'Cart Abandonment', 'Revenue per Visitor'],
    connectors: ['Shopify', 'WooCommerce', 'Stripe', 'Google Analytics', 'Facebook Ads', 'Amazon Seller Central'],
    templates: ['Customer Segmentation', 'Inventory Forecasting', 'Churn Prediction', 'Product Performance', 'Marketing Attribution'],
    sampleQueries: [
      'Show me the top 10 products by revenue this month',
      'What is our customer acquisition cost by channel?',
      'Which customers are at risk of churning?',
      'Analyze seasonal trends in our product categories'
    ]
  },
  {
    id: 'saas',
    name: 'SaaS Startups',
    description: 'Growth analytics for software-as-a-service companies',
    icon: '💻',
    metrics: ['MRR', 'ARR', 'Churn Rate', 'NPS', 'Activation Rate', 'Feature Adoption'],
    connectors: ['Stripe', 'Mixpanel', 'Amplitude', 'Intercom', 'HubSpot', 'Segment'],
    templates: ['Cohort Analysis', 'Feature Usage', 'Subscription Health', 'Expansion Revenue', 'User Journey'],
    sampleQueries: [
      'What is our monthly recurring revenue trend?',
      'Which features correlate with user retention?',
      'Show me cohort retention by signup month',
      'Analyze our freemium to paid conversion funnel'
    ]
  },
  {
    id: 'fintech',
    name: 'FinTech',
    description: 'Financial services and payment analytics',
    icon: '💳',
    metrics: ['Transaction Volume', 'Processing Fees', 'Fraud Rate', 'Settlement Time', 'Compliance Score'],
    connectors: ['Plaid', 'Stripe Connect', 'Square', 'PayPal', 'Dwolla', 'Yodlee'],
    templates: ['Fraud Detection', 'Risk Assessment', 'Transaction Analysis', 'Regulatory Reporting', 'Customer Due Diligence'],
    sampleQueries: [
      'Identify unusual transaction patterns',
      'Calculate our fraud detection accuracy',
      'Show transaction volume by geography',
      'Analyze payment method preferences'
    ]
  }
];

interface VerticalSelectorProps {
  onVerticalSelect: (vertical: VerticalConfig) => void;
  selectedVertical?: VerticalConfig;
}

const VerticalSelector: React.FC<VerticalSelectorProps> = ({ onVerticalSelect, selectedVertical }) => {
  const [showDetails, setShowDetails] = useState<string | null>(null);

  return (
    <div className="vertical-selector">
      <div className="selector-header">
        <h2>🎯 Choose Your Industry Vertical</h2>
        <p>AURA adapts to your industry's specific needs, metrics, and workflows</p>
      </div>
      
      <div className="vertical-grid">
        {verticalConfigs.map((vertical) => (
          <div 
            key={vertical.id}
            className={`vertical-card ${selectedVertical?.id === vertical.id ? 'selected' : ''}`}
            onClick={() => onVerticalSelect(vertical)}
            onMouseEnter={() => setShowDetails(vertical.id)}
            onMouseLeave={() => setShowDetails(null)}
          >
            <div className="card-header">
              <span className="vertical-icon">{vertical.icon}</span>
              <h3>{vertical.name}</h3>
            </div>
            
            <p className="vertical-description">{vertical.description}</p>
            
            <div className="vertical-features">
              <div className="feature-section">
                <h4>📊 Key Metrics</h4>
                <div className="feature-tags">
                  {vertical.metrics.slice(0, 3).map((metric) => (
                    <span key={metric} className="metric-tag">{metric}</span>
                  ))}
                  {vertical.metrics.length > 3 && (
                    <span className="more-tag">+{vertical.metrics.length - 3} more</span>
                  )}
                </div>
              </div>
              
              <div className="feature-section">
                <h4>🔌 Pre-built Connectors</h4>
                <div className="feature-tags">
                  {vertical.connectors.slice(0, 3).map((connector) => (
                    <span key={connector} className="connector-tag">{connector}</span>
                  ))}
                  {vertical.connectors.length > 3 && (
                    <span className="more-tag">+{vertical.connectors.length - 3} more</span>
                  )}
                </div>
              </div>
            </div>
            
            {selectedVertical?.id === vertical.id && (
              <div className="selected-indicator">
                ✅ Active Vertical
              </div>
            )}
          </div>
        ))}
      </div>
      
      {showDetails && (
        <div className="vertical-details">
          {(() => {
            const vertical = verticalConfigs.find(v => v.id === showDetails);
            if (!vertical) return null;
            
            return (
              <div className="details-content">
                <h3>{vertical.icon} {vertical.name} - Deep Dive</h3>
                
                <div className="details-grid">
                  <div className="detail-section">
                    <h4>🎯 Industry Templates</h4>
                    <ul>
                      {vertical.templates.map((template) => (
                        <li key={template}>{template}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="detail-section">
                    <h4>💬 Sample Questions You Can Ask</h4>
                    <ul>
                      {vertical.sampleQueries.map((query) => (
                        <li key={query}>"{query}"</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })()}
        </div>
      )}
      
      {selectedVertical && (
        <div className="current-vertical-status">
          <div className="status-content">
            <span className="status-icon">{selectedVertical.icon}</span>
            <div className="status-text">
              <strong>AURA for {selectedVertical.name}</strong>
              <p>Specialized for {selectedVertical.description.toLowerCase()}</p>
            </div>
            <button 
              className="change-vertical-btn"
              onClick={() => setShowDetails(selectedVertical.id)}
            >
              View Details
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export { VerticalSelector, verticalConfigs };
export type { VerticalConfig };