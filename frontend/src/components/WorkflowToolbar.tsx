import React from 'react';

interface WorkflowToolbarProps {
  isExecuting: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onFitView: () => void;
}

const WorkflowToolbar: React.FC<WorkflowToolbarProps> = ({
  isExecuting,
  onStart,
  onPause,
  onReset,
  onZoomIn,
  onZoomOut,
  onFitView,
}) => {
  return (
    <div className="workflow-toolbar">
      <div className="toolbar-section">
        <h4>🎮 Execution Controls</h4>
        <div className="execution-buttons">
          <button
            className={`execution-btn start ${isExecuting ? 'disabled' : ''}`}
            onClick={onStart}
            disabled={isExecuting}
            title="Start Workflow Execution"
          >
            ▶️ Start
          </button>
          <button
            className={`execution-btn pause ${!isExecuting ? 'disabled' : ''}`}
            onClick={onPause}
            disabled={!isExecuting}
            title="Pause Execution"
          >
            ⏸️ Pause
          </button>
          <button
            className="execution-btn reset"
            onClick={onReset}
            title="Reset All Nodes"
          >
            🔄 Reset
          </button>
        </div>
      </div>

      <div className="toolbar-section">
        <h4>🔍 View Controls</h4>
        <div className="view-buttons">
          <button
            className="view-btn"
            onClick={onZoomIn}
            title="Zoom In"
          >
            🔍+
          </button>
          <button
            className="view-btn"
            onClick={onZoomOut}
            title="Zoom Out"
          >
            🔍-
          </button>
          <button
            className="view-btn"
            onClick={onFitView}
            title="Fit to View"
          >
            📐 Fit
          </button>
        </div>
      </div>

      <div className="toolbar-section">
        <h4>⚙️ Workflow Actions</h4>
        <div className="workflow-buttons">
          <button className="workflow-btn">
            💾 Save
          </button>
          <button className="workflow-btn">
            📋 Export
          </button>
          <button className="workflow-btn">
            🔧 Settings
          </button>
        </div>
      </div>

      <div className="toolbar-section">
        <h4>📊 Quick Stats</h4>
        <div className="stats">
          <div className="stat-item">
            <span className="stat-label">Nodes:</span>
            <span className="stat-value">6</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Status:</span>
            <span className={`stat-value ${isExecuting ? 'running' : 'idle'}`}>
              {isExecuting ? 'Running' : 'Idle'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkflowToolbar; 