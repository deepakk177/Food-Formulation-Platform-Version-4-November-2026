'use client';

import React from 'react';
import KnowledgeGraph from '@/components/knowledge-graph/knowledge-graph';

export default function KnowledgeGraphExplorerPage() {
  return (
    <div className="max-w-7xl mx-auto py-4 space-y-6">
      <KnowledgeGraph
        title="Interactive Knowledge Graph Explorer"
        subtitle="Explore grounded Neo4j relationships across food ingredients, physical properties, functional roles, processing rules, constraints, nutrients, and safety claims."
      />
    </div>
  );
}
