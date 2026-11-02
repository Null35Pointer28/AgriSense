"""
AgriSense - SQLite Database Layer
Handles persistent storage for:
- Farming logs and field observations
- Soil health test records
- Crop recommendation history
- User location and preferences
Uses safe parameterized queries and proper connection lifecycles.
"""

import os
import sqlite3
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "agrisense.db")

_initialized = False

def get_connection():
    global _initialized
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if not _initialized:
        init_db(conn)
        _initialized = True
    return conn

def init_db(conn=None):
    """Initializes tables if they do not already exist."""
    def _create(c):
        cursor = c.cursor()
        
        # Farming / Soil / Recommendation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS farming_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                field_name TEXT NOT NULL,
                crop_recommended TEXT NOT NULL,
                confidence REAL,
                nitrogen REAL NOT NULL,
                phosphorus REAL NOT NULL,
                potassium REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                ph REAL NOT NULL,
                rainfall REAL NOT NULL,
                location_name TEXT,
                latitude REAL,
                longitude REAL,
                selected_crop TEXT,
                notes TEXT
            );
        """)

        # User preferences & last known location
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        c.commit()

    if conn is not None:
        _create(conn)
    else:
        with sqlite3.connect(DB_PATH) as c:
            _create(c)

def save_recommendation_history(data):
    """
    Saves a crop recommendation or soil test record to the database.
    """
    query = """
        INSERT INTO farming_history (
            field_name, crop_recommended, confidence,
            nitrogen, phosphorus, potassium,
            temperature, humidity, ph, rainfall,
            location_name, latitude, longitude,
            selected_crop, notes, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    timestamp = data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    field_name = data.get("field_name") or "Main Field"
    crop_recommended = data.get("crop_recommended") or "Unknown"
    confidence = float(data.get("confidence") or 0.0)
    nitrogen = float(data.get("nitrogen") or 0.0)
    phosphorus = float(data.get("phosphorus") or 0.0)
    potassium = float(data.get("potassium") or 0.0)
    temperature = float(data.get("temperature") or 0.0)
    humidity = float(data.get("humidity") or 0.0)
    ph = float(data.get("ph") or 0.0)
    rainfall = float(data.get("rainfall") or 0.0)
    location_name = data.get("location_name") or "Local Farm"
    latitude = float(data.get("latitude")) if data.get("latitude") is not None else None
    longitude = float(data.get("longitude")) if data.get("longitude") is not None else None
    selected_crop = data.get("selected_crop") or crop_recommended
    notes = data.get("notes") or ""

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            field_name, crop_recommended, confidence,
            nitrogen, phosphorus, potassium,
            temperature, humidity, ph, rainfall,
            location_name, latitude, longitude,
            selected_crop, notes, timestamp
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_history(limit=50):
    """Retrieves previous farming history records ordered by date descending."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farming_history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_history_by_id(record_id):
    """Retrieves a single farming history record."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM farming_history WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def delete_history_record(record_id):
    """Deletes a history record by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM farming_history WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_history_summary():
    """Calculates summary statistics from historical records."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_records FROM farming_history")
        total = cursor.fetchone()["total_records"]

        cursor.execute("""
            SELECT crop_recommended, COUNT(*) as count 
            FROM farming_history 
            GROUP BY crop_recommended 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_crops = [dict(r) for r in cursor.fetchall()]

        cursor.execute("""
            SELECT AVG(nitrogen) as avg_n, AVG(phosphorus) as avg_p, AVG(potassium) as avg_k, AVG(ph) as avg_ph
            FROM farming_history
        """)
        averages = dict(cursor.fetchone())

        return {
            "total_records": total,
            "top_crops": top_crops,
            "averages": {
                "n": round(averages["avg_n"] or 0, 1),
                "p": round(averages["avg_p"] or 0, 1),
                "k": round(averages["avg_k"] or 0, 1),
                "ph": round(averages["avg_ph"] or 0, 2)
            }
        }

def set_preference(key, value):
    """Saves or updates a key-value user preference."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_preferences (key, value, updated_at) 
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
        """, (key, str(value)))
        conn.commit()

def get_preference(key, default=None):
    """Retrieves a user preference."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM user_preferences WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row["value"] if row else default
