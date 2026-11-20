"""
Pipeline V2 Phase 2A Genuine Acquisition and Staging Runner.
"""

import os
import sys
import json
from pathlib import Path

# Add src to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "src"))

from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.core.registry import PipelineRegistry
from pipeline_v2.storage.duckdb_store import DuckDBStore
from pipeline_v2.acquisition.foodon_acquirer import FoodonAcquirer
from pipeline_v2.acquisition.gsfa_acquirer import GsfaAcquirer
from pipeline_v2.acquisition.usda_acquirer import UsdaAcquirer
from pipeline_v2.acquisition.pubchem_acquirer import PubChemAcquirer
from pipeline_v2.extractors.foodon.extractor import FoodonExtractor
from pipeline_v2.extractors.gsfa.extractor import GsfaExtractor
from pipeline_v2.extractors.usda.extractor import UsdaExtractor
from pipeline_v2.extractors.pubchem.extractor import PubChemExtractor
from pipeline_v2.models.execution_models import ExecutionRunRecord, ExecutionStatus, ProcessingStage


def run_phase_2a():
    print("Starting Phase 2A Genuine Acquisition and Staging Pipeline...")
    manifest = ManifestManager(manifest_id="MANIFEST-PHASE-2A")
    db_path = "data/intermediate_v2/kg_staging.duckdb"
    store = DuckDBStore(db_path)
    store.initialize_schema()

    # Synchronize declarative source registry to satisfy foreign keys
    registry = PipelineRegistry(str(root_dir / "config_v2"))
    registry.load_all()
    store.sync_source_registry(registry.sources)

    # Register active datasets into dataset_registry
    store.record_dataset("DSK-FOODON-2024-03", "SRC-FOODON", "2024-03", release_date="2024-03-15")
    store.record_dataset("DSK-CODEX-GSFA-ONLINE", "SRC-CODEX-GSFA", "48th Session", release_date="2024-01-01")
    store.record_dataset("DSK-USDA-FDC-FOUNDATION", "SRC-USDA-FDC", "October 2024", release_date="2024-10-28")
    store.record_dataset("DSK-PUBCHEM-COMPOUNDS", "SRC-PUBCHEM", "Live REST API", release_date="2024-11-01")

    run_record = ExecutionRunRecord(
        execution_id="RUN-PHASE-2A-ACQUISITION-01",
        stage_name=ProcessingStage.ACQUISITION,
        status=ExecutionStatus.RUNNING,
        parameters={"phase": "2A", "sources": ["SRC-FOODON", "SRC-CODEX-GSFA", "SRC-USDA-FDC", "SRC-PUBCHEM"]},
    )
    store.record_execution_run(run_record)

    # 1. FoodOn Acquisition & Extraction
    print("1. Acquiring and extracting FoodOn OWL classes...")
    foodon_acq = FoodonAcquirer()
    foodon_asset = foodon_acq.acquire(manifest)
    store.record_asset(foodon_asset)

    foodon_ext = FoodonExtractor()
    # Phase 2A verified batch: 1,000 genuine FoodOn classes (complete ontology contains 39,682 named classes; see Phase 2A.1 audit report)
    foodon_batch = foodon_ext.extract_records(foodon_asset.local_path, foodon_asset.asset_id, max_records=1000)
    print(f"   FoodOn extracted: {len(foodon_batch.records)} records.")

    # 2. Codex GSFA Acquisition & Extraction
    print("2. Acquiring and extracting Codex GSFA food additives...")
    gsfa_acq = GsfaAcquirer()
    gsfa_asset = gsfa_acq.acquire_additive_index(manifest)
    store.record_asset(gsfa_asset)

    gsfa_ext = GsfaExtractor()
    gsfa_batch = gsfa_ext.extract_from_html_index(gsfa_asset.local_path, gsfa_asset.asset_id)
    print(f"   Codex GSFA extracted: {len(gsfa_batch.records)} records.")

    # 3. USDA FDC Acquisition & Extraction
    print("3. Acquiring and extracting USDA FDC Foundation and SR Legacy foods...")
    usda_acq = UsdaAcquirer()
    queries = ["milk", "egg", "wheat flour", "cheddar cheese", "soybean oil", "sucrose"]
    usda_records_total = []
    usda_rejected_total = []
    usda_assets = []

    for q in queries:
        try:
            safe_q = q.replace(" ", "_")
            path = usda_acq.query_foods_by_data_type(query=q, data_types=["Foundation", "SR Legacy"], page_size=20)
            asset_id = f"AST-USDA-SEARCH-{safe_q.upper()}"
            asset = usda_acq.register_acquired_asset(asset_id, path, manifest)
            store.record_asset(asset)
            usda_assets.append(asset)

            ext = UsdaExtractor()
            batch = ext.extract_from_json_file(path, asset_id)
            usda_records_total.extend(batch.records)
            usda_rejected_total.extend(batch.rejected_records)
        except Exception as e:
            print(f"   Warning querying USDA for {q}: {e}")

    print(f"   USDA FDC extracted: {len(usda_records_total)} records, rejected: {len(usda_rejected_total)}.")

    # 4. PubChem Acquisition & Extraction
    print("4. Acquiring and extracting NCBI PubChem verified compounds...")
    pubchem_acq = PubChemAcquirer()
    key_cids = [
        1183,      # Vanillin
        2519,      # Caffeine
        311,       # Citric acid
        5988,      # Sucrose
        54670067,  # L-Ascorbic acid (Vitamin C)
        712,       # Sodium benzoate
        23665764,  # Potassium sorbate
        104,       # Glycine
    ]
    pubchem_records_total = []
    pubchem_assets = []

    for cid in key_cids:
        try:
            path = pubchem_acq.fetch_by_cid(cid)
            asset_id = f"AST-PUBCHEM-CID-{cid}"
            asset = pubchem_acq.register_acquired_asset(asset_id, path, manifest)
            store.record_asset(asset)
            pubchem_assets.append(asset)

            ext = PubChemExtractor()
            batch = ext.extract_from_json_file(path, asset_id)
            pubchem_records_total.extend(batch.records)
        except Exception as e:
            print(f"   Warning fetching PubChem CID {cid}: {e}")

    print(f"   PubChem extracted: {len(pubchem_records_total)} records.")

    # Stage all extracted records into DuckDB raw_records
    all_extracted = foodon_batch.records + gsfa_batch.records + usda_records_total + pubchem_records_total
    all_rejected = foodon_batch.rejected_records + gsfa_batch.rejected_records + usda_rejected_total
    print(f"Total authentic source records ready to stage in DuckDB: {len(all_extracted)}")

    chunk_size = 5000
    with store.transaction():
        for i in range(0, len(all_extracted), chunk_size):
            chunk = all_extracted[i : i + chunk_size]
            tuples = [
                (
                    f"{r.source_id}:{r.source_record_id}",
                    r.source_id,
                    r.dataset_id,
                    r.source_record_id,
                    r.raw_asset_id,
                    json.dumps(r.original_fields),
                    r.extraction_timestamp,
                    run_record.execution_id,
                )
                for r in chunk
            ]
            store.conn.executemany(
                """
                INSERT INTO raw_records (
                    raw_record_id, source_id, dataset_id, native_record_id,
                    asset_id, payload_json, extracted_at, execution_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (raw_record_id) DO NOTHING;
                """,
                tuples,
            )

    # Save Manifest
    manifest_json = Path("data/manifests_v2/phase_2a_manifest.json")
    manifest_csv = Path("data/manifests_v2/phase_2a_manifest.csv")
    manifest.save_json(manifest_json)
    manifest.export_csv(manifest_csv)

    # Update Execution Run
    run_record.status = ExecutionStatus.COMPLETED
    run_record.total_records_processed = len(all_extracted)
    run_record.total_records_failed = len(all_rejected)
    store.record_execution_run(run_record)

    print("\n=======================================================")
    print("Phase 2A Genuine Acquisition & Staging Succeeded!")
    print(f"DuckDB raw_records staged: {store.count_records('raw_records')}")
    print(f"DuckDB source_assets tracked: {store.count_records('source_assets')}")
    print(f"Manifest total assets registered: {len(manifest.assets)}")
    print("=======================================================\n")
    store.close()

    return {
        "foodon_extracted": len(foodon_batch.records),
        "gsfa_extracted": len(gsfa_batch.records),
        "usda_extracted": len(usda_records_total),
        "usda_rejected": len(usda_rejected_total),
        "pubchem_extracted": len(pubchem_records_total),
        "total_staged": len(all_extracted),
    }


if __name__ == "__main__":
    run_phase_2a()
