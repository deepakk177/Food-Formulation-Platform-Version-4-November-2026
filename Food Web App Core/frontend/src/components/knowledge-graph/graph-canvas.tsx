'use client';

import React, { useEffect, useRef } from 'react';
import cytoscape, { Core, EventObject } from 'cytoscape';
import { GraphNode, GraphEdge, NodeType } from '@/types/graph';

interface GraphCanvasProps {
  nodes: GraphNode[];
  edges: GraphEdge[];
  rootNodeId?: string;
  selectedNodeId?: string | null;
  selectedEdgeId?: string | null;
  selectedTypeFilter?: string;
  onNodeSelect?: (node: GraphNode | null) => void;
  onEdgeSelect?: (edge: GraphEdge | null) => void;
  layoutName?: string;
}

export const NODE_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  Ingredient: { bg: '#164E3D', border: '#D1E2D9', text: '#FFFFFF' },
  Property: { bg: '#2563EB', border: '#93C5FD', text: '#FFFFFF' },
  Function: { bg: '#7C3AED', border: '#C4B5FD', text: '#FFFFFF' },
  Constraint: { bg: '#D97706', border: '#FDE68A', text: '#FFFFFF' },
  Process: { bg: '#475569', border: '#CBD5E1', text: '#FFFFFF' },
  Nutrient: { bg: '#0D9488', border: '#99F6E4', text: '#FFFFFF' },
  Allergen: { bg: '#DC2626', border: '#FCA5A5', text: '#FFFFFF' },
  Claim: { bg: '#EAB308', border: '#FEF08A', text: '#191C1E' },
};

export default function GraphCanvas({
  nodes,
  edges,
  rootNodeId,
  selectedNodeId,
  selectedTypeFilter = 'All',
  onNodeSelect,
  onEdgeSelect,
  layoutName = 'cose',
}: GraphCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);

  // Initialize and Update Cytoscape instance
  useEffect(() => {
    if (!containerRef.current) return;

    // Map graph data to Cytoscape elements
    const elements: cytoscape.ElementDefinition[] = [
      ...nodes.map((n) => {
        const isRoot = n.id === rootNodeId;
        const color = NODE_COLORS[n.type] || NODE_COLORS.Ingredient;
        return {
          data: {
            id: n.id,
            label: n.label,
            nodeType: n.type,
            bgColor: color.bg,
            borderColor: color.border,
            textColor: color.text,
            isRoot: isRoot ? 'true' : 'false',
            rawProperties: n.properties,
          },
        };
      }),
      ...edges.map((e) => ({
        data: {
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.type,
          rawProperties: e.properties,
        },
      })),
    ];

    const cy = cytoscape({
      container: containerRef.current,
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': 'data(bgColor)',
            'border-color': 'data(borderColor)',
            'border-width': 2,
            'label': 'data(label)',
            'color': '#191C1E',
            'font-family': 'Plus Jakarta Sans, sans-serif',
            'font-size': '11px',
            'font-weight': 'bold',
            'text-valign': 'bottom',
            'text-margin-y': 6,
            'text-background-color': '#FFFFFF',
            'text-background-opacity': 0.88,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'width': 34,
            'height': 34,
            'transition-property': 'background-color, border-color, width, height, opacity',
            'transition-duration': 0.2,
          },
        },
        {
          selector: 'node[isRoot = "true"]',
          style: {
            'width': 48,
            'height': 48,
            'border-width': 4,
            'border-color': '#164E3D',
            'font-size': '12px',
          },
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': '#CBD5E1',
            'target-arrow-color': '#CBD5E1',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 0.8,
            'curve-style': 'bezier',
            'opacity': 0.55,
          },
        },
        {
          selector: '.highlighted',
          style: {
            'border-width': 4,
            'border-color': '#164E3D',
            'opacity': 1,
            'z-index': 999,
          },
        },
        {
          selector: 'edge.highlighted',
          style: {
            'width': 3,
            'line-color': '#164E3D',
            'target-arrow-color': '#164E3D',
            'label': 'data(label)',
            'font-size': '10px',
            'font-family': 'IBM Plex Mono, monospace',
            'color': '#164E3D',
            'text-background-color': '#FFFFFF',
            'text-background-opacity': 0.95,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'opacity': 1,
            'z-index': 999,
          },
        },
        {
          selector: '.dimmed',
          style: {
            'opacity': 0.12,
          },
        },
      ],
      layout: {
        name: layoutName === 'concentric' ? 'concentric' : 'cose',
        animate: true,
        animationDuration: 600,
        padding: 60,
        nodeRepulsion: (node: any) => 800000,
        idealEdgeLength: (edge: any) => 150,
        edgeElasticity: (edge: any) => 100,
        nestingFactor: 1.2,
        gravity: 0.08,
        numIter: 1000,
        initialTemp: 1000,
        coolingFactor: 0.99,
        minTemp: 1.0,
      } as any,
      wheelSensitivity: 0.25,
    });

    // Event listeners
    cy.on('tap', 'node', (evt: EventObject) => {
      const nodeEl = evt.target;
      const nodeId = nodeEl.id();
      const nodeData = nodes.find((n) => n.id === nodeId) || null;

      // Dim non-connected elements
      cy.elements().removeClass('highlighted dimmed');
      const neighborhood = nodeEl.closedNeighborhood();
      cy.elements().difference(neighborhood).addClass('dimmed');
      neighborhood.addClass('highlighted');

      if (onNodeSelect) onNodeSelect(nodeData);
    });

    cy.on('tap', 'edge', (evt: EventObject) => {
      const edgeEl = evt.target;
      const edgeId = edgeEl.id();
      const edgeData = edges.find((e) => e.id === edgeId) || null;

      cy.elements().removeClass('highlighted dimmed');
      edgeEl.addClass('highlighted');
      edgeEl.connectedNodes().addClass('highlighted');
      cy.elements().difference(edgeEl.union(edgeEl.connectedNodes())).addClass('dimmed');

      if (onEdgeSelect) onEdgeSelect(edgeData);
    });

    cy.on('tap', (evt: EventObject) => {
      if (evt.target === cy) {
        cy.elements().removeClass('highlighted dimmed');
        if (onNodeSelect) onNodeSelect(null);
        if (onEdgeSelect) onEdgeSelect(null);
      }
    });

    // High-Contrast Dark Cursor state listeners
    cy.on('mouseover', 'node, edge', () => {
      containerRef.current?.classList.add('hovering-node');
    });

    cy.on('mouseout', 'node, edge', () => {
      containerRef.current?.classList.remove('hovering-node');
    });

    cy.on('grabon', () => {
      containerRef.current?.classList.add('grabbing');
    });

    cy.on('free', () => {
      containerRef.current?.classList.remove('grabbing');
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [nodes, edges, layoutName]);

  // Apply node type filter
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    if (!selectedTypeFilter || selectedTypeFilter === 'All') {
      cy.elements().removeClass('dimmed');
    } else {
      cy.batch(() => {
        cy.nodes().each((node) => {
          const nType = node.data('nodeType');
          if (nType === selectedTypeFilter || node.data('isRoot') === 'true') {
            node.removeClass('dimmed');
          } else {
            node.addClass('dimmed');
          }
        });
      });
    }
  }, [selectedTypeFilter]);

  // Highlight selected node from props
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy || !selectedNodeId) return;

    const targetEl = cy.getElementById(selectedNodeId);
    if (targetEl && targetEl.length > 0) {
      cy.elements().removeClass('highlighted dimmed');
      const neighborhood = targetEl.closedNeighborhood();
      cy.elements().difference(neighborhood).addClass('dimmed');
      neighborhood.addClass('highlighted');
      cy.animate({
        center: { eles: targetEl },
        zoom: 1.2,
        duration: 400,
      });
    }
  }, [selectedNodeId]);

  return (
    <div className="relative w-full h-full min-h-[500px] bg-[#FAFAF8] rounded-2xl border border-[#E5E9E6] overflow-hidden kg-canvas-container">
      <div ref={containerRef} className="w-full h-full absolute inset-0 kg-canvas-container" />
    </div>
  );
}
