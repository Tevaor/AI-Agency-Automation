import React from 'react';

interface NodePaletteProps {
  onDragStart: (event: React.DragEvent<HTMLDivElement>, nodeType: string, nodeData: any) => void;
}

const NodePalette: React.FC<NodePaletteProps> = ({ onDragStart }) => {
  const onDrag = (event: React.DragEvent<HTMLDivElement>, nodeType: string, nodeData: any) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ nodeType, nodeData }));
    event.dataTransfer.effectAllowed = 'move';
    onDragStart(event, nodeType, nodeData);
  };

  const nodes = [
    {
      id: 'trigger',
      label: 'Trigger',
      type: 'trigger',
      icon: '⚡',
      color: '#4CAF50',
      data: { label: 'New Trigger', status: 'pending', config: {} }
    },
    {
      id: 'agent',
      label: 'AI Agent',
      type: 'agent',
      icon: '🤖',
      color: '#2196F3',
      data: { label: 'New AI Agent', status: 'pending', config: {} }
    },
    {
      id: 'action',
      label: 'Action',
      type: 'action',
      icon: '🎯',
      color: '#9C27B0',
      data: { label: 'New Action', status: 'pending', config: {} }
    },
    {
      id: 'condition',
      label: 'Condition',
      type: 'condition',
      icon: '🔀',
      color: '#FF9800',
      data: { label: 'New Condition', status: 'pending', config: {} }
    },
    {
      id: 'delay',
      label: 'Delay',
      type: 'delay',
      icon: '⏳',
      color: '#607D8B',
      data: { label: 'New Delay', status: 'pending', config: {} }
    },
    {
      id: 'webhook',
      label: 'Webhook',
      type: 'webhook',
      icon: '🔗',
      color: '#795548',
      data: { label: 'New Webhook', status: 'pending', config: {} }
    },
  ];

  return (
    <div className="node-palette">
      <h4>Nodes</h4>
      <div className="nodes-list">
        {nodes.map((node) => (
          <div
            key={node.id}
            className="dndnode"
            onDragStart={(event) => onDrag(event, node.type, node.data)}
            draggable
            style={{ borderLeft: `5px solid ${node.color}` }}
          >
            <span className="node-icon" style={{ color: node.color }}>{node.icon}</span>
            <span className="node-label">{node.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NodePalette; 