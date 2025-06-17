import React, { useState, useCallback } from 'react';
import type { Connection, NodeTypes } from '@xyflow/react';
import { 
  MiniMap, 
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Panel,
  ReactFlowProvider,
  Handle,
  Position,
  ReactFlow
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import type { WorkflowNodeData } from './types';

// Custom Node Components
const TriggerNode = React.memo(({ data }: { data: WorkflowNodeData }) => (
  <div style={{
    border: `2px solid ${data.color || '#4CAF50'}`,
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '12px',
    minWidth: '150px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}>
    <Handle type="source" position={Position.Right} style={{ background: data.color || '#4CAF50' }} />
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <span style={{ color: data.color || '#4CAF50', fontSize: '16px' }}>⚡</span>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>{data.label}</h4>
        <span style={{ fontSize: '12px', color: '#666' }}>Trigger</span>
      </div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ 
        color: data.status === 'running' ? '#2196F3' : data.status === 'success' ? '#4CAF50' : '#9E9E9E',
        fontSize: '16px'
      }}>
        {data.status === 'running' ? '🔄' : data.status === 'success' ? '✅' : '⏳'}
      </span>
      <span style={{ fontSize: '12px', textTransform: 'capitalize' }}>{data.status}</span>
    </div>
  </div>
));

const AgentNode = React.memo(({ data }: { data: WorkflowNodeData }) => (
  <div style={{
    border: `2px solid ${data.color || '#2196F3'}`,
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '12px',
    minWidth: '180px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}>
    <Handle type="target" position={Position.Left} style={{ background: data.color || '#2196F3' }} />
    <Handle type="source" position={Position.Right} style={{ background: data.color || '#2196F3' }} />
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <span style={{ color: data.color || '#2196F3', fontSize: '16px' }}>🤖</span>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>{data.label}</h4>
        <span style={{ fontSize: '12px', color: '#666' }}>AI Agent</span>
      </div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ 
        color: data.status === 'running' ? '#2196F3' : data.status === 'success' ? '#4CAF50' : '#9E9E9E',
        fontSize: '16px'
      }}>
        {data.status === 'running' ? '🔄' : data.status === 'success' ? '✅' : '⏳'}
      </span>
      <span style={{ fontSize: '12px', textTransform: 'capitalize' }}>{data.status}</span>
    </div>
  </div>
));

const ActionNode = React.memo(({ data }: { data: WorkflowNodeData }) => (
  <div style={{
    border: `2px solid ${data.color || '#9C27B0'}`,
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '12px',
    minWidth: '160px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}>
    <Handle type="target" position={Position.Left} style={{ background: data.color || '#9C27B0' }} />
    <Handle type="source" position={Position.Right} style={{ background: data.color || '#9C27B0' }} />
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <span style={{ color: data.color || '#9C27B0', fontSize: '16px' }}>🎯</span>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>{data.label}</h4>
        <span style={{ fontSize: '12px', color: '#666' }}>Action</span>
      </div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ 
        color: data.status === 'running' ? '#2196F3' : data.status === 'success' ? '#4CAF50' : '#9E9E9E',
        fontSize: '16px'
      }}>
        {data.status === 'running' ? '🔄' : data.status === 'success' ? '✅' : '⏳'}
      </span>
      <span style={{ fontSize: '12px', textTransform: 'capitalize' }}>{data.status}</span>
    </div>
  </div>
));

const ConditionNode = React.memo(({ data }: { data: WorkflowNodeData }) => (
  <div style={{
    border: `2px solid ${data.color || '#FF9800'}`,
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '12px',
    minWidth: '140px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}>
    <Handle type="target" position={Position.Left} style={{ background: data.color || '#FF9800' }} />
    <Handle type="source" position={Position.Right} style={{ background: data.color || '#FF9800' }} />
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <span style={{ color: data.color || '#FF9800', fontSize: '16px' }}>🔀</span>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>{data.label}</h4>
        <span style={{ fontSize: '12px', color: '#666' }}>Condition</span>
      </div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ 
        color: data.status === 'running' ? '#2196F3' : data.status === 'success' ? '#4CAF50' : '#9E9E9E',
        fontSize: '16px'
      }}>
        {data.status === 'running' ? '🔄' : data.status === 'success' ? '✅' : '⏳'}
      </span>
      <span style={{ fontSize: '12px', textTransform: 'capitalize' }}>{data.status}</span>
    </div>
  </div>
));

const WebhookNode = React.memo(({ data }: { data: WorkflowNodeData }) => (
  <div style={{
    border: `2px solid ${data.color || '#795548'}`,
    backgroundColor: '#fff',
    borderRadius: '8px',
    padding: '12px',
    minWidth: '140px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  }}>
    <Handle type="target" position={Position.Left} style={{ background: data.color || '#795548' }} />
    <Handle type="source" position={Position.Right} style={{ background: data.color || '#795548' }} />
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
      <span style={{ color: data.color || '#795548', fontSize: '16px' }}>🔗</span>
      <div>
        <h4 style={{ margin: '0 0 4px 0', fontSize: '14px', fontWeight: '600' }}>{data.label}</h4>
        <span style={{ fontSize: '12px', color: '#666' }}>Webhook</span>
      </div>
    </div>
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
      <span style={{ 
        color: data.status === 'running' ? '#2196F3' : data.status === 'success' ? '#4CAF50' : '#9E9E9E',
        fontSize: '16px'
      }}>
        {data.status === 'running' ? '🔄' : data.status === 'success' ? '✅' : '⏳'}
      </span>
      <span style={{ fontSize: '12px', textTransform: 'capitalize' }}>{data.status}</span>
    </div>
  </div>
));

const nodeTypes: NodeTypes = {
  trigger: TriggerNode,
  agent: AgentNode,
  action: ActionNode,
  condition: ConditionNode,
  webhook: WebhookNode,
};

// Enhanced initial nodes with status and configuration
const initialNodes = [
  { 
    id: '1', 
    type: 'trigger', 
    position: { x: 0, y: 0 }, 
    data: { 
      label: 'WhatsApp Trigger',
      status: 'pending',
      color: '#4CAF50',
      config: { platform: 'whatsapp', event: 'message_received' }
    } 
  },
  { 
    id: '2', 
    type: 'agent',
    position: { x: 250, y: 0 }, 
    data: { 
      label: 'AI Response Agent',
      status: 'running',
      color: '#2196F3',
      config: { model: 'gpt-4', memory: true },
      logs: ['Processing message...', 'Generating response...']
    } 
  },
  { 
    id: '3', 
    type: 'condition',
    position: { x: 500, y: 0 }, 
    data: { 
      label: 'Intent Check',
      status: 'pending',
      color: '#FF9800',
      config: { conditions: ['support', 'sales'] }
    } 
  },
  { 
    id: '4', 
    type: 'action',
    position: { x: 750, y: -50 }, 
    data: { 
      label: 'Send Support Response',
      status: 'success',
      color: '#9C27B0',
      config: { platform: 'whatsapp', action: 'send_message' },
      duration: 1200
    } 
  },
  { 
    id: '5', 
    type: 'action',
    position: { x: 750, y: 50 }, 
    data: { 
      label: 'Send Sales Response',
      status: 'pending',
      color: '#9C27B0',
      config: { platform: 'whatsapp', action: 'send_message' }
    } 
  },
  { 
    id: '6', 
    type: 'webhook',
    position: { x: 1000, y: 0 }, 
    data: { 
      label: 'Log to CRM',
      status: 'pending',
      color: '#795548',
      config: { url: 'https://api.crm.com/webhook', method: 'POST' }
    } 
  },
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', label: 'message', style: { stroke: '#4CAF50', strokeWidth: 2 } },
  { id: 'e2-3', source: '2', target: '3', label: 'intent', style: { stroke: '#2196F3', strokeWidth: 2 } },
  { id: 'e3-4', source: '3', target: '4', label: 'support', style: { stroke: '#FF9800', strokeWidth: 2 } },
  { id: 'e3-5', source: '3', target: '5', label: 'sales', style: { stroke: '#FF9800', strokeWidth: 2 } },
  { id: 'e4-6', source: '4', target: '6', label: 'log', style: { stroke: '#9C27B0', strokeWidth: 2 } },
  { id: 'e5-6', source: '5', target: '6', label: 'log', style: { stroke: '#9C27B0', strokeWidth: 2 } },
];

const NodePalette = ({ onAddNode: _ }: { onAddNode: (nodeType: string, nodeData: any) => void }) => {
  const onDragStart = (event: React.DragEvent<HTMLDivElement>, nodeType: string, nodeData: any) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ nodeType, nodeData }));
    event.dataTransfer.effectAllowed = 'move';
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
    <Panel position="top-left" className="node-palette">
      <h4>Nodes</h4>
      <div className="nodes-list">
        {nodes.map((node) => (
          <div
            key={node.id}
            className="dndnode"
            onDragStart={(event) => onDragStart(event, node.type, node.data)}
            draggable
            style={{ borderLeft: `5px solid ${node.color}` }}
          >
            <span className="node-icon" style={{ color: node.color }}>{node.icon}</span>
            <span className="node-label">{node.label}</span>
          </div>
        ))}
      </div>
    </Panel>
  );
};

const ExecutionControls = ({
  isExecuting,
  onStart,
  onPause,
  onReset
}: {
  isExecuting: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
}) => (
  <Panel position="top-right" className="execution-controls">
    <button onClick={onStart} disabled={isExecuting} className="control-button run">▶️ Run</button>
    <button onClick={onPause} disabled={!isExecuting} className="control-button pause">⏸️ Pause</button>
    <button onClick={onReset} className="control-button reset">🔄 Reset</button>
  </Panel>
);

const ExecutionMonitor = ({ nodes }: { nodes: any[] }) => {
  const [activeTab, setActiveTab] = useState<'live' | 'history' | 'logs'>('live');

  // Calculate execution statistics
  const stats = {
    total: nodes.length,
    pending: nodes.filter(n => n.data.status === 'pending').length,
    running: nodes.filter(n => n.data.status === 'running').length,
    success: nodes.filter(n => n.data.status === 'success').length,
    failed: nodes.filter(n => n.data.status === 'failed').length,
    paused: nodes.filter(n => n.data.status === 'paused').length,
  };

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
    <Panel position="bottom-left" className="execution-monitor">
      <div className="monitor-tabs">
        <button
          className={`monitor-tab ${activeTab === 'live' ? 'active' : ''}`}
          onClick={() => setActiveTab('live')}
        >
          🔴 Live
        </button>
        <button
          className={`monitor-tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📈 History
        </button>
        <button
          className={`monitor-tab ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          📝 Logs
        </button>
      </div>

      {/* Live Status Overview */}
      {activeTab === 'live' && (
        <div className="live-status">
          <div className="status-overview">
            <div className="status-grid">
              <div className="status-item total">
                <span className="status-count">{stats.total}</span>
                <span className="status-label">Total</span>
              </div>
              <div className="status-item pending">
                <span className="status-count">{stats.pending}</span>
                <span className="status-label">Pending</span>
              </div>
              <div className="status-item running">
                <span className="status-count">{stats.running}</span>
                <span className="status-label">Running</span>
              </div>
              <div className="status-item success">
                <span className="status-count">{stats.success}</span>
                <span className="status-label">Success</span>
              </div>
              <div className="status-item failed">
                <span className="status-count">{stats.failed}</span>
                <span className="status-label">Failed</span>
              </div>
              <div className="status-item paused">
                <span className="status-count">{stats.paused}</span>
                <span className="status-label">Paused</span>
              </div>
            </div>
          </div>

          <div className="node-status-list">
            <h4>Node Status</h4>
            {nodes.map((node) => (
              <div key={node.id} className="node-status-item">
                <div className="node-status-header">
                  <span className="status-icon" style={{ color: getStatusColor(node.data.status) }}>
                    {getStatusIcon(node.data.status)}
                  </span>
                  <span className="node-name">{node.data.label}</span>
                  <span className="node-type">{node.type}</span>
                </div>
                <div className="node-status-details">
                  <span className="status-text">{node.data.status}</span>
                  {node.data.duration && (
                    <span className="duration">({node.data.duration}ms)</span>
                  )}
                </div>
                {node.data.logs && node.data.logs.length > 0 && (
                  <div className="node-logs">
                    {node.data.logs.slice(-2).map((log: string, index: number) => (
                      <div key={index} className="log-entry">
                        {log}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Execution History */}
      {activeTab === 'history' && (
        <div className="execution-history">
          <h4>Recent Executions</h4>
          {/* Mock history data */}
          <div className="no-history">
            <p>No execution history available (mock data removed for brevity).</p>
          </div>
        </div>
      )}

      {/* Logs */}
      {activeTab === 'logs' && (
        <div className="execution-logs">
          <h4>System Logs</h4>
          {/* Mock logs data */}
          <div className="logs-container">
            <div className="log-entry">
              <span className="log-timestamp">13:04:42</span>
              <span className="log-level info">INFO</span>
              <span className="log-message">Workflow execution started</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">13:04:43</span>
              <span className="log-level success">SUCCESS</span>
              <span className="log-message">WhatsApp trigger activated</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">13:04:44</span>
              <span className="log-level info">INFO</span>
              <span className="log-message">AI Agent processing message</span>
            </div>
            <div className="log-entry">
              <span className="log-timestamp">13:04:45</span>
              <span className="log-level success">SUCCESS</span>
              <span className="log-message">Response sent successfully</span>
            </div>
          </div>
        </div>
      )}
    </Panel>
  );
};

function EnhancedAgentFlowViewer() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes as any);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [isExecuting, setIsExecuting] = useState(false);

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  const onNodeDragStop = useCallback((_: any, node: any) => {
    // Update node position or other relevant data if needed
    setNodes((nds) =>
      nds.map((n) =>
        n.id === node.id ? { ...n, position: { x: node.position.x, y: node.position.y } } : n
      )
    );
  }, [setNodes]);

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const reactFlowBounds = event.currentTarget.getBoundingClientRect();
      const { nodeType, nodeData } = JSON.parse(event.dataTransfer.getData('application/reactflow'));

      // Calculate position relative to the ReactFlow instance
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      const newNode = {
        id: `node-${nodes.length + 1}`,
        type: nodeType,
        position,
        data: { ...nodeData, label: `${nodeType.charAt(0).toUpperCase() + nodeType.slice(1)} Node ${nodes.length + 1}` },
      };

      setNodes((nds) => nds.concat(newNode as any)); // Type assertion here
    },
    [nodes, setNodes]
  );

  const onStartExecution = () => {
    setIsExecuting(true);
    console.log("Execution Started!");
    // In a real app, trigger backend execution via API or WebSocket
  };

  const onPauseExecution = () => {
    setIsExecuting(false);
    console.log("Execution Paused.");
  };

  const onResetExecution = () => {
    setIsExecuting(false);
    setNodes(initialNodes as any);
    setEdges(initialEdges);
    console.log("Execution Reset.");
  };

  return (
    <div className="enhanced-agent-flow-viewer">
      <ReactFlowProvider>
        <div className="reactflow-wrapper" style={{ width: '100%', height: '100%' }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeDragStop={onNodeDragStop}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
            fitView
          >
            <MiniMap />
            <Controls />
            <Background />
            <NodePalette onAddNode={() => {}} /> {/* onAddNode is not used, but kept for compatibility */}
            <ExecutionControls
              isExecuting={isExecuting}
              onStart={onStartExecution}
              onPause={onPauseExecution}
              onReset={onResetExecution}
            />
            <ExecutionMonitor nodes={nodes} />
          </ReactFlow>
        </div>
      </ReactFlowProvider>
    </div>
  );
}

// Wrapper component to provide ReactFlowProvider
export default function EnhancedAgentFlowViewerWrapper() {
  return (
    <ReactFlowProvider>
      <EnhancedAgentFlowViewer />
    </ReactFlowProvider>
  );
} 