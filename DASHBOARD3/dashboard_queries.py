import sqlite3

def fetch_kpis():
    conn = sqlite3.connect("data/hotel_dashboard.db")
    cur = conn.cursor()

    kpis = {}

    cur.execute("SELECT SUM(price) FROM Room_Rates;")
    kpis["total_revenue"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) * 1.0 / (
            SELECT COUNT(*) FROM Rooms
        ) FROM Bookings
        WHERE check_out >= DATE('now') AND check_in <= DATE('now');
    """)
    kpis["occupancy_rate"] = round(cur.fetchone()[0] * 100, 2)

    cur.execute("""
        SELECT AVG(price) FROM Room_Rates;
    """)
    kpis["adr"] = round(cur.fetchone()[0], 2)

    cur.execute("""
        SELECT AVG(rating) FROM Reviews;
    """)
    kpis["nps"] = round(cur.fetchone()[0], 1)

    conn.close()
    return kpis

def fetch_monthly_revenue():
    conn = sqlite3.connect("data/hotel_dashboard.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT strftime('%Y-%m', date), SUM(price)
        FROM Room_Rates
        GROUP BY strftime('%Y-%m', date)
        ORDER BY 1 ASC;
    """)
    data = cur.fetchall()
    conn.close()
    return data

def fetch_market_share():
    conn = sqlite3.connect("data/hotel_dashboard.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT Rooms.room_type, COUNT(*) AS bookings
        FROM Bookings
        JOIN Rooms ON Bookings.room_id = Rooms.room_id
        GROUP BY Rooms.room_type;
    """)
    data = cur.fetchall()
    conn.close()
    return data

def fetch_guest_satisfaction():
    conn = sqlite3.connect("data/hotel_dashboard.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT rating, COUNT(*) FROM Reviews GROUP BY rating;
    """)
    data = cur.fetchall()
    conn.close()
    return data 