import { memo } from 'react';
import { Handle, Position } from '@xyflow/react';

interface ActionNodeProps {
  data: {
    label: string;
    status: 'pending' | 'running' | 'success' | 'failed' | 'paused';
    group?: string;
    color?: string;
    config?: any;
    duration?: number;
  };
}

const ActionNode = memo(({ data }: ActionNodeProps) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return '#9E9E9E';
      case 'running': return '#2196F3';
      case 'success': return '#4CAF50';
      case 'failed': return '#F44336';
      case 'paused': return '#FF9800';
      default: return '#9E9E9E';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending': return '⏳';
      case 'running': return '🔄';
      case 'success': return '✅';
      case 'failed': return '❌';
      case 'paused': return '⏸️';
      default: return '⏳';
    }
  };

  return (
    <div
      className="action-node"
      style={{
        border: `2px solid ${data.color || '#9C27B0'}`,
        backgroundColor: '#fff',
        borderRadius: '8px',
        padding: '12px',
        minWidth: '160px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
      }}
    >
      <Handle
        type="target"
        position={Position.Left}
        style={{ background: data.color || '#9C27B0' }}
      />
      <Handle
        type="source"
        position={Position.Right}
        style={{ background: data.color || '#9C27B0' }}
      />
      
      <div className="node-header">
        <div className="node-icon" style={{ color: data.color || '#9C27B0' }}>
          🎯
        </div>
        <div className="node-title">
          <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>
            {data.label}
          </h4>
          <span style={{ fontSize: '12px', color: '#666' }}>
            Action
          </span>
        </div>
      </div>

      <div className="node-status">
        <span
          className="status-indicator"
          style={{
            color: getStatusColor(data.status),
            fontSize: '16px',
            marginRight: '4px'
          }}
        >
          {getStatusIcon(data.status)}
        </span>
        <span
          className="status-text"
          style={{
            fontSize: '12px',
            color: getStatusColor(data.status),
            textTransform: 'capitalize'
          }}
        >
          {data.status}
        </span>
        {data.duration && (
          <span style={{ fontSize: '11px', color: '#666', marginLeft: '8px' }}>
            ({data.duration}ms)
          </span>
        )}
      </div>

      {data.config && (
        <div className="node-config">
          <div className="config-item">
            <span className="config-label">Platform:</span>
            <span className="config-value">{data.config.platform || 'N/A'}</span>
          </div>
          <div className="config-item">
            <span className="config-label">Action:</span>
            <span className="config-value">{data.config.action || 'N/A'}</span>
          </div>
        </div>
      )}

      {data.group && (
        <div className="node-group">
          <span className="group-tag" style={{ backgroundColor: data.color || '#9C27B0' }}>
            {data.group}
          </span>
        </div>
      )}
    </div>
  );
});

ActionNode.displayName = 'ActionNode';

export default ActionNode; 