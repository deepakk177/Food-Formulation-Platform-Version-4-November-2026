import os
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import logging

logger = logging.getLogger("core.visualizer")

def ensure_visualizations_dir(output_dir: Path) -> Path:
    viz_dir = output_dir / "visualizations"
    viz_dir.mkdir(parents=True, exist_ok=True)
    return viz_dir

def generate_classification_chart(counts: dict, output_dir: Path):
    """Generate bar chart showing the counts of datasets/files classified by domain."""
    viz_dir = ensure_visualizations_dir(output_dir)
    plt.figure(figsize=(8, 5))
    
    categories = list(counts.keys())
    values = list(counts.values())
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    plt.bar(categories, values, color=colors[:len(categories)], edgecolor='gray', width=0.6)
    plt.title("Dataset Domain Classification Count", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Data Domain", fontsize=11, fontweight='bold')
    plt.ylabel("Number of Files", fontsize=11, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_path = viz_dir / "dataset_classification.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved classification chart to {output_path}")

def generate_data_flow_diagram(output_dir: Path):
    """Generate Raw Data Flow Diagram using NetworkX."""
    viz_dir = ensure_visualizations_dir(output_dir)
    plt.figure(figsize=(10, 6))
    
    G = nx.DiGraph()
    G.add_edge("1. Raw Data Lake (data/raw/)", "2. Profilers (Module 2, 3, 4)")
    G.add_edge("2. Profilers (Module 2, 3, 4)", "3. Configuration Generator")
    G.add_edge("3. Configuration Generator", "4. Interface Configs (.yaml/.json)")
    G.add_edge("4. Interface Configs (.yaml/.json)", "5. Entity & Relation Builders")
    G.add_edge("5. Entity & Relation Builders", "6. Neo4j Graph Database")

    pos = {
        "1. Raw Data Lake (data/raw/)": (0, 4),
        "2. Profilers (Module 2, 3, 4)": (0, 3),
        "3. Configuration Generator": (0, 2),
        "4. Interface Configs (.yaml/.json)": (0, 1),
        "5. Entity & Relation Builders": (0, 0),
        "6. Neo4j Graph Database": (0, -1)
    }

    nx.draw_networkx_nodes(G, pos, node_size=3500, node_color='#add8e6', edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15, edge_color='gray', width=2)
    
    plt.title("Raw Data Flow & Configuration Interface Diagram", fontsize=12, fontweight='bold', pad=10)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = viz_dir / "raw_data_flow.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved data flow diagram to {output_path}")

def generate_knowledge_source_graph(output_dir: Path):
    """Generate Knowledge Source Graph displaying how raw files map to target domains."""
    viz_dir = ensure_visualizations_dir(output_dir)
    plt.figure(figsize=(12, 8))
    
    G = nx.Graph()
    
    # Sources
    sources = ["FooDB", "USDA FDC", "FlavorDB", "GSFA Online", "OpenFoodFacts", "Codex PDF", "FoodOn Ontology", "Research Papers/Patents"]
    # Target Domains
    domains = ["Ingredient Domain", "Nutritional Domain", "Chemical Domain", "Sensory Domain", "Regulatory Domain", "Processing Domain"]
    
    G.add_nodes_from(sources, bipartite=0)
    G.add_nodes_from(domains, bipartite=1)
    
    # Mappings
    mappings = [
        ("FooDB", "Ingredient Domain"), ("FooDB", "Chemical Domain"),
        ("USDA FDC", "Ingredient Domain"), ("USDA FDC", "Nutritional Domain"),
        ("FlavorDB", "Ingredient Domain"), ("FlavorDB", "Chemical Domain"), ("FlavorDB", "Sensory Domain"),
        ("GSFA Online", "Regulatory Domain"),
        ("OpenFoodFacts", "Ingredient Domain"), ("OpenFoodFacts", "Regulatory Domain"),
        ("Codex PDF", "Regulatory Domain"),
        ("FoodOn Ontology", "Ingredient Domain"), ("FoodOn Ontology", "Processing Domain"),
        ("Research Papers/Patents", "Processing Domain"), ("Research Papers/Patents", "Regulatory Domain")
    ]
    
    G.add_edges_from(mappings)
    
    pos = {}
    # Place sources on the left, domains on the right
    for i, s in enumerate(sources):
        pos[s] = (1, i * (len(domains) / len(sources)))
    for i, d in enumerate(domains):
        pos[d] = (2, i)
        
    nx.draw_networkx_nodes(G, pos, nodelist=sources, node_color='#ffcccb', node_size=1500, edgecolors='black')
    nx.draw_networkx_nodes(G, pos, nodelist=domains, node_color='#90ee90', node_size=2000, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='gray', style='dashed', width=1.5)
    
    plt.title("Knowledge Source to Semantic Domain Map", fontsize=14, fontweight='bold', pad=15)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = viz_dir / "knowledge_source_graph.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved knowledge source graph to {output_path}")

def generate_parser_flowchart(output_dir: Path):
    """Generate flowchart displaying parser recommendations based on file type."""
    viz_dir = ensure_visualizations_dir(output_dir)
    plt.figure(figsize=(10, 6))
    
    G = nx.DiGraph()
    G.add_edge("File Extensions / Magic Bytes", "CSV / TSV")
    G.add_edge("File Extensions / Magic Bytes", "JSON / JSONL")
    G.add_edge("File Extensions / Magic Bytes", "HTML / XML")
    G.add_edge("File Extensions / Magic Bytes", "PDF Documents")
    G.add_edge("File Extensions / Magic Bytes", "OWL Ontology")
    
    G.add_edge("CSV / TSV", "Pandas / Polars Parser")
    G.add_edge("JSON / JSONL", "orjson / json Parser")
    G.add_edge("HTML / XML", "BeautifulSoup / lxml Parser")
    G.add_edge("PDF Documents", "pdfplumber Parser")
    G.add_edge("OWL Ontology", "rdflib RDF Graph Parser")
    
    pos = {
        "File Extensions / Magic Bytes": (0, 4),
        "CSV / TSV": (-2, 2),
        "JSON / JSONL": (-1, 2),
        "HTML / XML": (0, 2),
        "PDF Documents": (1, 2),
        "OWL Ontology": (2, 2),
        "Pandas / Polars Parser": (-2, 0),
        "orjson / json Parser": (-1, 0),
        "BeautifulSoup / lxml Parser": (0, 0),
        "pdfplumber Parser": (1, 0),
        "rdflib RDF Graph Parser": (2, 0)
    }
    
    nx.draw_networkx_nodes(G, pos, node_size=1600, node_color='#e6e6fa', edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=12, edge_color='black')
    
    plt.title("Recommended Parser Decision Flowchart", fontsize=12, fontweight='bold', pad=10)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = viz_dir / "parser_flowchart.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved parser flowchart to {output_path}")

def generate_kg_contribution_diagram(output_dir: Path):
    """Generate Knowledge Graph Contribution Diagram showing nodes and edges to be built."""
    viz_dir = ensure_visualizations_dir(output_dir)
    plt.figure(figsize=(10, 8))
    
    G = nx.DiGraph()
    # Edges representing relationships in the schema
    edges = [
        ("Product", "Ingredient", "CONSTITUENT_OF"),
        ("Ingredient", "Compound", "HAS_PROPERTY"),
        ("Ingredient", "Nutrient", "HAS_NUTRIENT"),
        ("Ingredient", "SensoryProperty", "EXHIBITS_SENSORY"),
        ("FoodAdditive", "FoodCategory", "REGULATED_BY"),
        ("FoodAdditive", "INSNumber", "MAPS_TO"),
        ("Product", "Process", "REQUIRES_PROCESS"),
        ("Process", "Equipment", "USES_EQUIPMENT"),
        ("Ingredient", "Evidence", "SUPPORTED_BY"),
        ("Evidence", "Source", "SOURCE_OF")
    ]
    
    for u, v, r in edges:
        G.add_edge(u, v, label=r)
        
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_color='#b1f2ff', node_size=1800, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    # Draw edges with curvature
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=15, edge_color='darkblue', width=1.5)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='red')
    
    plt.title("Target Knowledge Graph Schema & Contribution Map", fontsize=12, fontweight='bold', pad=15)
    plt.axis('off')
    plt.tight_layout()
    
    output_path = viz_dir / "kg_contribution.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    logger.info(f"Saved KG contribution diagram to {output_path}")

def generate_all_visualizations(counts: dict, output_dir: Path):
    """Executes all 5 visualization generations."""
    try:
        generate_classification_chart(counts, output_dir)
        generate_data_flow_diagram(output_dir)
        generate_knowledge_source_graph(output_dir)
        generate_parser_flowchart(output_dir)
        generate_kg_contribution_diagram(output_dir)
        logger.info("All visualizations generated successfully.")
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}", exc_info=True)
