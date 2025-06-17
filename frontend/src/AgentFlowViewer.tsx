import React, { useCallback } from 'react';
import type { Connection, Node, NodeTypes } from '@xyflow/react';
import { ReactFlow, MiniMap, Controls, Background, useNodesState, useEdgesState, addEdge, Position, Handle } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

interface WorkflowNodeData {
  label: string;
  status: string;
  color: string;
  config: { [key: string]: any }; // Refined to allow string indexing
  logs?: string[];
  [key: string]: any; // Add index signature
}

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
const initialNodes: Node<WorkflowNodeData>[] = [
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
      label: 'Send WhatsApp Message',
      status: 'pending',
      color: '#9C27B0',
      config: { platform: 'whatsapp', action_type: 'send_message' }
    }
  }
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', label: '1 item' },
  { id: 'e2-3', source: '2', target: '3' },
  { id: 'e2-4', source: '2', target: '4', style: { strokeDasharray: '5 5' }, label: 'Chat Model*' },
  { id: 'e2-5', source: '2', target: '5', style: { strokeDasharray: '5 5' }, label: 'Memory' },
];

function AgentFlowViewer() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback((params: Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  return (
    <div className="reactflow-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}

export default AgentFlowViewer; 