import React, { useState } from 'react';
import { VerticalSelector, type VerticalConfig } from './VerticalSelector';
import { pluginRegistry, shopifyConnectorPlugin, cohortAnalysisTemplate } from '../plugins/PluginSystem';
import './VerticalSelector.css';
import './StrategicDemo.css';

interface StrategicDemoProps {
  onVerticalSelect: (vertical: VerticalConfig) => void;
}

const StrategicDemo: React.FC<StrategicDemoProps> = ({ onVerticalSelect }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedVertical, setSelectedVertical] = useState<VerticalConfig | null>(null);
  const [showPluginDemo, setShowPluginDemo] = useState(false);

  // Initialize plugin registry with example plugins
  React.useEffect(() => {
    pluginRegistry.installPlugin(shopifyConnectorPlugin);
    pluginRegistry.installPlugin(cohortAnalysisTemplate);
    pluginRegistry.enablePlugin('shopify-connector');
    pluginRegistry.enablePlugin('cohort-analysis-template');
  }, []);

  const strategicPillars = [
    {
      id: 'vertical',
      title: '🎯 Hyper-Focus on Niche Vertical',
      subtitle: 'Depth over Breadth Strategy',
      description: 'Instead of a generic data agent, AURA becomes the "AURA for E-commerce" or "AURA for SaaS Startups"',
      benefits: [
        'Domain-specific knowledge of industry jargon and metrics',
        'Pre-built connectors for vertical-specific tools',
        'Templated models for common industry use cases',
        'Faster time-to-value for customers'
      ],
      demo: <VerticalSelector onVerticalSelect={(v) => {
        setSelectedVertical(v);
        onVerticalSelect(v);
      }} selectedVertical={selectedVertical || undefined} />
    },
    {
      id: 'extensible',
      title: '🔧 Radically Open & Extensible',
      subtitle: 'Platform Moat Strategy',
      description: 'Build AURA like VS Code - extensible, open, and community-driven',
      benefits: [
        'Bring Your Own Warehouse - works with existing infrastructure',
        'Plugin marketplace for connectors and transformations',
        'Open-source core builds trust and community',
        'Reduces vendor lock-in concerns'
      ],
      demo: showPluginDemo ? (
        <div className="plugin-marketplace-demo">
          <h3>🏪 AURA Plugin Marketplace</h3>
          <div className="plugin-grid">
            {pluginRegistry.getAllPlugins().map(plugin => (
              <div key={plugin.id} className="plugin-card">
                <div className="plugin-header">
                  <span className="plugin-icon">{plugin.icon || '🔌'}</span>
                  <div>
                    <h4>{plugin.name}</h4>
                    <p className="plugin-version">v{plugin.version}</p>
                  </div>
                </div>
                <p className="plugin-description">{plugin.description}</p>
                <div className="plugin-meta">
                  <span className="plugin-category">{plugin.category}</span>
                  <span className="plugin-author">by {plugin.author}</span>
                </div>
                <button className="install-btn">
                  ✅ Installed
                </button>
              </div>
            ))}
          </div>
          <div className="marketplace-actions">
            <button className="primary-btn">Browse All Plugins</button>
            <button className="secondary-btn">Develop a Plugin</button>
          </div>
        </div>
      ) : (
        <button 
          className="demo-trigger-btn"
          onClick={() => setShowPluginDemo(true)}
        >
          🏪 Show Plugin Marketplace Demo
        </button>
      )
    },
    {
      id: 'glassbox',
      title: '🔍 Glass Box AI for Trust',
      subtitle: 'Adoption Moat Strategy',  
      description: 'Transparent, auditable AI that shows its work and allows human collaboration',
      benefits: [
        'Every generated query/code is reviewed before execution',
        'Version control for all AI outputs',  
        'Human-in-the-loop corrections and learning',
        'Builds trust with data professionals'
      ],
      demo: (
        <div className="glassbox-demo">
          <h3>🔍 Glass Box Transparency</h3>
          <div className="transparency-features">
            <div className="feature">
              <h4>📝 Code Review Interface</h4>
              <p>AI-generated SQL is presented for human review and editing</p>
              <div className="mockup">
                <div className="code-mockup">
                  <div className="code-header">🤖 AI Generated → 👤 Human Reviewed</div>
                  <pre><code>SELECT product_name, SUM(revenue) FROM sales GROUP BY product_name</code></pre>
                  <div className="review-actions">
                    <button className="edit-btn">✏️ Edit</button>
                    <button className="approve-btn">✅ Approve</button>
                  </div>
                </div>
              </div>
            </div>
            <div className="feature">
              <h4>📚 Version History</h4>
              <p>Track all changes and decisions made by AI and humans</p>
              <div className="version-list">
                <div className="version-item ai">🤖 v1 - Initial AI generation</div>
                <div className="version-item human">👤 v2 - Human optimization</div>
                <div className="version-item ai">🤖 v3 - AI refinement</div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'unified',
      title: '✨ Superior Unified Experience',
      subtitle: 'Stickiness Moat Strategy',
      description: 'One conversation, one context - seamless workflow from schema design to analysis',
      benefits: [
        'Single context across the entire data workflow',
        'Lightning-fast conversational interface',
        'No context switching between tools',
        'Delightful user experience as a competitive advantage'
      ],
      demo: (
        <div className="unified-experience-demo">
          <h3>✨ Unified Data Workflow</h3>
          <div className="workflow-steps">
            <div className="workflow-step active">
              <div className="step-number">1</div>
              <div className="step-content">
                <h4>💬 Natural Language Query</h4>
                <p>"Show me our top customers by revenue this quarter"</p>
              </div>
            </div>
            <div className="workflow-arrow">→</div>
            <div className="workflow-step active">
              <div className="step-number">2</div>
              <div className="step-content">
                <h4>🔍 Glass Box Review</h4>
                <p>Generated SQL presented for approval</p>
              </div>
            </div>
            <div className="workflow-arrow">→</div>
            <div className="workflow-step active">
              <div className="step-number">3</div>
              <div className="step-content">
                <h4>📊 Smart Visualization</h4>
                <p>Automatic chart selection and rendering</p>
              </div>
            </div>
            <div className="workflow-arrow">→</div>
            <div className="workflow-step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h4>🧠 AI Insights</h4>
                <p>Contextual analysis and recommendations</p>
              </div>
            </div>
          </div>
          <div className="context-continuity">
            <h4>🔗 Context Continuity</h4>
            <p>Follow-up: "Now show me the trend over the last 6 months" - AI remembers the previous context</p>
          </div>
        </div>
      )
    }
  ];

  return (
    <div className="strategic-demo">
      <div className="demo-header">
        <h1>🚀 AURA's Sustainable Development Strategy</h1>
        <p className="strategy-subtitle">
          The 4 Pillars for Competing with Big Tech Through Focused Excellence
        </p>
        <div className="value-proposition">
          <strong>Core Strategy:</strong> Solve 100% of needs for a specific vertical, 
          rather than 80% of needs for 80% of the market
        </div>
      </div>

      <div className="pillars-navigation">
        {strategicPillars.map((pillar, index) => (
          <button
            key={pillar.id}
            className={`pillar-nav ${currentStep === index ? 'active' : ''}`}
            onClick={() => setCurrentStep(index)}
          >
            <span className="pillar-number">{index + 1}</span>
            <span className="pillar-title">{pillar.title}</span>
          </button>
        ))}
      </div>

      <div className="pillar-content">
        {strategicPillars[currentStep] && (
          <div className="pillar-detail">
            <div className="pillar-header">
              <h2>{strategicPillars[currentStep].title}</h2>
              <h3 className="pillar-subtitle">{strategicPillars[currentStep].subtitle}</h3>
              <p className="pillar-description">{strategicPillars[currentStep].description}</p>
            </div>

            <div className="pillar-body">
              <div className="benefits-section">
                <h4>🎯 Strategic Benefits</h4>
                <ul className="benefits-list">
                  {strategicPillars[currentStep].benefits.map((benefit, index) => (
                    <li key={index}>{benefit}</li>
                  ))}
                </ul>
              </div>

              <div className="demo-section">
                <h4>🎪 Interactive Demo</h4>
                <div className="demo-container">
                  {strategicPillars[currentStep].demo}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="rollout-plan">
        <h2>📋 Phased Rollout Plan</h2>
        <div className="phases">
          <div className="phase current">
            <h3>Phase 1: MVP - "Analyst in a Box" ✅</h3>
            <p>Connect to existing data warehouse. Nail NLP-to-SQL-to-Visualization with Glass Box approach for one vertical.</p>
            <div className="phase-status completed">Current Status: Completed</div>
          </div>
          <div className="phase next">
            <h3>Phase 2: "Engineer & Analyst Team" 🔧</h3>
            <p>Expand into NLP-driven data ingestion and transformation. Deep integration with dbt and data engineering workflows.</p>
            <div className="phase-status in-progress">Status: In Development</div>
          </div>
          <div className="phase future">
            <h3>Phase 3: "Full Vision" 🚀</h3>
            <p>Incorporate data science persona with AutoML and forecasting. Complete end-to-end unified experience.</p>
            <div className="phase-status planned">Status: Planned</div>
          </div>
        </div>
      </div>

      <div className="competitive-advantage">
        <h2>⚡ Why This Strategy Wins</h2>
        <div className="advantage-grid">
          <div className="advantage-card">
            <h3>🎯 Focus Beats Scale</h3>
            <p>Big tech must serve everyone. We serve one vertical perfectly.</p>
          </div>
          <div className="advantage-card">
            <h3>🔓 Open Beats Closed</h3>
            <p>No vendor lock-in. Customers keep control of their data and tools.</p>
          </div>
          <div className="advantage-card">
            <h3>👥 Trust Beats Magic</h3>
            <p>Transparent AI builds trust with data professionals who need to audit and explain results.</p>
          </div>
          <div className="advantage-card">
            <h3>⚡ Speed Beats Features</h3>
            <p>Unified experience eliminates context switching and delivers faster insights.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StrategicDemo;