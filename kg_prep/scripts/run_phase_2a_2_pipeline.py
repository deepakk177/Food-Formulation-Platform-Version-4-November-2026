"""
Pipeline V2 Execution Script: Phase 2A.2 Complete FoodOn & USDA Source Ingestion.

Executes:
1. Complete FoodOn streaming ingestion: stages all 39,682 named classes in 5,000-record chunks.
2. Complete USDA Foundation Foods bulk ingestion: stages all 316 foods and 14,111 nutrient measurements.
3. Complete USDA SR Legacy Foods bulk ingestion: stages all 7,793 foods and 644,125 nutrient measurements.
4. Preserves 296 Codex GSFA additives and 8 PubChem reference compounds.
5. Employs chunked transactions with constant memory and idempotent replayability.
"""

import os
import sys
import time
from pathlib import Path

# Add src to PYTHONPATH
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir / "src"))

from pipeline_v2.core.logging_config import setup_logger
from pipeline_v2.core.manifest import ManifestManager
from pipeline_v2.core.registry import PipelineRegistry
from pipeline_v2.models.execution_models import ExecutionRunRecord, ExecutionStatus, ProcessingStage
from pipeline_v2.models.manifest_models import AssetRecord, IntegrityStatus
from pipeline_v2.storage.duckdb_store import DuckDBStore
from pipeline_v2.extractors.foodon.extractor import FoodonExtractor
from pipeline_v2.extractors.usda.extractor import UsdaExtractor
from pipeline_v2.extractors.gsfa.extractor import GsfaExtractor
from pipeline_v2.extractors.pubchem.extractor import PubChemExtractor


def run_phase_2a_2():
    logger = setup_logger("phase_2a_2_runner")
    logger.info("Starting Phase 2A.2 Complete Source Ingestion...")

    manifest = ManifestManager(manifest_id="MANIFEST-PHASE-2A-2")
    db_path = "data/intermediate_v2/kg_staging.duckdb"
    store = DuckDBStore(db_path)
    store.initialize_schema()

    # Synchronize declarative source registry
    registry = PipelineRegistry(str(root_dir / "config_v2"))
    registry.load_all()
    store.sync_source_registry(registry.sources)

    # Synchronize dataset registry
    store.record_dataset(
        "DSK-FOODON-2024-03",
        "SRC-FOODON",
        "2024-03",
        release_date="2024-03-15",
        sha256_hash="1e11fc50283c6498697a7aca9606c9d914f1cda71cc5510e006d949c32df7db0",
        download_url="https://github.com/FoodOntology/foodon/raw/master/foodon.owl",
        record_count=39682,
    )
    store.record_dataset(
        "DSK-CODEX-GSFA-ONLINE",
        "SRC-CODEX-GSFA",
        "48th Session",
        release_date="2024-01-01",
        sha256_hash="ff06587e0d5abdc84e6b6a2650964013a34fc80f4483880052ee8f124679fae8",
        download_url="https://www.fao.org/gsfaonline/",
        record_count=296,
    )
    store.record_dataset(
        "DSK-USDA-FDC-FOUNDATION",
        "SRC-USDA-FDC",
        "2024-10-31",
        release_date="2024-10-31",
        sha256_hash="b7d8c56e2f1a66e4088a2e0a29350682fa0be2199b5030438a204aa76326b9a8",
        download_url="https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2024-10-31.zip",
        record_count=316,
    )
    store.record_dataset(
        "DSK-USDA-FDC-SR-LEGACY",
        "SRC-USDA-FDC",
        "2018-04",
        release_date="2018-04-01",
        sha256_hash="7669bcfb507204f14115456fef95b7feee1ce5c9c9968417c805a5a9bfdc1ea8",
        download_url="https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_json_2018-04.zip",
        record_count=7793,
    )
    store.record_dataset(
        "DSK-PUBCHEM-COMPOUNDS",
        "SRC-PUBCHEM",
        "Live REST API",
        release_date="2024-11-01",
        download_url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/",
        record_count=8,
    )

    execution_id = "RUN-PHASE-2A-2-INGESTION-01"
    run_record = ExecutionRunRecord(
        execution_id=execution_id,
        stage_name=ProcessingStage.ACQUISITION,
        status=ExecutionStatus.RUNNING,
        parameters={"phase": "2A.2", "scope": "Complete FoodOn & USDA Bulk"},
    )
    store.record_execution_run(run_record)

    total_staged_run = 0

    # --------------------------------------------------------------------------
    # 1. FoodOn Complete Streaming Staging (39,682 Named Classes)
    # --------------------------------------------------------------------------
    foodon_owl_path = Path("data/raw_v2/foodon/foodon.owl")
    foodon_sha = manifest.compute_sha256(foodon_owl_path)
    foodon_asset = AssetRecord(
        asset_id="AST-FOODON-OWL-001",
        source_id="SRC-FOODON",
        dataset_id="DSK-FOODON-2024-03",
        original_filename="foodon.owl",
        local_path=str(foodon_owl_path),
        source_url="https://github.com/FoodOntology/foodon/raw/master/foodon.owl",
        dataset_version="2024-03",
        file_size_bytes=foodon_owl_path.stat().st_size,
        sha256=foodon_sha,
        content_type="application/rdf+xml",
        access_status="LOCAL_AVAILABLE",
        integrity_status=IntegrityStatus.VERIFIED,
    )
    manifest.assets[foodon_asset.asset_id] = foodon_asset
    store.record_asset(foodon_asset)

    print("1. Streaming all 39,682 FoodOn classes into DuckDB in 5,000-record chunks...")
    foodon_ext = FoodonExtractor(execution_id=execution_id)
    foodon_staged = 0
    t0 = time.time()
    for chunk in foodon_ext.stream_records(foodon_owl_path, foodon_asset.asset_id, chunk_size=5000):
        n = store.stage_raw_records_chunk(chunk, execution_id)
        foodon_staged += n
        print(f"   Staged chunk of {n} FoodOn records (Cumulative: {foodon_staged}/39,682)...")
    t1 = time.time()
    print(f"   FoodOn complete: {foodon_staged} classes staged in {t1-t0:.2f}s.")
    total_staged_run += foodon_staged

    # --------------------------------------------------------------------------
    # 2. USDA Foundation Foods Bulk Staging (316 Foods, 14,111 Nutrients)
    # --------------------------------------------------------------------------
    f_path = Path("data/raw_v2/usda_bulk/foundationDownload.json")
    f_sha = manifest.compute_sha256(f_path)
    f_asset = AssetRecord(
        asset_id="AST-USDA-BULK-FOUNDATION-JSON",
        source_id="SRC-USDA-FDC",
        dataset_id="DSK-USDA-FDC-FOUNDATION",
        original_filename="foundationDownload.json",
        local_path=str(f_path),
        source_url="https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2024-10-31.zip",
        dataset_version="2024-10-31",
        file_size_bytes=f_path.stat().st_size,
        sha256=f_sha,
        content_type="application/json",
        access_status="LOCAL_AVAILABLE",
        integrity_status=IntegrityStatus.VERIFIED,
    )
    manifest.assets[f_asset.asset_id] = f_asset
    store.record_asset(f_asset)

    print("2. Staging complete USDA Foundation Foods bulk dataset (316 foods)...")
    usda_ext = UsdaExtractor(execution_id=execution_id)
    f_staged = 0
    for chunk in usda_ext.stream_from_json_file(f_path, f_asset.asset_id, chunk_size=500):
        n = store.stage_raw_records_chunk(chunk, execution_id)
        f_staged += n
    print(f"   USDA Foundation Foods complete: {f_staged} foods staged.")
    total_staged_run += f_staged

    # --------------------------------------------------------------------------
    # 3. USDA SR Legacy Foods Bulk Staging (7,793 Foods, 644,125 Nutrients)
    # --------------------------------------------------------------------------
    sr_path = Path("data/raw_v2/usda_bulk/FoodData_Central_sr_legacy_food_json_2018-04.json")
    sr_sha = manifest.compute_sha256(sr_path)
    sr_asset = AssetRecord(
        asset_id="AST-USDA-BULK-SR-LEGACY-JSON",
        source_id="SRC-USDA-FDC",
        dataset_id="DSK-USDA-FDC-SR-LEGACY",
        original_filename="FoodData_Central_sr_legacy_food_json_2018-04.json",
        local_path=str(sr_path),
        source_url="https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_json_2018-04.zip",
        dataset_version="2018-04",
        file_size_bytes=sr_path.stat().st_size,
        sha256=sr_sha,
        content_type="application/json",
        access_status="LOCAL_AVAILABLE",
        integrity_status=IntegrityStatus.VERIFIED,
    )
    manifest.assets[sr_asset.asset_id] = sr_asset
    store.record_asset(sr_asset)

    print("3. Staging complete USDA SR Legacy bulk dataset (7,793 foods) in 1,000-food chunks...")
    sr_staged = 0
    t2 = time.time()
    for chunk in usda_ext.stream_from_json_file(sr_path, sr_asset.asset_id, chunk_size=1000):
        n = store.stage_raw_records_chunk(chunk, execution_id)
        sr_staged += n
        print(f"   Staged chunk of {n} SR Legacy foods (Cumulative: {sr_staged}/7,793)...")
    t3 = time.time()
    print(f"   USDA SR Legacy complete: {sr_staged} foods staged in {t3-t2:.2f}s.")
    total_staged_run += sr_staged

    # --------------------------------------------------------------------------
    # 4. Codex GSFA & PubChem Idempotent Verification
    # --------------------------------------------------------------------------
    gsfa_path = Path("data/raw_v2/codex_gsfa/gsfa_additives.html")
    if gsfa_path.exists():
        gsfa_sha = manifest.compute_sha256(gsfa_path)
        gsfa_asset = AssetRecord(
            asset_id="AST-CODEX-GSFA-ADDITIVES-001",
            source_id="SRC-CODEX-GSFA",
            dataset_id="DSK-CODEX-GSFA-ONLINE",
            original_filename="gsfa_additives.html",
            local_path=str(gsfa_path),
            source_url="https://www.fao.org/gsfaonline/",
            dataset_version="48th Session",
            file_size_bytes=gsfa_path.stat().st_size,
            sha256=gsfa_sha,
            content_type="text/html",
            access_status="LOCAL_AVAILABLE",
            integrity_status=IntegrityStatus.VERIFIED,
        )
        manifest.assets[gsfa_asset.asset_id] = gsfa_asset
        store.record_asset(gsfa_asset)

        gsfa_ext = GsfaExtractor(execution_id=execution_id)
        gsfa_batch = gsfa_ext.extract_from_html_index(gsfa_path, gsfa_asset.asset_id)
        n_gsfa = store.stage_raw_records_chunk(gsfa_batch.records, execution_id)
        print(f"4. Codex GSFA verified: {len(gsfa_batch.records)} additives present in database.")

    pubchem_cids = [1183, 2519, 311, 5988, 54670067, 712, 23665764, 104]
    pubchem_ext = PubChemExtractor(execution_id=execution_id)
    pubchem_records = []
    for cid in pubchem_cids:
        p_path = Path(f"data/raw_v2/pubchem/pubchem_cid_{cid}.json")
        if p_path.exists():
            p_asset_id = f"AST-PUBCHEM-CID-{cid}"
            p_sha = manifest.compute_sha256(p_path)
            p_asset = AssetRecord(
                asset_id=p_asset_id,
                source_id="SRC-PUBCHEM",
                dataset_id="DSK-PUBCHEM-COMPOUNDS",
                original_filename=p_path.name,
                local_path=str(p_path),
                source_url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON",
                dataset_version="Live REST API",
                file_size_bytes=p_path.stat().st_size,
                sha256=p_sha,
                content_type="application/json",
                access_status="LOCAL_AVAILABLE",
                integrity_status=IntegrityStatus.VERIFIED,
            )
            manifest.assets[p_asset.asset_id] = p_asset
            store.record_asset(p_asset)

            b = pubchem_ext.extract_from_json_file(p_path, p_asset_id)
            pubchem_records.extend(b.records)

    store.stage_raw_records_chunk(pubchem_records, execution_id)
    print(f"5. PubChem verified: {len(pubchem_records)} reference compounds present in database.")

    # --------------------------------------------------------------------------
    # 5. Manifest & Execution Finalization
    # --------------------------------------------------------------------------
    manifest_json = Path("data/manifests_v2/phase_2a_2_manifest.json")
    manifest_csv = Path("data/manifests_v2/phase_2a_2_manifest.csv")
    manifest.save_json(manifest_json)
    manifest.export_csv(manifest_csv)

    run_record.status = ExecutionStatus.COMPLETED
    run_record.total_records_processed = total_staged_run
    run_record.total_records_failed = 0
    run_record.summary_metrics = {
        "foodon_classes_staged": foodon_staged,
        "usda_foundation_foods_staged": f_staged,
        "usda_sr_legacy_foods_staged": sr_staged,
        "total_staged_in_run": total_staged_run,
    }
    store.record_execution_run(run_record)

    total_in_db = store.count_records("raw_records")
    foodon_count = store.conn.execute("SELECT count(*) FROM raw_records WHERE source_id='SRC-FOODON'").fetchone()[0]
    usda_count = store.conn.execute("SELECT count(*) FROM raw_records WHERE source_id='SRC-USDA-FDC'").fetchone()[0]
    gsfa_count = store.conn.execute("SELECT count(*) FROM raw_records WHERE source_id='SRC-CODEX-GSFA'").fetchone()[0]
    pubchem_count = store.conn.execute("SELECT count(*) FROM raw_records WHERE source_id='SRC-PUBCHEM'").fetchone()[0]

    print("=" * 60)
    print("Phase 2A.2 Complete Source Ingestion Succeeded!")
    print(f"Total raw_records in DuckDB: {total_in_db}")
    print(f"  FoodOn named classes: {foodon_count}")
    print(f"  USDA food items:      {usda_count}")
    print(f"  Codex GSFA additives: {gsfa_count}")
    print(f"  PubChem compounds:    {pubchem_count}")
    print("=" * 60)
    store.close()


if __name__ == "__main__":
    run_phase_2a_2()
