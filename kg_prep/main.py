import argparse
import sys
import asyncio
from pathlib import Path
from src.orchestrator import DataLakeOrchestrator, PrepPipelineOrchestrator

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Food Formulation Knowledge Graph & Grounded Data Validation Pipeline"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--pipeline",
        action="store_true",
        help="Execute full end-to-end Knowledge Acquisition, Normalization, Grounded DB, KG Prep, and Validation pipeline."
    )
    group.add_argument(
        "--reproducibility-test",
        action="store_true",
        help="Run reproducibility verification test across consecutive pipeline runs."
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Execute raw collection for all active raw data sources."
    )
    group.add_argument(
        "--source",
        type=str,
        help="Execute raw collection for a single source ID (e.g. 'usda_fdc', 'foodb', 'combase')."
    )
    group.add_argument(
        "--domain",
        type=str,
        help="Execute raw collection for a domain category (e.g. 'structured', 'semi_structured', 'unstructured')."
    )
    
    parser.add_argument(
        "--config-dir",
        type=str,
        default="config",
        help="Directory containing config.yaml (default: 'config')."
    )
    
    return parser.parse_args()

async def async_main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parent
    config_dir_path = project_root / args.config_dir

    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    try:
        if args.pipeline:

            print("\n>> Executing Complete End-to-End Food KG Pipeline...\n")
            # 1. Run raw acquisition first
            data_lake = DataLakeOrchestrator(config_dir=config_dir_path, project_root=project_root)
            await data_lake.run_all()

            # 2. Run prep, fusion, grounded DB, and validation
            prep_orchestrator = PrepPipelineOrchestrator(project_root=project_root)
            report = prep_orchestrator.run_end_to_end()
            
            if report.get("summary", {}).get("status") == "PASSED":
                print("\n[SUCCESS] End-to-End Food KG Pipeline Completed with Status: PASSED")
                return 0
            else:
                print("\n[FAILURE] Pipeline validation reported errors.")
                return 1

        elif args.reproducibility_test:
            print("\n>> Executing Pipeline Reproducibility Test...\n")
            prep_orchestrator = PrepPipelineOrchestrator(project_root=project_root)
            passed = prep_orchestrator.run_reproducibility_test()
            if passed:
                print("\n[SUCCESS] Pipeline Reproducibility Verification Passed!")
                return 0
            else:
                print("\n[FAILURE] Reproducibility Verification Failed.")
                return 1

        elif args.source:
            data_lake = DataLakeOrchestrator(config_dir=config_dir_path, project_root=project_root)
            print(f"\n>> Executing raw collection for source: '{args.source}'...\n")
            results = await data_lake.run_source(args.source)
            return 0
        elif args.domain:
            data_lake = DataLakeOrchestrator(config_dir=config_dir_path, project_root=project_root)
            print(f"\n>> Executing raw collection for domain: '{args.domain}'...\n")
            results = await data_lake.run_domain(args.domain)
            return 0
        else:
            data_lake = DataLakeOrchestrator(config_dir=config_dir_path, project_root=project_root)
            print("\n>> Executing complete Data Lake raw collection...\n")
            results = await data_lake.run_all()
            return 0
            
    except Exception as e:
        print(f"\n[ERROR] Pipeline execution crashed: {e}", file=sys.stderr)
        return 1

def main():
    exit_code = asyncio.run(async_main())
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
