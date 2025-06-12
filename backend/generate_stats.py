#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime, timedelta

# Update these paths to match your setup
DB_PATH = 'calls.db'
OUTPUT_PATH = 'stats.json'

# Only export last 24 hours of data
try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Calculate 24 hours ago
    one_day_ago = datetime.now() - timedelta(days=1)

    stats = {
        'last_updated': datetime.now().isoformat(),
        'collection_period': '24_hours',
        'total_calls_24h': conn.execute('''
            SELECT COUNT(*) FROM calls 
            WHERE timestamp > ?
        ''', (one_day_ago,)).fetchone()[0],
        'successful_calls_24h': conn.execute('''
            SELECT COUNT(*) FROM calls 
            WHERE status = 200 AND timestamp > ?
        ''', (one_day_ago,)).fetchone()[0],
        'hourly_breakdown': [dict(row) for row in conn.execute('''
            SELECT 
                strftime('%H', timestamp) as hour,
                COUNT(*) as calls,
                AVG(brightness) as avg_brightness
            FROM calls 
            WHERE timestamp > ?
            GROUP BY strftime('%H', timestamp)
            ORDER BY hour
        ''', (one_day_ago,)).fetchall()],
        'all_calls_24h': [dict(row) for row in conn.execute('''
            SELECT 
                datetime(timestamp, 'localtime') as time, 
                brightness, 
                status 
            FROM calls 
            WHERE timestamp > ?
            ORDER BY timestamp DESC
        ''', (one_day_ago,)).fetchall()]
    }

    conn.close()

    # Write stats
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"24-hour stats exported at {datetime.now()}")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error generating stats: {e}")