# Copyright 2024 Jheng-Hong Yang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import Any, Dict, List

import yaml
from fastmcp import FastMCP
from sqlalchemy import create_engine, inspect, text


def get_db_config() -> str:
    """Returns the database connection string."""
    # In a real application, you might get this from environment variables,
    # a config file, or a secrets manager.
    script_dir = Path(__file__).parent
    db_path = script_dir / "data" / "erp_demo.db"
    return f"sqlite:///{db_path}"


DATABASE_URL = get_db_config()
engine = create_engine(DATABASE_URL)

mcp = FastMCP(name="sql-mcp-server")


# @mcp.tool()
# def configure_database_connection(
#     client_username: str, client_password: str, database_name: str = None
# ) -> Dict[str, str]:
#     """
#     Configures the database connection for the application, targeting a specific SQLite database.
#     Client username and password are not used for SQLite connection strings but are accepted for API consistency.
#     The server is assumed to be 'localhost' for local SQLite files.

#     Args:
#         client_username: The username provided by the client.
#         client_password: The password provided by the client.
#         database_name: The path to the SQLite database file (e.g., 'data/erp_demo.db').
#                        Defaults to script_dir/data/erp_demo.db.

#     Returns:
#         A dictionary with a status message indicating success or failure.
#     """
#     global engine, DATABASE_URL  # Declare intent to modify global variables

#     # Server-side context
#     server_host = "localhost"  # Implicit for local SQLite files

#     if database_name is None:
#         script_dir = Path(__file__).parent
#         db_path = script_dir / "data" / "erp_demo.db"
#         database_name = str(db_path)

#     print(
#         f"Received request to configure database with client user: {str(client_username)}, target DB: {database_name}"
#     )

#     try:
#         new_db_url = f"sqlite:///./{database_name.strip()}"
#         print(f"Attempting to set database connection to: {new_db_url}")

#         # Update global DATABASE_URL and re-initialize engine
#         DATABASE_URL = new_db_url
#         engine = create_engine(DATABASE_URL)

#         # Test the new connection
#         with engine.connect() as connection:
#             connection.execute(
#                 text("SELECT 1")
#             )  # A simple query to verify connectivity

#         success_message = (
#             f"Database connection successfully configured to '{database_name}' on server '{server_host}'. "
#             f"Client user: '{str(client_username)}'. Active DATABASE_URL: {DATABASE_URL}"
#         )
#         print(success_message)
#         return {"status": "success", "message": success_message}
#     except Exception as e:
#         error_message = (
#             f"Failed to configure database connection to '{database_name}': {str(e)}"
#         )
#         print(error_message)
#         # Optionally, consider reverting to a known good default configuration or exiting
#         return {"status": "error", "message": error_message}


@mcp.tool()
def list_tables() -> List[Dict[str, Any]]:
    """
    List all user-defined tables in the database, including their schema and, if available,
    a description. Uses SQLAlchemy Inspector for database-agnostic metadata.
    Args:
        None
    Returns:
        A list of dictionaries, where each dictionary contains 'schema_name',
        'table_name', and its 'description'. If an error occurs, returns a list
        containing a single dictionary with an 'error' key.
    """
    try:
        with open("data/schema.yaml", "r") as f:
            schema_data = yaml.safe_load(f)
        yaml_tables = schema_data.get("tables", {})
    except Exception as e:
        # If schema.yaml is not found or is invalid, proceed without it
        # but log the error or notify. For simplicity here, we'll just initialize to empty.
        print(f"Could not load or parse data/schema.yaml: {e}")
        yaml_tables = {}

    try:
        inspector = inspect(engine)
        tables_info = []

        # Get all schema names. For SQLite, this will usually just be ['main'].
        # For PostgreSQL, it can include 'public' and user-defined schemas.
        schemas = inspector.get_schema_names()

        for schema in schemas:
            # Exclude common system schemas. This list can be expanded if needed.
            if engine.name == "postgresql" and schema in (
                "pg_catalog",
                "information_schema",
                "pg_toast",
                "pg_temp_1",
                "pg_toast_temp_1",
            ):
                continue
            if (
                engine.name == "sqlite" and schema != "main"
            ):  # For SQLite, only process 'main' for user tables
                continue

            for table_name in inspector.get_table_names(schema=schema):
                description = "No description available"
                if (
                    engine.name == "postgresql"
                ):  # Table comments are more reliably supported in PostgreSQL
                    try:
                        # Attempt to get table comment for PostgreSQL
                        # This requires the table to have an OID, which is typical.
                        comment_query = text(
                            "SELECT obj_description(oid, 'pg_class') FROM pg_class WHERE relname = :table AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = :schema)"
                        )
                        with engine.connect() as conn:
                            result = conn.execute(
                                comment_query, {"table": table_name, "schema": schema}
                            ).scalar_one_or_none()
                        if result:
                            description = result
                    except Exception:
                        # If getting comment fails, stick to the default
                        pass  # Keep "No description available"
                elif engine.name == "sqlite":
                    if table_name in yaml_tables:
                        # If schema.yaml has a description field for the table, use it.
                        # For now, assuming 'description' key might exist directly under the table name.
                        # If schema.yaml structure is different, this lookup needs adjustment.
                        description = yaml_tables[table_name].get(
                            "description",
                            "Defined in schema.yaml; description pending.",
                        )
                    else:
                        description = "No description available (not in schema.yaml)"

                tables_info.append(
                    {
                        "schema_name": schema,
                        "table_name": table_name,
                        "description": description,
                    }
                )
        return tables_info

    except Exception as e:
        return [{"error": f"An error occurred while listing tables: {str(e)}"}]


@mcp.tool()
def execute_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a SQL SELECT query and return the results.
    For security reasons, only SELECT queries are permitted.
    The tool also includes internal checks to disallow common SQL comment markers (-- and /*).

    IMPORTANT SECURITY CONSIDERATIONS:
    - This tool only executes SELECT statements. Other types of queries will be rejected.
    - Queries containing SQL comment markers ('--', '/*') will be rejected as a
      precautionary measure against potential SQL injection techniques.
    - While these internal checks provide an additional layer of safety, if the provided
      SELECT query string is constructed dynamically (e.g., incorporating user input),
      the calling agent/client MUST STILL use parameterized queries (prepared statements)
      during the construction of that query string. This is the most robust defense
      against SQL injection vulnerabilities.
    - This tool executes the provided query string after these checks. The responsibility
      for ensuring the internal components of the SELECT query are safe beyond these specific
      checks (e.g., properly escaped or parameterized if built dynamically) lies with the caller.

    Args:
        query: The SQL SELECT query to execute.
    Returns:
        List of dictionaries containing the query results, or an error message
        if the query is not a SELECT statement, contains disallowed characters,
        or if execution fails.
    """
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return [
            {
                "error": "For security reasons, only SELECT queries are allowed. Ensure your query is a SELECT statement."
            }
        ]

    # Internal check for common SQL comment markers
    if "--" in query or "/*" in query:
        return [
            {
                "error": "For security reasons, queries containing SQL comment markers (--, /*) are not allowed."
            }
        ]

    with engine.connect() as connection:
        try:
            # Execute the query and get a Result object
            # SQLAlchemy's text() construct itself encourages parameterization if used correctly by the caller
            # when building the query string. For example, text("SELECT * FROM users WHERE id = :user_id")
            result_set = connection.execute(text(query))

            # Process query results
            results = [
                {
                    key: (value.isoformat() if hasattr(value, "isoformat") else value)
                    for key, value in row_mapping.items()
                }
                for row_mapping in result_set.mappings()
            ]
            return results
        except Exception as e:
            return [{"error": f"An error occurred while executing the query: {str(e)}"}]


@mcp.tool()
def search_customers(search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for customers.

    Args:
        search_term: The keyword to search for (searches in Name, Email, and Phone).
        limit: The maximum number of results to return (default is 10).

    Returns:
        A list of customer information.
    """
    inspector = inspect(engine)
    customer_table_name_actual = None

    try:
        # Find the 'Customers' table, being mindful of schema and case
        for schema_name in inspector.get_schema_names():
            # Skip system schemas based on database type
            if engine.name == "postgresql" and schema_name in (
                "pg_catalog",
                "information_schema",
                "pg_toast",
                "pg_temp_1",
                "pg_toast_temp_1",
            ):
                continue
            if engine.name == "sqlite" and schema_name != "main":
                continue

            for table_name in inspector.get_table_names(schema=schema_name):
                if table_name.lower() == "customers":
                    customer_table_name_actual = (
                        table_name  # Use the actual casing from DB
                    )
                    break
            if customer_table_name_actual:
                break

        if not customer_table_name_actual:
            return [{"error": "Table 'Customers' not found in the database."}]

        query_string = f"""
            SELECT CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax
            FROM {customer_table_name_actual}
            WHERE CompanyName LIKE :search_pattern OR
                  ContactName LIKE :search_pattern OR
                  Phone LIKE :search_pattern
            ORDER BY CompanyName
            LIMIT :limit
        """
        query = text(query_string)
        search_pattern = f"%{search_term}%"

        with engine.connect() as connection:
            result_set = connection.execute(
                query, {"search_pattern": search_pattern, "limit": limit}
            )
            results = [
                {
                    key: (value.isoformat() if hasattr(value, "isoformat") else value)
                    for key, value in row_mapping.items()
                }
                for row_mapping in result_set.mappings()
            ]
            if not results:
                return [{"message": "No customers found matching your search term."}]
            return results
    except Exception as e:
        # This will catch errors from inspection or query execution
        return [{"error": f"Error searching customers: {str(e)}"}]


@mcp.tool()
def get_customer_info(customer_id: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific customer.

    Args:
        customer_id: The ID of the customer.

    Returns:
        A dictionary containing customer information.
    """
    inspector = inspect(engine)
    customer_table_name_actual = None

    try:
        # Find the 'Customers' table, being mindful of schema and case
        for schema_name in inspector.get_schema_names():
            # Skip system schemas based on database type
            if engine.name == "postgresql" and schema_name in (
                "pg_catalog",
                "information_schema",
                "pg_toast",
                "pg_temp_1",
                "pg_toast_temp_1",
            ):
                continue
            if engine.name == "sqlite" and schema_name != "main":
                continue

            for table_name in inspector.get_table_names(schema=schema_name):
                if table_name.lower() == "customers":
                    customer_table_name_actual = (
                        table_name  # Use the actual casing from DB
                    )
                    break
            if customer_table_name_actual:
                break

        if not customer_table_name_actual:
            return {"error": "Table 'Customers' not found in the database."}

        query_string = f"SELECT * FROM {customer_table_name_actual} WHERE CustomerID = :customer_id"
        query = text(query_string)

        with engine.connect() as connection:
            result_set = connection.execute(query, {"customer_id": customer_id})
            row_mapping = result_set.mappings().fetchone()

            if not row_mapping:
                return {"error": f"No customer found with ID: {customer_id}"}

            # Process the row into a dictionary, handling data types
            result = {
                key: (value.isoformat() if hasattr(value, "isoformat") else value)
                for key, value in row_mapping.items()
            }
            return result
    except Exception as e:
        return {"error": f"Error retrieving customer info: {str(e)}"}


if __name__ == "__main__":
    mcp.run()
