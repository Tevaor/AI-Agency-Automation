import React, { useState } from 'react';

interface AgentConfigPanelProps {
  node: any;
  onUpdateConfig: (nodeId: string, config: any) => void;
  onClose: () => void;
}

const AgentConfigPanel: React.FC<AgentConfigPanelProps> = ({
  node,
  onUpdateConfig,
  onClose,
}) => {
  const [config, setConfig] = useState(node.data.config || {});
  const [activeTab, setActiveTab] = useState<'general' | 'advanced' | 'logs'>('general');

  const handleConfigChange = (key: string, value: any) => {
    const newConfig = { ...config, [key]: value };
    setConfig(newConfig);
    onUpdateConfig(node.id, newConfig);
  };

  const renderGeneralConfig = () => (
    <div className="config-section">
      <div className="config-field">
        <label>Node Label</label>
        <input
          type="text"
          value={node.data.label}
          onChange={(e) => onUpdateConfig(node.id, { label: e.target.value })}
          placeholder="Enter node label"
        />
      </div>

      <div className="config-field">
        <label>Group</label>
        <select
          value={node.data.group || 'default'}
          onChange={(e) => onUpdateConfig(node.id, { group: e.target.value })}
        >
          <option value="campaign">Campaign</option>
          <option value="ai">AI</option>
          <option value="logic">Logic</option>
          <option value="response">Response</option>
          <option value="integration">Integration</option>
          <option value="default">Default</option>
        </select>
      </div>

      <div className="config-field">
        <label>Color</label>
        <input
          type="color"
          value={node.data.color || '#607D8B'}
          onChange={(e) => onUpdateConfig(node.id, { color: e.target.value })}
        />
      </div>

      {/* Node-specific configuration */}
      {node.data.type === 'trigger' && (
        <>
          <div className="config-field">
            <label>Platform</label>
            <select
              value={config.platform || ''}
              onChange={(e) => handleConfigChange('platform', e.target.value)}
            >
              <option value="whatsapp">WhatsApp</option>
              <option value="email">Email</option>
              <option value="webhook">Webhook</option>
              <option value="slack">Slack</option>
            </select>
          </div>
          <div className="config-field">
            <label>Event Type</label>
            <input
              type="text"
              value={config.event || ''}
              onChange={(e) => handleConfigChange('event', e.target.value)}
              placeholder="e.g., message_received"
            />
          </div>
        </>
      )}

      {node.data.type === 'agent' && (
        <>
          <div className="config-field">
            <label>AI Model</label>
            <select
              value={config.model || ''}
              onChange={(e) => handleConfigChange('model', e.target.value)}
            >
              <option value="gpt-4">GPT-4</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              <option value="claude-3">Claude 3</option>
              <option value="custom">Custom Model</option>
            </select>
          </div>
          <div className="config-field">
            <label>Context</label>
            <input
              type="text"
              value={config.context || ''}
              onChange={(e) => handleConfigChange('context', e.target.value)}
              placeholder="e.g., customer_service"
            />
          </div>
          <div className="config-field">
            <label>
              <input
                type="checkbox"
                checked={config.memory || false}
                onChange={(e) => handleConfigChange('memory', e.target.checked)}
              />
              Enable Memory
            </label>
          </div>
        </>
      )}

      {node.data.type === 'action' && (
        <>
          <div className="config-field">
            <label>Platform</label>
            <select
              value={config.platform || ''}
              onChange={(e) => handleConfigChange('platform', e.target.value)}
            >
              <option value="whatsapp">WhatsApp</option>
              <option value="email">Email</option>
              <option value="slack">Slack</option>
              <option value="api">API</option>
            </select>
          </div>
          <div className="config-field">
            <label>Action</label>
            <select
              value={config.action || ''}
              onChange={(e) => handleConfigChange('action', e.target.value)}
            >
              <option value="send_message">Send Message</option>
              <option value="create_record">Create Record</option>
              <option value="update_record">Update Record</option>
              <option value="api_call">API Call</option>
            </select>
          </div>
          <div className="config-field">
            <label>Template</label>
            <input
              type="text"
              value={config.template || ''}
              onChange={(e) => handleConfigChange('template', e.target.value)}
              placeholder="e.g., support_response"
            />
          </div>
        </>
      )}

      {node.data.type === 'condition' && (
        <div className="config-field">
          <label>Conditions</label>
          <textarea
            value={JSON.stringify(config.conditions || [], null, 2)}
            onChange={(e) => {
              try {
                const conditions = JSON.parse(e.target.value);
                handleConfigChange('conditions', conditions);
              } catch (error) {
                // Invalid JSON, ignore
              }
            }}
            placeholder="Enter conditions as JSON array"
            rows={4}
          />
        </div>
      )}

      {node.data.type === 'webhook' && (
        <>
          <div className="config-field">
            <label>URL</label>
            <input
              type="url"
              value={config.url || ''}
              onChange={(e) => handleConfigChange('url', e.target.value)}
              placeholder="https://api.example.com/webhook"
            />
          </div>
          <div className="config-field">
            <label>Method</label>
            <select
              value={config.method || 'POST'}
              onChange={(e) => handleConfigChange('method', e.target.value)}
            >
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
            </select>
          </div>
        </>
      )}
    </div>
  );

  const renderAdvancedConfig = () => (
    <div className="config-section">
      <div className="config-field">
        <label>Timeout (seconds)</label>
        <input
          type="number"
          value={config.timeout || 30}
          onChange={(e) => handleConfigChange('timeout', parseInt(e.target.value))}
          min="1"
          max="300"
        />
      </div>

      <div className="config-field">
        <label>Retry Attempts</label>
        <input
          type="number"
          value={config.retries || 3}
          onChange={(e) => handleConfigChange('retries', parseInt(e.target.value))}
          min="0"
          max="10"
        />
      </div>

      <div className="config-field">
        <label>Priority</label>
        <select
          value={config.priority || 'normal'}
          onChange={(e) => handleConfigChange('priority', e.target.value)}
        >
          <option value="low">Low</option>
          <option value="normal">Normal</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      <div className="config-field">
        <label>Custom Headers</label>
        <textarea
          value={JSON.stringify(config.headers || {}, null, 2)}
          onChange={(e) => {
            try {
              const headers = JSON.parse(e.target.value);
              handleConfigChange('headers', headers);
            } catch (error) {
              // Invalid JSON, ignore
            }
          }}
          placeholder="Enter headers as JSON object"
          rows={3}
        />
      </div>
    </div>
  );

  const renderLogs = () => (
    <div className="config-section">
      <div className="logs-container">
        <h4>Recent Logs</h4>
        {node.data.logs && node.data.logs.length > 0 ? (
          <div className="log-list">
            {node.data.logs.map((log: string, index: number) => (
              <div key={index} className="log-entry">
                <span className="log-timestamp">
                  {new Date().toLocaleTimeString()}
                </span>
                <span className="log-message">{log}</span>
              </div>
            ))}
          </div>
        ) : (
          <p>No logs available</p>
        )}
      </div>
    </div>
  );

  return (
    <div className="agent-config-panel">
      <div className="config-header">
        <h3>⚙️ {node.data.label} Configuration</h3>
        <button className="close-btn" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="config-tabs">
        <button
          className={`config-tab ${activeTab === 'general' ? 'active' : ''}`}
          onClick={() => setActiveTab('general')}
        >
          General
        </button>
        <button
          className={`config-tab ${activeTab === 'advanced' ? 'active' : ''}`}
          onClick={() => setActiveTab('advanced')}
        >
          Advanced
        </button>
        <button
          className={`config-tab ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          Logs
        </button>
      </div>

      <div className="config-content">
        {activeTab === 'general' && renderGeneralConfig()}
        {activeTab === 'advanced' && renderAdvancedConfig()}
        {activeTab === 'logs' && renderLogs()}
      </div>

      <div className="config-footer">
        <button className="save-btn" onClick={() => onUpdateConfig(node.id, config)}>
          💾 Save Changes
        </button>
        <button className="reset-btn" onClick={() => setConfig(node.data.config || {})}>
          🔄 Reset
        </button>
      </div>
    </div>
  );
};

export default AgentConfigPanel; 