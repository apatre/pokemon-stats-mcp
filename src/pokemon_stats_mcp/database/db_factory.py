from pokemon_stats_mcp.database.db_base import DBModelBase

class DBModelFactory:
    def __init__(self, db_type: str):
        self.db_type = db_type

    def get_db_model(self, *args, **kwargs) -> DBModelBase:
        """Factory method to get the appropriate DBModel instance based on the db_type."""

        db_type = self.db_type.lower()
        if db_type == "duckdb":
            from pokemon_stats_mcp.database.db_duckdb import DBDuckDBModel
            return DBDuckDBModel(*args, **kwargs)
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")
