import React, { useState, useEffect } from 'react';
import type { WorkflowExecution } from '../types';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, type TooltipItem } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface ExecutionMonitorProps {
  workflowId: string;
  isVisible: boolean;
  onClose: () => void;
}

const ExecutionMonitor: React.FC<ExecutionMonitorProps> = ({
  workflowId,
  isVisible,
  onClose
}) => {
  const [execution, setExecution] = useState<WorkflowExecution | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'nodes' | 'logs'>('overview');

  // Mock data for demonstration
  useEffect(() => {
    if (isVisible && workflowId) {
      // In a real application, you would fetch data from the backend or WebSocket
      const mockExecution: WorkflowExecution = {
        execution_id: 'exec_123',
        workflow_id: workflowId,
        status: 'running',
        start_time: new Date().toISOString(),
        node_status: {
          'node-1': 'success',
          'node-2': 'running',
          'node-3': 'pending',
        },
        node_logs: {
          'node-1': ['Node 1 started', 'Node 1 finished successfully'],
          'node-2': ['Node 2 started', 'Processing data...'],
        },
        node_durations: {
          'node-1': 1.5,
        },
        errors: [],
        steps: [
          { node_id: 'node-1', status: 'success', log: 'Task A completed', timestamp: new Date().toISOString(), duration: 1000 },
          { node_id: 'node-2', status: 'running', log: 'Task B started', timestamp: new Date().toISOString(), duration: 0 },
        ]
      };
      setExecution(mockExecution);
    }
  }, [workflowId, isVisible]);

  if (!isVisible) {
    return null;
  }

  if (!execution) {
    return (
      <div className="execution-monitor">
        <div className="monitor-header">
          <h3>📊 Execution Monitor</h3>
          <button className="monitor-toggle" onClick={onClose}>✕</button>
        </div>
        <div className="monitor-content">
          <p>Loading execution data for workflow: {workflowId}...</p>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'var(--accent-success)';
      case 'failed': return 'var(--accent-error)';
      case 'running': return 'var(--accent-info)';
      case 'pending': return 'var(--text-muted)';
      case 'paused': return 'var(--accent-warning)';
      default: return 'var(--text-secondary)';
    }
  };

  const chartData = {
    labels: Object.keys(execution.node_durations),
    datasets: [
      {
        label: 'Node Duration (seconds)',
        data: Object.values(execution.node_durations),
        borderColor: 'var(--accent-primary)',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: 'var(--text-primary)'
        }
      },
      title: {
        display: true,
        text: 'Node Execution Durations',
        color: 'var(--text-primary)'
      },
      tooltip: {
        callbacks: {
          label: function(context: TooltipItem<'line'>) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-US', { style: 'unit', unit: 'second' }).format(context.parsed.y);
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: 'var(--text-secondary)'
        },
        grid: {
          color: 'var(--border-primary)'
        }
      },
      y: {
        ticks: {
          color: 'var(--text-secondary)'
        },
        grid: {
          color: 'var(--border-primary)'
        }
      }
    }
  };

  return (
    <div className="execution-monitor">
      <div className="monitor-header">
        <h3>📊 Execution Monitor - {execution.workflow_id}</h3>
        <button className="monitor-toggle" onClick={onClose}>✕</button>
      </div>

      <div className="monitor-tabs">
        <button
          className={`monitor-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`monitor-tab ${activeTab === 'nodes' ? 'active' : ''}`}
          onClick={() => setActiveTab('nodes')}
        >
          Nodes
        </button>
        <button
          className={`monitor-tab ${activeTab === 'logs' ? 'active' : ''}`}
          onClick={() => setActiveTab('logs')}
        >
          Logs
        </button>
      </div>

      <div className="monitor-content">
        {activeTab === 'overview' && (
          <div className="monitor-section">
            <h4>General Info</h4>
            <p><strong>Status:</strong> <span style={{ color: getStatusColor(execution.status) }}>{execution.status.toUpperCase()}</span></p>
            <p><strong>Started:</strong> {new Date(execution.start_time).toLocaleString()}</p>
            {execution.end_time && <p><strong>Ended:</strong> {new Date(execution.end_time).toLocaleString()}</p>}
            {execution.errors.length > 0 && (
              <div className="errors-list">
                <h4>Errors</h4>
                {execution.errors.map((error: string, index: number) => (
                  <p key={index} style={{ color: 'var(--accent-error)' }}>{error}</p>
                ))}
              </div>
            )}
            <div className="chart-container">
              <Line data={chartData} options={chartOptions} />
            </div>
          </div>
        )}

        {activeTab === 'nodes' && (
          <div className="monitor-section">
            <h4>Node Status</h4>
            {Object.entries(execution.node_status).map(([nodeId, status]) => (
              <div key={nodeId} className="node-status-item">
                <span><strong>{nodeId}:</strong> <span style={{ color: getStatusColor(status) }}>{status.toUpperCase()}</span></span>
                {execution.node_durations[nodeId] > 0 && (
                  <span className="node-duration">{execution.node_durations[nodeId].toFixed(2)}s</span>
                )}
              </div>
            ))}
          </div>
        )}

        {activeTab === 'logs' && (
          <div className="monitor-section">
            <h4>Execution Logs</h4>
            {Object.entries(execution.node_logs).map(([nodeId, logs]) => (
              <div key={nodeId} className="node-log-section">
                <h5>Node: {nodeId}</h5>
                <div className="logs-list">
                  {logs.map((log: string, index: number) => (
                    <p key={index} className="log-entry">{log}</p>
                  ))}
                </div>
              </div>
            ))}
            {execution.errors.length > 0 && (
              <div className="errors-list">
                <h4>Overall Errors</h4>
                {execution.errors.map((error: string, index: number) => (
                  <p key={index} style={{ color: 'var(--accent-error)' }}>{error}</p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ExecutionMonitor; 