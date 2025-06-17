export interface WorkflowNodeData {
  label: string;
  status: string;
  color: string;
  config: { [key: string]: any };
  logs?: string[];
  [key: string]: any;
}

export interface WorkflowNode {
    id: string;
    type: string;
    label: string;
    position: { x: number; y: number; };
    data: WorkflowNodeData;
}

export interface WorkflowEdge {
    id: string;
    source: string;
    target: string;
    sourceHandle?: string;
    targetHandle?: string;
}

export interface WorkflowExecutionStep {
    node_id: string;
    status: string;
    log: string;
    timestamp: string;
    duration: number;
}

export interface WorkflowExecution {
    execution_id: string;
    workflow_id: string;
    status: string;
    start_time: string;
    end_time?: string;
    node_status: { [key: string]: string };
    node_logs: { [key: string]: string[] };
    node_durations: { [key: string]: number };
    errors: string[];
    steps: WorkflowExecutionStep[];
} 