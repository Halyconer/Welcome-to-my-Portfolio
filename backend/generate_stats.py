#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime, timedelta

# Should be in the same directory
DB_PATH = 'calls.db'
OUTPUT_PATH = 'stats.json'

# Only export last 24 hours of data
try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    stats = {
        'last_updated': datetime.now().isoformat(),
        'collection_period': '24_hours',
        'update_frequency': 'daily',
        
        'total_calls_all_time': conn.execute('SELECT COUNT(*) FROM calls').fetchone()[0],
        'avg_brightness_all_time': conn.execute('SELECT AVG(brightness) FROM calls').fetchone()[0]
        }

    conn.close()

    # Write stats
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"Total stats exported at {datetime.now()} (updates daily)")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error generating stats: {e}")
