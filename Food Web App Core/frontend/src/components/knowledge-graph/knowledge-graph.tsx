'use client';

import React, { useState, useEffect } from 'react';
import { GraphResponse, GraphNode, GraphEdge } from '@/types/graph';
import GraphCanvas from './graph-canvas';
import GraphToolbar from './graph-toolbar';
import GraphFilters from './graph-filters';
import GraphStats from './graph-stats';
import GraphLegend from './graph-legend';
import GraphNodeDetails from './graph-node-details';
import { Loader2, RefreshCw, AlertCircle, CheckCircle, Database } from 'lucide-react';

interface KnowledgeGraphProps {
  initialIngredientId?: string;
  title?: string;
  subtitle?: string;
}

export default function KnowledgeGraph({
  initialIngredientId,
  title = 'Interactive Knowledge Graph Explorer',
  subtitle = 'Visually navigate grounded Neo4j food science relationships, ingredient properties, constraints, and process rules.',
}: KnowledgeGraphProps) {
  const [data, setData] = useState<GraphResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [healthStatus, setHealthStatus] = useState<any>(null);

  // Interaction State
  const [depth, setDepth] = useState(2);
  const [selectedFilter, setSelectedFilter] = useState('All');
  const [layoutName, setLayoutName] = useState('cose');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);

  // Fetch Health & Graph Data
  const fetchGraphData = async (ingId?: string, currentDepth: number = depth) => {
    setLoading(true);
    setError(null);
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      // Check health
      const hRes = await fetch(`${api_url}/api/knowledge-graph/health`);
      if (hRes.ok) {
        const hData = await hRes.json();
        setHealthStatus(hData);
      }

      // Fetch Subgraph
      let endpoint = `${api_url}/api/knowledge-graph`;
      if (ingId) {
        endpoint = `${api_url}/api/knowledge-graph/ingredient/${encodeURIComponent(ingId)}/subgraph?depth=${currentDepth}`;
      } else if (initialIngredientId) {
        endpoint = `${api_url}/api/knowledge-graph/ingredient/${encodeURIComponent(initialIngredientId)}/subgraph?depth=${currentDepth}`;
      }

      const res = await fetch(endpoint);
      if (!res.ok) throw new Error(`Knowledge Graph API returned status ${res.status}`);

      const graphData: GraphResponse = await res.json();
      setData(graphData);

      // Default select root node if present
      if (graphData.nodes.length > 0) {
        const root = graphData.nodes.find((n) => n.id === graphData.rootNode) || graphData.nodes[0];
        setSelectedNode(root);
      }
    } catch (err: any) {
      console.error('[KnowledgeGraph] Fetch error:', err);
      setError(err.message || 'Unable to load Knowledge Graph data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraphData(initialIngredientId, depth);
  }, [initialIngredientId, depth]);

  const handleSearchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchTerm.trim()) return;

    setLoading(true);
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${api_url}/api/knowledge-graph/search?q=${encodeURIComponent(searchTerm.trim())}`);
      if (res.ok) {
        const sRes = await res.json();
        if (sRes.results && sRes.results.length > 0) {
          const matchId = sRes.results[0].id;
          fetchGraphData(matchId, depth);
        } else {
          alert(`No Knowledge Graph nodes found matching "${searchTerm}".`);
        }
      }
    } catch (err) {
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExpandNode = (nodeId: string) => {
    const nextDepth = Math.min(3, depth + 1);
    setDepth(nextDepth);
    fetchGraphData(nodeId, nextDepth);
  };

  return (
    <div className="space-y-6 font-sans text-[#191C1E]">
      
      {/* Top Title & Diagnostic Connection Badge */}
      <div className="bg-white p-5 rounded-2xl border border-[#E5E9E6] shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-[#191C1E] font-heading flex items-center gap-2">
            <Database className="h-5 w-5 text-[#164E3D]" /> {title}
          </h2>
          <p className="text-xs text-[#5F6D67] font-bold mt-0.5">{subtitle}</p>
        </div>

        {healthStatus && (
          <div className="flex items-center gap-2 self-start md:self-auto font-mono text-xs">
            <span
              className={`px-3 py-1.5 rounded-full border flex items-center gap-1.5 font-bold ${
                healthStatus.connected
                  ? 'bg-[#ECF4F0] text-[#164E3D] border-[#D1E2D9]'
                  : 'bg-amber-50 text-amber-900 border-amber-300'
              }`}
            >
              <span className={`h-2 w-2 rounded-full ${healthStatus.connected ? 'bg-[#164E3D]' : 'bg-amber-600'}`} />
              {healthStatus.connected ? 'Neo4j Database Connected' : 'Grounded KG Index Mode'}
            </span>
          </div>
        )}
      </div>

      {/* Dynamic Statistics Bar */}
      {data && <GraphStats stats={data.stats} />}

      {/* Toolbar Controls (Search, Depth, Layout, Zoom, Fit, Reset) */}
      <GraphToolbar
        depth={depth}
        onDepthChange={(d) => setDepth(d)}
        searchTerm={searchTerm}
        onSearchChange={(q) => setSearchTerm(q)}
        onSearchSubmit={handleSearchSubmit}
        layoutName={layoutName}
        onLayoutChange={(l) => setLayoutName(l)}
        onReset={() => fetchGraphData(initialIngredientId, depth)}
      />

      {/* Node Type Category Filters */}
      <GraphFilters selectedFilter={selectedFilter} onFilterChange={(f) => setSelectedFilter(f)} />

      {/* Main Graph Visualization Workspace */}
      <div className="flex flex-col lg:flex-row items-start gap-6 min-h-[550px] relative">
        
        {/* Graph Canvas Container */}
        <div className="flex-1 w-full h-[550px] relative">
          {loading ? (
            <div className="w-full h-full bg-[#FAFAF8] rounded-2xl border border-[#E5E9E6] flex flex-col items-center justify-center space-y-3">
              <Loader2 className="h-8 w-8 text-[#164E3D] animate-spin" />
              <span className="text-xs font-mono font-bold text-[#5F6D67]">
                Retrieving Knowledge Graph neighborhood from Neo4j...
              </span>
            </div>
          ) : error ? (
            <div className="w-full h-full bg-red-50 rounded-2xl border border-red-200 flex flex-col items-center justify-center space-y-3 p-6 text-center">
              <AlertCircle className="h-8 w-8 text-red-600" />
              <div className="space-y-1">
                <h4 className="text-sm font-bold text-red-900">Knowledge Graph Error</h4>
                <p className="text-xs text-red-700 font-mono">{error}</p>
              </div>
              <button
                onClick={() => fetchGraphData(initialIngredientId, depth)}
                className="px-4 py-2 rounded-xl bg-red-600 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm"
              >
                <RefreshCw className="h-3.5 w-3.5" /> Retry Connection
              </button>
            </div>
          ) : data ? (
            <GraphCanvas
              nodes={data.nodes}
              edges={data.edges}
              rootNodeId={data.rootNode}
              selectedNodeId={selectedNode?.id}
              selectedTypeFilter={selectedFilter}
              layoutName={layoutName}
              onNodeSelect={(node) => {
                setSelectedNode(node);
                setSelectedEdge(null);
              }}
              onEdgeSelect={(edge) => {
                setSelectedEdge(edge);
                setSelectedNode(null);
              }}
            />
          ) : (
            <div className="w-full h-full bg-[#FAFAF8] rounded-2xl border border-[#E5E9E6] flex items-center justify-center text-xs font-mono text-[#5F6D67]">
              No Knowledge Graph relationships found.
            </div>
          )}
        </div>

        {/* Right Side Slide-over Details Panel */}
        <GraphNodeDetails
          selectedNode={selectedNode}
          selectedEdge={selectedEdge}
          onClose={() => {
            setSelectedNode(null);
            setSelectedEdge(null);
          }}
          onExpandNode={handleExpandNode}
        />

      </div>

      {/* Semantic Color Schema Legend */}
      <GraphLegend />

    </div>
  );
}
