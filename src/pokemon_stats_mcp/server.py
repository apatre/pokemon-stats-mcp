import logging
import pandas as pd
from mcp.server.fastmcp import FastMCP
from pokemon_stats_mcp.database import DuckDBAdapter
import os
import sys

# Dynamic path resolution to import pipeline package inside src
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

logger = logging.getLogger("pokemon_stats_mcp.server")

# Define FastMCP server
mcp = FastMCP("Pokemon Stats Companion")

DB_PATH = "data/pokemon_stats.duckdb"

# Centralized database adapter setup. Easily swappable!
db_adapter = DuckDBAdapter(db_path=DB_PATH)

@mcp.tool()
def sync_version_data(version_group_name: str) -> str:
    """Trigger the extract-load-transform pipeline for a specific PokéAPI version group.
    
    This downloads all entities associated with the version group (versions, pokedexes,
    species, pokemon varieties, evolution chains, regions, locations, location-areas)
    and populates the DuckDB staging tables, then runs dbt to transform them into the 
    clean relational database in the 'raw' schema.
    
    Example:
        sync_version_data("red-blue")
    """
    logger.info(f"Syncing version data for group: {version_group_name}")
    try:
        from pipeline.orchestrate import orchestrate
        # We limit locations and pokedexes to keep bootstrap/sync fast
        orchestrate(version_group_name=version_group_name, db_path=DB_PATH, limit=10)
        return f"Successfully synchronized and transformed all data for version group '{version_group_name}'!"
    except Exception as e:
        logger.error(f"Error syncing version data: {e}")
        return f"Sync failed: {str(e)}"

@mcp.tool()
def query_db(sql: str) -> str:
    """Execute a SQL query against the DuckDB database.
    
    You can query the raw transformed models in the 'raw' schema or the staging tables in the 'staging' schema.
    
    Example query:
        SELECT pokemon_id, pokemon_name, base_experience FROM raw.pokemon LIMIT 5
    """
    logger.info(f"Executing query: {sql}")
    try:
        db_adapter.connect()
        # Execute query directly
        df = db_adapter.execute_query(sql)
        
        if df.empty:
            return "Query returned 0 results."
            
        try:
            return df.to_markdown(index=False)
        except Exception:
            return df.to_string(index=False)
    except Exception as e:
        logger.error(f"Error running query: {e}")
        return f"Error executing query: {str(e)}"
    finally:
        db_adapter.close()
