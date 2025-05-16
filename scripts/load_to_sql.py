#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import os
import pathlib
import sqlite3
from typing import Any, Dict, List

import yaml

DB_PATH = "erp_demo.db"
SCHEMA_FILE = "data/schema.yaml"
DATA_DIR = pathlib.Path("data")
BATCH_SIZE = 1000  # 幾筆一批 executemany，可依機器記憶體調整


# ---------------------------------------------------------------------------
def create_tables_from_yaml(schema: Dict[str, Any], conn: sqlite3.Connection):
    cur = conn.cursor()
    for table, cfg in schema["tables"].items():
        cols_sql: List[str] = []
        pk_inline = []  # 多欄位 PK 需額外宣告
        for col, props in cfg["columns"].items():
            col_type = props.get("type", "TEXT")
            not_null = " NOT NULL" if props.get("not_null") else ""
            default = f" DEFAULT {props['default']}" if "default" in props else ""
            cols_sql.append(f'"{col}" {col_type}{not_null}{default}')
            if props.get("pk"):
                pk_inline.append(f'"{col}"')
        pk_clause = f", PRIMARY KEY({','.join(pk_inline)})" if pk_inline else ""
        ddl = (
            f'CREATE TABLE IF NOT EXISTS "{table}" ({", ".join(cols_sql)}{pk_clause});'
        )
        cur.execute(ddl)
        print(f"🛠️  {table} created.")
    conn.commit()


# ---------------------------------------------------------------------------
def load_jsonl(table: str, jsonl_path: pathlib.Path, conn: sqlite3.Connection):
    cur = conn.cursor()
    rows = []
    sql = None
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():  # 空白行略過
                continue
            obj = json.loads(line)
            if sql is None:
                # 第一次遇到此表 → 動態決定欄位與 SQL 模板
                columns = list(obj.keys())  # Original column names for data extraction
                quoted_columns_for_sql = [
                    f'"{col}"' for col in columns
                ]  # Quote column names for SQL
                placeholders = ",".join("?" * len(columns))
                sql = f'INSERT OR REPLACE INTO "{table}" ({",".join(quoted_columns_for_sql)}) VALUES ({placeholders})'
            rows.append(
                tuple(obj.get(col) for col in columns)
            )  # Use original column names for fetching values
            # 滿 batch 就寫一次
            if len(rows) >= BATCH_SIZE:
                cur.executemany(sql, rows)
                rows.clear()
    # 把剩餘不足 batch 的寫入
    if rows:
        cur.executemany(sql, rows)
    conn.commit()
    print(f"✅  {table}: {jsonl_path.name} loaded ({cur.rowcount} rows).")


# ---------------------------------------------------------------------------
def main():
    # Delete existing database file for a clean run
    if pathlib.Path(DB_PATH).exists():
        try:
            os.remove(DB_PATH)
            print(f"🧹 Deleted existing database: {DB_PATH}")
        except OSError as e:
            print(f"Error deleting database {DB_PATH}: {e}")
            # Optionally, decide if you want to exit if DB can't be deleted
            # return

    schema = yaml.safe_load(pathlib.Path(SCHEMA_FILE).read_text(encoding="utf-8"))
    conn = sqlite3.connect(DB_PATH)

    # 1) 建表
    create_tables_from_yaml(schema, conn)

    # 2) 依資料夾自動匯入
    # Create a mapping from a normalized (lowercase, no underscores) table name to schema-defined table name
    table_name_map = {
        name.lower().replace("_", ""): name for name in schema["tables"].keys()
    }

    for jsonl_file in DATA_DIR.glob("*.jsonl"):
        # Normalize the file stem (lowercase, no underscores)
        normalized_file_stem = jsonl_file.stem.lower().replace("_", "")
        actual_table_name = table_name_map.get(normalized_file_stem)

        if actual_table_name:
            load_jsonl(actual_table_name, jsonl_file, conn)
        else:
            print(
                f"⚠️  No table definition found in schema for {jsonl_file.name}. Skipping."
            )

    conn.close()
    print(f"🎉 All done → {DB_PATH}")


if __name__ == "__main__":
    main()
