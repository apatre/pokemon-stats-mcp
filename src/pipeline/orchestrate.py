import os
import sys
import logging
import subprocess
from typing import Any

# Ensure project and pipeline root directories are in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.pokemon_stats_mcp.database import DuckDBAdapter, DatabaseAdapter
from extract import extract_load

def setup_logging(log_file: str = "data/pipeline.log") -> None:
    # Ensure parent log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers = []
    
    # File handler writing clean formatted logs
    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    
    # Console stream handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)

# Initialize logging configuration
setup_logging()
logger = logging.getLogger("orchestration")

def transform() -> None:
    """Run dbt models to transform staging data into clean relational structures."""
    logger.info("Starting Transform step (running dbt)...")
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    dbt_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "transform/dbt"))
    dbt_executable = os.path.abspath(os.path.join(base_dir, ".venv/bin/dbt"))

    subprocess.run(
        [dbt_executable, "run", "--profiles-dir", "."],
        cwd=dbt_dir,
        check=True
    )
    logger.info("Transform step (dbt) completed successfully!")

def orchestrate(version_group_name: str = "red-blue", db_path: str = "data/pokemon_stats.duckdb", limit: int = 150, mode: str = "all") -> None:
    """Full orchestration pipeline with staggered execution support (extract-only, transform-only, or all)."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    absolute_db_path = os.path.join(base_dir, db_path)
    
    if mode not in ["all", "extract", "transform"]:
        raise ValueError(f"Invalid mode '{mode}'. Choose from: 'all', 'extract', 'transform'.")

    # 1. Run Extract-Load step
    if mode in ["all", "extract"]:
        db_adapter = DuckDBAdapter(db_path=absolute_db_path)
        try:
            db_adapter.connect()
            extract_load(version_group_name, db_adapter, limit)
        except Exception as e:
            logger.error(f"Extract-Load step failed: {e}")
            raise
        finally:
            db_adapter.close()

    # 2. Run Transform (dbt) step AFTER releasing the DuckDB connection file lock
    if mode in ["all", "transform"]:
        try:
            transform()
            logger.info("Orchestration transform step completed successfully!")
        except Exception as e:
            logger.error(f"Transform step failed: {e}")
            raise

    logger.info(f"Orchestration pipeline finished successfully for mode '{mode}'!")

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Orchestrate Pokemon Stats extraction & transformation.")
    parser.add_argument("version_group", nargs="?", default="firered-leafgreen", help="PokeAPI version group name to extract (default: firered-leafgreen)")
    parser.add_argument("--mode", choices=["all", "extract", "transform"], default="all", help="Pipeline execution mode (default: all)")
    parser.add_argument("--limit", type=int, default=150, help="Max items to fetch for list endpoints (default: 150)")
    parser.add_argument("--db-path", default="data/pokemon_stats.duckdb", help="Path to DuckDB database file (default: data/pokemon_stats.duckdb)")
    
    args = parser.parse_args()
    
    orchestrate(
        version_group_name=args.version_group,
        db_path=args.db_path,
        limit=args.limit,
        mode=args.mode
    )

if __name__ == "__main__":
    main()
