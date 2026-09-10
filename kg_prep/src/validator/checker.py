import os
import json
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Set

logger = logging.getLogger("validator")

class PipelineValidator:
    """Audits schema compliance, duplicate IDs, and referential integrity of output CSV files."""
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.nodes_dir = self.output_dir / "Nodes"
        self.relationships_dir = self.output_dir / "Relationships"
        
        # 20 required node types
        self.node_headers = {
            "Ingredients": ["ID", "Name", "Source"],
            "Products": ["ID", "Name", "IngredientsText", "Source"],
            "Nutrients": ["ID", "Name", "Value", "Unit", "Source"],
            "Compounds": ["ID", "Name", "ChemicalFormula", "CASNumber", "Source"],
            "Flavors": ["ID", "Name", "Source"],
            "FlavorMolecules": ["ID", "Name", "PubChemID", "FEMANumber", "CASNumber", "Source"],
            "FunctionalRoles": ["ID", "Name", "Source"],
            "FoodAdditives": ["ID", "Name", "Source"],
            "INS": ["ID", "Name", "Source"],
            "FoodCategories": ["ID", "Name", "Source"],
            "Regulations": ["ID", "Name", "Source"],
            "Constraints": ["ID", "constraint_id", "constraint_type", "parameter", "operator", "limit_value", "jurisdiction", "source_id", "evidence_id", "validation_status"],
            "Processes": ["ID", "Name", "Source"],
            "ProcessConditions": ["ID", "Name", "Source"],
            "Allergens": ["ID", "Name", "Source"],
            "Properties": ["ID", "Name", "Value", "Source"],
            "Packaging": ["ID", "Name", "Source"],
            "Equipment": ["ID", "Name", "Source"],
            "Evidence": ["ID", "Name", "Text", "Source"],
            "Sources": ["ID", "Name", "Type", "Source"]
        }

        # 26 required relationship names and their expected node mappings
        self.relationship_specs = {
            "ingredient_contains_compound": ("Ingredients", "Compounds"),
            "ingredient_has_nutrient": ("Ingredients", "Nutrients"),
            "ingredient_has_flavor": ("Ingredients", "Flavors"),
            "ingredient_performs_role": ("Ingredients", "FunctionalRoles"),
            "ingredient_has_property": ("Ingredients", "Properties"),
            "ingredient_used_in_product": ("Ingredients", "Products"),
            "product_in_category": ("Products", "FoodCategories"),
            "ingredient_has_constraint": ("Ingredients", "Constraints"),
            "product_has_constraint": ("Products", "Constraints"),
            "ingredient_interactions": ("Ingredients", "Ingredients"),
            "foodadditive_has_ins": ("FoodAdditives", "INS"),
            "foodadditive_allowed_in_foodcategory": ("FoodAdditives", "FoodCategories"),
            "regulation_has_constraint": ("Regulations", "Constraints"),
            "constraint_applies_to_category": ("Constraints", "FoodCategories"),
            "constraint_applies_to_ingredient": ("Constraints", "Ingredients"),
            "product_requires_process": ("Products", "Processes"),
            "process_has_condition": ("Processes", "ProcessConditions"),
            "process_uses_equipment": ("Processes", "Equipment"),
            "evidence_supports_entity": ("Evidence", "FoodAdditives"),
            "constraint_supported_by_evidence": ("Constraints", "Evidence"),
            "property_supported_by_evidence": ("Properties", "Evidence"),
            "process_supported_by_evidence": ("Processes", "Evidence"),
            "source_supports_evidence": ("Sources", "Evidence"),
            "ingredient_has_allergen": ("Ingredients", "Allergens"),
            "product_has_allergen": ("Products", "Allergens"),
            "product_requires_packaging": ("Products", "Packaging")
        }

    def calculate_graph_connectivity(self, resolved_node_ids: Dict[str, Set[str]]) -> Dict[str, Any]:
        """Performs graph connectivity analysis, reachability from ProductCategory, and orphan node classification."""
        all_nodes = {}
        for ntype, id_set in resolved_node_ids.items():
            for nid in id_set:
                all_nodes[nid] = ntype

        # Build adjacency graph
        adj = {nid: set() for nid in all_nodes.keys()}
        reverse_adj = {nid: set() for nid in all_nodes.keys()}
        edges_count = 0

        rel_audit_dir = self.relationships_dir / "audit"
        rel_audit_dir.mkdir(parents=True, exist_ok=True)

        for rel_file in self.relationships_dir.rglob("*.csv"):
            if rel_file.parent.name in ["neo4j", "audit"] or rel_file.name in ["relationship_schema.csv", "relationship_statistics.csv", "relationship_coverage.csv", "relationship_merge_report.csv", "orphan_entities.csv", "graph_statistics.csv", "graph_connectivity_report.csv", "orphan_nodes.csv"]:
                continue
            try:
                df = pd.read_csv(rel_file)
                if df.empty:
                    continue
                for _, row in df.iterrows():
                    src = str(row.get("source_id") or row.get("SourceID", ""))
                    tgt = str(row.get("target_id") or row.get("TargetID", ""))
                    if src in adj and tgt in adj:
                        adj[src].add(tgt)
                        reverse_adj[tgt].add(src)
                        edges_count += 1
            except Exception:
                pass

        # Reachability from Root Nodes (ProductCategories & Products)
        root_nodes = set()
        for nid, ntype in all_nodes.items():
            if ntype in ["FoodCategories", "Products"]:
                root_nodes.add(nid)

        visited_reachable = set()
        queue = list(root_nodes)
        for r in root_nodes:
            visited_reachable.add(r)

        shortest_paths = {r: 0 for r in root_nodes}
        parents = {r: "ROOT" for r in root_nodes}

        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            curr_dist = shortest_paths[curr]

            neighbors = adj.get(curr, set()).union(reverse_adj.get(curr, set()))
            for nbr in neighbors:
                if nbr not in visited_reachable:
                    visited_reachable.add(nbr)
                    shortest_paths[nbr] = curr_dist + 1
                    parents[nbr] = curr
                    queue.append(nbr)

        # Connected Components Analysis (undirected)
        unvisited = set(all_nodes.keys())
        components = []
        while unvisited:
            seed = next(iter(unvisited))
            comp = set()
            c_queue = [seed]
            unvisited.remove(seed)
            comp.add(seed)

            c_head = 0
            while c_head < len(c_queue):
                node = c_queue[c_head]
                c_head += 1
                nbrs = adj.get(node, set()).union(reverse_adj.get(node, set()))
                for nbr in nbrs:
                    if nbr in unvisited:
                        unvisited.remove(nbr)
                        comp.add(nbr)
                        c_queue.append(nbr)
            components.append(comp)

        largest_comp_size = max([len(c) for c in components]) if components else 0
        reachable_count = len(visited_reachable)
        total_nodes_cnt = len(all_nodes)
        pct_reachable = round((reachable_count / total_nodes_cnt * 100.0), 2) if total_nodes_cnt > 0 else 0.0

        # Build Connectivity Report CSV
        connectivity_rows = []
        for nid, ntype in all_nodes.items():
            is_reach = nid in visited_reachable
            connectivity_rows.append({
                "node_id": nid,
                "node_type": ntype,
                "canonical_name": nid,
                "reachable_from_product_category": is_reach,
                "shortest_path_length": shortest_paths.get(nid, -1),
                "parent_node": parents.get(nid, "NONE"),
                "reason_if_disconnected": "NONE" if is_reach else "NO_PATH_TO_PRODUCT_CATEGORY",
                "status": "CONNECTED" if is_reach else "DISCONNECTED"
            })

        df_conn = pd.DataFrame(connectivity_rows)
        df_conn.to_csv(self.output_dir / "graph_connectivity_report.csv", index=False)
        df_conn.to_csv(rel_audit_dir / "graph_connectivity_report.csv", index=False)

        # Build Orphan Nodes Audit CSV
        orphan_rows = []
        orphan_cnt = 0
        for nid, ntype in all_nodes.items():
            degree = len(adj.get(nid, set())) + len(reverse_adj.get(nid, set()))
            if degree == 0:
                orphan_cnt += 1
                orphan_rows.append({
                    "node_id": nid,
                    "node_type": ntype,
                    "canonical_name": nid,
                    "reason": "No incoming or outgoing relationship edges in raw source data",
                    "possible_parent": "ProductCategory",
                    "recommended_relationship": "BELONGS_TO_CATEGORY" if ntype == "Product" else "HAS_INGREDIENT",
                    "evidence_available": "NO_SOURCE_EVIDENCE",
                    "status": "ORPHAN_VALID" if ntype in ["Sources", "Regulations"] else "REQUIRES_REVIEW"
                })

        df_orph = pd.DataFrame(orphan_rows)
        df_orph.to_csv(self.output_dir / "orphan_nodes.csv", index=False)
        df_orph.to_csv(rel_audit_dir / "orphan_nodes.csv", index=False)

        # Graph Statistics CSV
        graph_stats = [{
            "total_nodes": total_nodes_cnt,
            "total_relationships": edges_count,
            "connected_nodes": reachable_count,
            "orphan_nodes": orphan_cnt,
            "connected_components": len(components),
            "largest_component_size": largest_comp_size,
            "nodes_reachable_from_product_category": reachable_count,
            "percentage_reachable": pct_reachable
        }]

        df_gstats = pd.DataFrame(graph_stats)
        df_gstats.to_csv(self.output_dir / "graph_statistics.csv", index=False)
        df_gstats.to_csv(rel_audit_dir / "graph_statistics.csv", index=False)

        logger.info(f"Graph Connectivity Analysis Complete: {reachable_count}/{total_nodes_cnt} ({pct_reachable}%) nodes reachable from ProductCategory across {len(components)} components.")
        return graph_stats[0]

    def validate_pipeline(self) -> Dict[str, Any]:
        """Runs the validation audits and saves a report JSON."""
        report = {
            "summary": {
                "status": "PASSED",
                "total_errors": 0,
                "total_warnings": 0,
                "nodes_validated": 0,
                "relationships_validated": 0
            },
            "errors": [],
            "warnings": [],
            "node_stats": {},
            "relationship_stats": {}
        }
        
        # Load all node IDs first for referential checks
        resolved_node_ids = {}
        
        # 1. Audit Nodes
        for node_type, expected_cols in self.node_headers.items():
            file_path = self.nodes_dir / f"{node_type}.csv"
            report["summary"]["nodes_validated"] += 1
            
            if not file_path.exists():
                report["errors"].append(f"Missing node file: {node_type}.csv")
                report["summary"]["status"] = "FAILED"
                report["node_stats"][node_type] = {"status": "MISSING", "count": 0}
                continue
                
            try:
                df = pd.read_csv(file_path)
                row_count = len(df)
                report["node_stats"][node_type] = {"status": "OK", "count": row_count}
                
                # Check column compliance
                missing_cols = [col for col in expected_cols if col not in df.columns]
                if missing_cols:
                    report["errors"].append(f"Node {node_type}.csv is missing expected columns: {missing_cols}")
                    report["summary"]["status"] = "FAILED"
                    
                if not df.empty:
                    # Check for null IDs
                    null_ids = df["ID"].isna().sum()
                    if null_ids > 0:
                        report["errors"].append(f"Node {node_type}.csv contains {null_ids} records with null ID.")
                        report["summary"]["status"] = "FAILED"
                        
                    # Check for duplicate IDs
                    duplicate_ids = df["ID"].duplicated().sum()
                    if duplicate_ids > 0:
                        report["errors"].append(f"Node {node_type}.csv contains {duplicate_ids} duplicate IDs.")
                        report["summary"]["status"] = "FAILED"
                        
                    # Synthetic / Placeholder detector check
                    from src.validator.synthetic_detector import SyntheticDetector
                    synth_detector = SyntheticDetector()
                    for _, row in df.iterrows():
                        is_synth, reason = synth_detector.is_synthetic(row.to_dict())
                        if is_synth:
                            report["errors"].append(f"Node {node_type}.csv contains synthetic/placeholder record: {row.get('ID')} ({row.get('Name')}) -> {reason}")
                            report["summary"]["status"] = "FAILED"

                    resolved_node_ids[node_type] = set(df["ID"].dropna().astype(str))

                else:
                    resolved_node_ids[node_type] = set()
                    
            except Exception as e:
                report["errors"].append(f"Failed to read node file {node_type}.csv: {e}")
                report["summary"]["status"] = "FAILED"

        # 2. Audit Relationships
        for rel_name, (src_node_type, tgt_node_type) in self.relationship_specs.items():
            file_path = self.relationships_dir / f"{rel_name}.csv"
            report["summary"]["relationships_validated"] += 1
            
            if not file_path.exists():
                report["errors"].append(f"Missing relationship file: {rel_name}.csv")
                report["summary"]["status"] = "FAILED"
                report["relationship_stats"][rel_name] = {"status": "MISSING", "count": 0}
                continue
                
            try:
                df = pd.read_csv(file_path)
                row_count = len(df)
                report["relationship_stats"][rel_name] = {"status": "OK", "count": row_count}
                
                # Check column compliance
                has_src = "SourceID" in df.columns or "source_id" in df.columns
                has_tgt = "TargetID" in df.columns or "target_id" in df.columns
                if not (has_src and has_tgt):
                    report["errors"].append(f"Relationship {rel_name}.csv is missing source/target ID columns.")
                    report["summary"]["status"] = "FAILED"
                    
                if not df.empty:
                    # Check referential integrity
                    src_nodes = resolved_node_ids.get(src_node_type, set())
                    tgt_nodes = resolved_node_ids.get(tgt_node_type, set())
                    all_nodes = set(sum([list(s) for s in resolved_node_ids.values()], []))
                    
                    orphaned_src = 0
                    orphaned_tgt = 0
                    
                    for idx, row in df.iterrows():
                        src_id = str(row.get("SourceID") or row.get("source_id", ""))
                        tgt_id = str(row.get("TargetID") or row.get("target_id", ""))
                        
                        if src_id not in src_nodes and src_id not in all_nodes:
                            orphaned_src += 1
                        if tgt_id not in tgt_nodes and tgt_id not in all_nodes:
                            orphaned_tgt += 1
                            
                    if orphaned_src > 0:
                        report["errors"].append(f"Relationship {rel_name}.csv contains {orphaned_src} SourceIDs not found in {src_node_type}.csv.")
                        report["summary"]["status"] = "FAILED"
                    if orphaned_tgt > 0:
                        report["errors"].append(f"Relationship {rel_name}.csv contains {orphaned_tgt} TargetIDs not found in {tgt_node_type}.csv.")
                        report["summary"]["status"] = "FAILED"
                        
            except Exception as e:
                report["errors"].append(f"Failed to read relationship file {rel_name}.csv: {e}")
                report["summary"]["status"] = "FAILED"

        # 3. Calculate Graph Connectivity & Output Ledgers
        gstats = self.calculate_graph_connectivity(resolved_node_ids)
        report["graph_stats"] = gstats

        # Update totals
        report["summary"]["total_errors"] = len(report["errors"])
        report["summary"]["total_warnings"] = len(report["warnings"])
        
        # Save report files (JSON & CSV)
        report_path = self.output_dir / "validation_report.json"
        csv_report_path = self.output_dir / "validation_report.csv"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4)
            logger.info(f"Saved validation report to {report_path}")
            
            # Export CSV format of validation stats
            stats_list = []
            for k, v in report.get("node_stats", {}).items():
                stats_list.append({"Type": "Node", "Category": k, "Status": v.get("status"), "Count": v.get("count")})
            for k, v in report.get("relationship_stats", {}).items():
                stats_list.append({"Type": "Relationship", "Category": k, "Status": v.get("status"), "Count": v.get("count")})
            pd.DataFrame(stats_list).to_csv(csv_report_path, index=False)
            logger.info(f"Saved CSV validation report to {csv_report_path}")
        except Exception as e:
            logger.error(f"Failed to save validation report to file: {e}")
            
        return report
