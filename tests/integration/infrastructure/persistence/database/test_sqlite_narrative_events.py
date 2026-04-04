"""测试 entity_base 和 narrative_events 表的存在性与结构（事件溯源架构）。"""
import sqlite3
from pathlib import Path

import pytest

SCHEMA_PATH = (
    Path(__file__).resolve().parents[5] / "infrastructure" / "persistence" / "database" / "schema.sql"
)


@pytest.fixture
def db_conn(tmp_path):
    """创建临时数据库并应用 schema。"""
    db_path = tmp_path / "test_narrative.db"
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    yield conn
    conn.close()


def test_entity_base_table_exists(db_conn):
    """验证 entity_base 表存在且结构正确。"""
    cursor = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='entity_base'"
    )
    assert cursor.fetchone() is not None, "entity_base 表不存在"

    # 验证列结构
    cursor = db_conn.execute("PRAGMA table_info(entity_base)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "id" in columns
    assert "novel_id" in columns
    assert "entity_type" in columns
    assert "name" in columns
    assert "core_attributes" in columns
    assert "created_at" in columns


def test_narrative_events_table_exists(db_conn):
    """验证 narrative_events 表存在且结构正确。"""
    cursor = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='narrative_events'"
    )
    assert cursor.fetchone() is not None, "narrative_events 表不存在"

    # 验证列结构
    cursor = db_conn.execute("PRAGMA table_info(narrative_events)")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    assert "event_id" in columns
    assert "novel_id" in columns
    assert "chapter_number" in columns
    assert "event_summary" in columns
    assert "mutations" in columns
    assert "timestamp_ts" in columns


def test_entity_base_indexes_exist(db_conn):
    """验证 entity_base 索引存在。"""
    cursor = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='entity_base'"
    )
    indexes = [row[0] for row in cursor.fetchall()]
    assert "idx_entity_base_novel" in indexes


def test_narrative_events_indexes_exist(db_conn):
    """验证 narrative_events 索引存在。"""
    cursor = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='narrative_events'"
    )
    indexes = [row[0] for row in cursor.fetchall()]
    assert "idx_narrative_events_novel_chapter" in indexes


def test_entity_base_foreign_key_constraint(db_conn):
    """验证 entity_base 外键约束到 novels 表。"""
    cursor = db_conn.execute("PRAGMA foreign_key_list(entity_base)")
    fks = cursor.fetchall()
    assert len(fks) > 0
    assert any(fk[2] == "novels" for fk in fks)


def test_narrative_events_foreign_key_constraint(db_conn):
    """验证 narrative_events 外键约束到 novels 表。"""
    cursor = db_conn.execute("PRAGMA foreign_key_list(narrative_events)")
    fks = cursor.fetchall()
    assert len(fks) > 0
    assert any(fk[2] == "novels" for fk in fks)
