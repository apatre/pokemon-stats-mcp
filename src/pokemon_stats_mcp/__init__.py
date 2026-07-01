import logging
import os
from pokemon_stats_mcp.database import DuckDBAdapter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main() -> None:
    db_dir = "data"
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "pokemon_stats.duckdb")

    # Dynamic path resolution to import pipeline package inside src
    import sys
    base_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if base_dir_path not in sys.path:
        sys.path.insert(0, base_dir_path)

    # Swappable database adapter setup
    db_adapter = DuckDBAdapter(db_path=db_path)
    db_adapter.connect()

    try:
        # Check if version_group table already contains data
        has_data = False
        try:
            res = db_adapter.execute_query("SELECT COUNT(*) FROM staging.version_group")
            if not res.empty and res.iloc[0, 0] > 0:
                has_data = True
                logger.info(f"Staging tables already exist in '{db_path}' and contain data. Skipping PokéAPI bootstrap.")
        except Exception:
            pass

        if not has_data:
            logger.info(f"Bootstrap tables are empty or missing in '{db_path}'. Triggering extraction from PokéAPI...")
            
            # Close active connection to release file lock, since orchestrate will connect internally
            db_adapter.close()
            
            from pipeline.orchestrate import orchestrate
            orchestrate(version_group_name="red-blue", db_path=db_path, limit=10)
            
            db_adapter.connect()
            logger.info("Bootstrap data extraction completed successfully!")
            
    except Exception as e:
        logger.error(f"Error checking or loading bootstrap tables: {str(e)}")
        raise
    finally:
        try:
            db_adapter.close()
        except Exception:
            pass

    logger.info("Launching FastMCP server...")
    from pokemon_stats_mcp.server import mcp
    mcp.run()
