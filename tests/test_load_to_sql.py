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

import json
import pathlib
import sqlite3
import sys
import tempfile
import unittest

import yaml

# Add the script's parent directory to the Python path
# to allow importing load_to_sql
script_dir = pathlib.Path(__file__).resolve().parent.parent / "scripts"
sys.path.append(str(script_dir))

from load_to_sql import create_tables_from_yaml, load_jsonl


class TestLoadToSql(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database, schema, and data for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = pathlib.Path(self.temp_dir.name)

        self.db_path = self.temp_path / "test_erp.db"
        self.schema_file = self.temp_path / "test_schema.yaml"
        self.data_file = self.temp_path / "keyword_table.jsonl"

        # 1. Create a dummy schema with a keyword-like column name
        self.schema_content = {
            "tables": {
                "keyword_table": {
                    "columns": {
                        "id": {"type": "INTEGER", "pk": True},
                        "order": {"type": "TEXT"},  # "order" is an SQL keyword
                        "description": {"type": "TEXT"},
                    }
                }
            }
        }
        with open(self.schema_file, "w", encoding="utf-8") as f:
            yaml.dump(self.schema_content, f)

        # 2. Create dummy JSONL data
        self.jsonl_data = [
            {"id": 1, "order": "first_order", "description": "Item A"},
            {"id": 2, "order": "second_order", "description": "Item B"},
        ]
        with open(self.data_file, "w", encoding="utf-8") as f:
            for item in self.jsonl_data:
                f.write(json.dumps(item) + "\n")

        self.conn = sqlite3.connect(self.db_path)

    def tearDown(self):
        """Clean up temporary files and close the database connection."""
        self.conn.close()
        self.temp_dir.cleanup()
        # Remove script_dir from path if it was added
        script_dir_str = str(pathlib.Path(__file__).resolve().parent.parent / "scripts")
        if script_dir_str in sys.path:
            sys.path.remove(script_dir_str)

    def test_load_jsonl_with_keyword_column_name(self):
        """Test loading data into a table with an SQL keyword as a column name."""
        # 1. Create tables based on the schema
        create_tables_from_yaml(self.schema_content, self.conn)

        # 2. Load data using load_jsonl
        # The print statements in load_jsonl can be suppressed or redirected if noisy for tests
        # For now, we'll allow them.
        load_jsonl("keyword_table", self.data_file, self.conn)

        # 3. Verify data was loaded correctly
        cur = self.conn.cursor()
        cur.execute('SELECT id, "order", description FROM keyword_table ORDER BY id')
        rows = cur.fetchall()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], (1, "first_order", "Item A"))
        self.assertEqual(rows[1], (2, "second_order", "Item B"))

        # Test with a different keyword-like column name
        # (e.g., "group") to be more robust, if necessary.
        # For now, "order" should suffice to demonstrate the fix.


if __name__ == "__main__":
    unittest.main()
