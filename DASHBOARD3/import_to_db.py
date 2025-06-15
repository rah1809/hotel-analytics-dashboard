import pandas as pd
import sqlite3
from tqdm import tqdm
import os

# Paths
CSV_PATH = os.path.join(os.path.dirname(__file__), 'data', 'hotel_booking_cleaned.csv')
DB_PATH = os.path.join(os.path.dirname(__file__), 'hotel_analytics.db')

# Connect to SQLite DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Helper caches to avoid duplicate inserts
hotel_cache = {}
room_type_cache = {}
guest_cache = {}
channel_cache = {}
meal_plan_cache = {}
skipped_rows = []

# Read CSV in chunks
chunk_size = 10000
for chunk in pd.read_csv(CSV_PATH, chunksize=chunk_size):
    for idx, row in tqdm(chunk.iterrows(), total=len(chunk), desc='Importing rows'):
        try:
            # --- Hotel ---
            hotel_key = (row['hotel'], row.get('continent', ''), row.get('country', ''))
            if hotel_key not in hotel_cache:
                cursor.execute('INSERT OR IGNORE INTO hotel (name, type, continent, country) VALUES (?, ?, ?, ?)',
                               (row['hotel'], row['hotel'], row.get('continent', ''), row.get('country', '')))
                cursor.execute('SELECT hotel_id FROM hotel WHERE name=? AND type=? AND continent=? AND country=?',
                               (row['hotel'], row['hotel'], row.get('continent', ''), row.get('country', '')))
                hotel_row = cursor.fetchone()
                if not hotel_row:
                    skipped_rows.append({'reason': 'hotel not found after insert', 'row': row.to_dict()})
                    continue
                hotel_id = hotel_row[0]
                hotel_cache[hotel_key] = hotel_id
            else:
                hotel_id = hotel_cache[hotel_key]

            # --- Room Type ---
            room_type_key = (hotel_id, row.get('reserved_room_type', 'Unknown'))
            if room_type_key not in room_type_cache:
                cursor.execute('INSERT OR IGNORE INTO room_type (hotel_id, name, capacity) VALUES (?, ?, ?)',
                               (hotel_id, row.get('reserved_room_type', 'Unknown'), None))
                cursor.execute('SELECT room_type_id FROM room_type WHERE hotel_id=? AND name=?',
                               (hotel_id, row.get('reserved_room_type', 'Unknown')))
                room_type_row = cursor.fetchone()
                if not room_type_row:
                    skipped_rows.append({'reason': 'room_type not found after insert', 'row': row.to_dict()})
                    continue
                room_type_id = room_type_row[0]
                room_type_cache[room_type_key] = room_type_id
            else:
                room_type_id = room_type_cache[room_type_key]

            # --- Guest ---
            guest_key = (row.get('name', 'Unknown'), row.get('country', ''))
            if guest_key not in guest_cache:
                cursor.execute('INSERT OR IGNORE INTO guest (name, country) VALUES (?, ?)',
                               (row.get('name', 'Unknown'), row.get('country', '')))
                cursor.execute('SELECT guest_id FROM guest WHERE name=? AND country=?',
                               (row.get('name', 'Unknown'), row.get('country', '')))
                guest_row = cursor.fetchone()
                if not guest_row:
                    skipped_rows.append({'reason': 'guest not found after insert', 'row': row.to_dict()})
                    continue
                guest_id = guest_row[0]
                guest_cache[guest_key] = guest_id
            else:
                guest_id = guest_cache[guest_key]

            # --- Booking ---
            cursor.execute('''INSERT INTO booking (guest_id, hotel_id, room_type_id, check_in_date, check_out_date, booking_date, status)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (guest_id, hotel_id, room_type_id, row.get('arrival_date'), row.get('departure_date'), row.get('booking_date'),
                            'Cancelled' if row.get('is_canceled', 0) == 1 else 'Confirmed'))
            booking_id = cursor.lastrowid

            # --- Channel ---
            channel_name = row.get('distribution_channel', 'Unknown')
            if channel_name not in channel_cache:
                cursor.execute('INSERT OR IGNORE INTO channel (name) VALUES (?)', (channel_name,))
                cursor.execute('SELECT channel_id FROM channel WHERE name=?', (channel_name,))
                channel_row = cursor.fetchone()
                if not channel_row:
                    skipped_rows.append({'reason': 'channel not found after insert', 'row': row.to_dict()})
                    continue
                channel_id = channel_row[0]
                channel_cache[channel_name] = channel_id
            else:
                channel_id = channel_cache[channel_name]
            cursor.execute('INSERT OR IGNORE INTO booking_channel (booking_id, channel_id) VALUES (?, ?)', (booking_id, channel_id))

            # --- Meal Plan ---
            meal_plan_name = row.get('meal', 'Unknown')
            if meal_plan_name not in meal_plan_cache:
                cursor.execute('INSERT OR IGNORE INTO meal_plan (name) VALUES (?)', (meal_plan_name,))
                cursor.execute('SELECT meal_plan_id FROM meal_plan WHERE name=?', (meal_plan_name,))
                meal_plan_row = cursor.fetchone()
                if not meal_plan_row:
                    skipped_rows.append({'reason': 'meal_plan not found after insert', 'row': row.to_dict()})
                    continue
                meal_plan_id = meal_plan_row[0]
                meal_plan_cache[meal_plan_name] = meal_plan_id
            else:
                meal_plan_id = meal_plan_cache[meal_plan_name]
            cursor.execute('INSERT OR IGNORE INTO booking_meal_plan (booking_id, meal_plan_id) VALUES (?, ?)', (booking_id, meal_plan_id))

            # --- Special Requests ---
            if row.get('total_of_special_requests', 0) > 0:
                cursor.execute('INSERT INTO special_request (booking_id, request_type, created_at) VALUES (?, ?, ?)',
                               (booking_id, 'General', row.get('booking_date')))

            # --- Rate ---
            if 'adr' in row and pd.notnull(row['adr']):
                cursor.execute('INSERT INTO rate (hotel_id, room_type_id, date, adr) VALUES (?, ?, ?, ?)',
                               (hotel_id, room_type_id, row.get('arrival_date'), row['adr']))
        except Exception as e:
            skipped_rows.append({'reason': str(e), 'row': row.to_dict()})
            continue
    conn.commit()

print(f'Data import complete! Skipped {len(skipped_rows)} rows.')
if skipped_rows:
    print('Sample skipped rows:')
    for s in skipped_rows[:5]:
        print(s['reason'])

cursor.close()
conn.close() 