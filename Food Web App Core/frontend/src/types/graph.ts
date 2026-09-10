export type NodeType =
  | 'Ingredient'
  | 'Property'
  | 'Function'
  | 'Constraint'
  | 'Process'
  | 'Nutrient'
  | 'Allergen'
  | 'Claim';

export interface GraphNode {
  id: string;
  label: string;
  type: NodeType | string;
  properties?: Record<string, any>;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  properties?: Record<string, any>;
}

export interface GraphStats {
  totalNodes: number;
  properties: number;
  functions: number;
  constraints: number;
  processes: number;
  allergens: number;
  nutrients?: number;
  claims?: number;
}

export interface GraphResponse {
  rootNode?: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: GraphStats;
}
