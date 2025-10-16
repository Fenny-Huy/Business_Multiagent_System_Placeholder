import duckdb

DB_PATH = 'business_analytics.duckdb'

def explore_duckdb_table(table_name: str, limit: int = 2):
    """Connect to DuckDB, select rows from the given table, and print them."""
    import ast
    con = duckdb.connect(DB_PATH)
    try:
        query = f"SELECT attributes, hours FROM {table_name} WHERE business_id='eEOYSgkmpB90uNA7lDOMRA' LIMIT {limit}"
        result = con.execute(query).fetchdf()
        # Parse each attributes string to a Python object
        def parse_attr(val):
            if isinstance(val, str):
                try:
                    return ast.literal_eval(val)
                except Exception:
                    return val
            return val
        result['hours'] = result['hours'].apply(parse_attr)
        result['attributes'] = result['attributes'].apply(parse_attr)
        # result['Ambience'] = result['attributes'].apply(lambda x: parse_attr(x.get('Ambience')) if isinstance(x, dict) and 'Ambience' in x else None)
        print(result)
        print("\nAs JSON:")
        print(result.to_json(orient="records", indent=2))
    finally:
        con.close()

if __name__ == "__main__":
    # Example usage: list tables, then select from one
    con = duckdb.connect(DB_PATH)
    tables = con.execute("SHOW TABLES").fetchall()
    print("Tables in database:", tables)
    con.close()
    # Replace 'your_table_name' with an actual table name from above
    explore_duckdb_table('businesses')
