#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime

# Use absolute path since cron runs from different directory
DB_PATH = '/home/pi/your-flask-app/calls.db'  # Update this path
OUTPUT_PATH = '/home/pi/stats.json'  # This file will be served by Flask

# Connect to database
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

# Gather all your stats
stats = {
    'last_updated': datetime.now().isoformat(),
    'total_calls': conn.execute('SELECT COUNT(*) FROM calls').fetchone()[0],
    'successful_calls': conn.execute('SELECT COUNT(*) FROM calls WHERE status = 200').fetchone()[0],
    'failed_calls': conn.execute('SELECT COUNT(*) FROM calls WHERE status != 200').fetchone()[0],
    'average_brightness': conn.execute('SELECT AVG(brightness) FROM calls WHERE brightness IS NOT NULL').fetchone()[0],
    'last_24h_calls': conn.execute('''
        SELECT COUNT(*) FROM calls 
        WHERE timestamp > datetime('now', '-1 day')
    ''').fetchone()[0],
    'recent_calls': [dict(row) for row in conn.execute('''
        SELECT datetime(timestamp, 'localtime') as time, brightness, status 
        FROM calls 
        ORDER BY id DESC 
        LIMIT 20
    ''').fetchall()],
    'daily_stats': [dict(row) for row in conn.execute('''
        SELECT 
            date(timestamp) as date,
            COUNT(*) as calls,
            AVG(brightness) as avg_brightness
        FROM calls 
        GROUP BY date(timestamp)
        ORDER BY date DESC
        LIMIT 30
    ''').fetchall()]
}

conn.close()

# Write to JSON file
with open(OUTPUT_PATH, 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Stats exported at {datetime.now()}")
