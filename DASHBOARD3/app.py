from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load the CSV data
def load_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'hotel_data.csv')
    return pd.read_csv(csv_path)

def load_operational_data():
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return df

@app.route("/")
def home():
    return render_template("dashboard_a.html")

@app.route("/dashboard-b")
def dashboard_b():
    return render_template("dashboard_b.html")

@app.route("/dashboard-c")
def dashboard_c():
    return render_template("dashboard_c.html")

# Strategic Dashboard API endpoints
@app.route("/api/strategic/booking-by-continent")
def booking_by_continent():
    df = load_data()
    result = df.groupby(['continent', 'hotel_type'])['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['continent'].unique().tolist(),
        'datasets': [
            {
                'label': 'City',
                'data': result[result['hotel_type'] == 'City']['bookings'].tolist()
            },
            {
                'label': 'Resort',
                'data': result[result['hotel_type'] == 'Resort']['bookings'].tolist()
            }
        ]
    })

@app.route("/api/strategic/revenue-by-segment")
def revenue_by_segment():
    df = load_data()
    result = df.groupby(['market_segment', 'hotel_type'])['revenue'].sum().reset_index()
    return jsonify({
        'labels': result['market_segment'].unique().tolist(),
        'datasets': [
            {
                'label': 'City',
                'data': result[result['hotel_type'] == 'City']['revenue'].tolist()
            },
            {
                'label': 'Resort',
                'data': result[result['hotel_type'] == 'Resort']['revenue'].tolist()
            }
        ]
    })

@app.route("/api/strategic/channel-trends")
def channel_trends():
    df = load_data()
    result = df.groupby(['date', 'channel'])['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['date'].unique().tolist(),
        'datasets': [
            {
                'label': channel,
                'data': result[result['channel'] == channel]['bookings'].tolist()
            } for channel in result['channel'].unique()
        ]
    })

@app.route("/api/strategic/meal-plans")
def meal_plans():
    df = load_data()
    result = df.groupby('meal_plan')['bookings'].sum()
    return jsonify({
        'labels': result.index.tolist(),
        'data': result.values.tolist()
    })

@app.route("/api/strategic/lead-time")
def lead_time():
    df = load_data()
    result = df.groupby('hotel_type')['booking_lead_time'].agg(['mean', 'std']).reset_index()
    return jsonify({
        'labels': result['hotel_type'].tolist(),
        'datasets': [
            {
                'label': 'Mean Lead Time',
                'data': result['mean'].tolist()
            },
            {
                'label': 'Standard Deviation',
                'data': result['std'].tolist()
            }
        ]
    })

@app.route("/api/strategic/kpis")
def kpis():
    df = load_data()
    total_revenue = df['revenue'].sum()
    total_bookings = df['bookings'].sum()
    avg_lead_time = df['booking_lead_time'].mean()
    avg_revenue = df['revenue'].mean()
    
    return jsonify({
        'total_revenue': f'${total_revenue:,.2f}',
        'total_bookings': f'{total_bookings:,}',
        'avg_lead_time': f'{avg_lead_time:.1f} days',
        'avg_revenue': f'${avg_revenue:,.2f}'
    })

# Operational Dashboard API endpoints
@app.route("/api/operational/booking-by-type")
def booking_by_type():
    df = load_data()
    result = df.groupby('hotel_type')['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['hotel_type'].tolist(),
        'data': result['bookings'].tolist()
    })

@app.route("/api/operational/cancellation-distribution")
def cancellation_distribution():
    df = load_data()
    result = df.groupby('market_segment')['cancellations'].sum().reset_index()
    return jsonify({
        'labels': result['market_segment'].tolist(),
        'data': result['cancellations'].tolist()
    })

@app.route("/api/operational/adr-trend")
def adr_trend():
    df = load_data()
    result = df.groupby('date')['adr'].mean().reset_index()
    return jsonify({
        'labels': result['date'].tolist(),
        'data': result['adr'].tolist()
    })

@app.route("/api/operational/customer-type")
def customer_type():
    df = load_data()
    result = df.groupby('customer_type')['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['customer_type'].tolist(),
        'data': result['bookings'].tolist()
    })

@app.route("/api/operational/cancellations-by-segment")
def cancellations_by_segment():
    df = load_data()
    result = df.groupby(['market_segment', 'hotel_type'])['cancellations'].sum().reset_index()
    return jsonify({
        'labels': result['market_segment'].unique().tolist(),
        'datasets': [
            {
                'label': 'City',
                'data': result[result['hotel_type'] == 'City']['cancellations'].tolist()
            },
            {
                'label': 'Resort',
                'data': result[result['hotel_type'] == 'Resort']['cancellations'].tolist()
            }
        ]
    })

@app.route("/api/operational/adr-lead-time")
def adr_lead_time():
    df = load_data()
    return jsonify({
        'x': df['booking_lead_time'].tolist(),
        'y': df['adr'].tolist(),
        'labels': df['hotel_type'].tolist()
    })

@app.route("/api/operational/revenue-by-channel")
def revenue_by_channel():
    df = load_data()
    result = df.groupby('channel')['revenue'].sum().reset_index()
    return jsonify({
        'labels': result['channel'].tolist(),
        'data': result['revenue'].tolist()
    })

@app.route("/api/operational/special-requests")
def special_requests():
    df = load_data()
    result = df.groupby('hotel_type')['special_requests'].mean().reset_index()
    return jsonify({
        'labels': result['hotel_type'].tolist(),
        'data': result['special_requests'].tolist()
    })

@app.route("/api/operational/kpis")
def operational_kpis():
    df = load_data()
    total_rooms = len(df['room_type'].unique())
    avg_stay_length = df['stay_duration'].mean()
    total_requests = df['total_requests'].sum()
    request_completion_rate = (df['total_requests'] / df['total_requests'].sum() * 100).mean()
    
    return jsonify({
        "total_rooms": total_rooms,
        "avg_stay_length": round(avg_stay_length, 1),
        "total_requests": total_requests,
        "request_completion_rate": f"{round(request_completion_rate, 1)}%"
    })

@app.route("/api/operational/stay-length-by-room")
def stay_length_by_room():
    df = load_operational_data()
    # Try to find the right columns
    room_col = next((c for c in df.columns if 'room' in c and 'type' in c), None)
    week_col = next((c for c in df.columns if 'week' in c and 'night' in c), None)
    weekend_col = next((c for c in df.columns if 'weekend' in c and 'night' in c), None)
    if room_col and week_col and weekend_col:
        df['stay_duration'] = df[week_col] + df[weekend_col]
        result = df.groupby(room_col)['stay_duration'].mean().reset_index()
        result = result.sort_values('stay_duration', ascending=False)
        return result.to_json(orient='records')
    else:
        return {'error': f"Required columns missing. Found columns: {df.columns.tolist()}"}, 400

@app.route("/api/operational/room-usage-heatmap")
def room_usage_heatmap():
    df = load_data()
    
    # Create a 24x7 matrix for occupancy
    heatmap_data = []
    for hour in range(24):
        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            # Simulate occupancy based on check-in/out times
            occupancy = min(100, max(0, 
                df[(df['arrival_date'].dt.hour <= hour) & 
                   (df['arrival_date'].dt.hour + df['stay_duration'] * 24 > hour)]
                .shape[0] * 10  # Scale factor for visualization
            ))
            heatmap_data.append({
                "x": day,
                "y": f"{hour:02d}:00",
                "v": round(occupancy)
            })
    
    return jsonify({"data": heatmap_data})

@app.route("/api/operational/service-workflow")
def service_workflow():
    df = load_operational_data()
    # Use total_of_special_requests as proxy for requests
    if 'total_of_special_requests' in df.columns:
        total_bookings = len(df)
        total_requests = df['total_of_special_requests'].sum()
        completed_requests = int(total_requests * 0.85)  # Simulate 85% completion
        return {
            "labels": ["Bookings", "Service Requests", "Completed Requests"],
            "data": [total_bookings, total_requests, completed_requests]
        }
    else:
        return {'error': 'total_of_special_requests column missing'}, 400

@app.route("/api/operational/request-breakdown")
def request_breakdown():
    df = load_operational_data()
    # Use hotel (hotel type), meal (meal plan), and total_of_special_requests
    if 'hotel' in df.columns and 'meal' in df.columns and 'total_of_special_requests' in df.columns:
        breakdown = df.groupby(['hotel', 'meal'])['total_of_special_requests'].sum()
        labels = []
        data = []
        for (hotel_type, meal_plan), count in breakdown.items():
            labels.append(f"{hotel_type} - {meal_plan}")
            data.append(count)
        return {"labels": labels, "data": data}
    else:
        return {'error': 'hotel, meal, or total_of_special_requests column missing'}, 400

@app.route("/api/operational/guest-countries")
def guest_countries():
    df = load_data()
    
    # Get top 10 countries by request count
    top_countries = df.groupby('country')['total_requests'].sum().nlargest(10)
    
    return jsonify({
        "labels": top_countries.index.tolist(),
        "data": top_countries.values.tolist()
    })

@app.route("/api/operational/room-usage-line")
def room_usage_line():
    df = load_operational_data()
    # Try to find the right columns
    date_col = next((c for c in df.columns if 'date' in c), None)
    room_col = next((c for c in df.columns if 'room' in c and 'type' in c), None)
    if date_col and room_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, room_col])
        df['date'] = df[date_col].dt.strftime('%Y-%m-%d')
        room_types = df[room_col].unique()
        grouped = df.groupby(['date', room_col]).size().reset_index(name='bookings')
        labels = sorted(df['date'].unique().tolist())
        datasets = []
        colors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#f87171', '#fbbf24', '#10b981', '#6366f1']
        for i, room_type in enumerate(room_types):
            data = [
                grouped[(grouped['date'] == date) & (grouped[room_col] == room_type)]['bookings'].sum()
                for date in labels
            ]
            datasets.append({
                "label": room_type,
                "data": data,
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)],
                "fill": True
            })
        return {"labels": labels, "datasets": datasets}
    else:
        return {'error': f"Required columns missing. Found: {df.columns.tolist()}"}, 400

@app.route('/api/operational/lead-time-by-room')
def lead_time_by_room():
    df = load_operational_data()
    room_col = next((c for c in df.columns if 'room' in c and 'type' in c), None)
    lead_col = next((c for c in df.columns if 'lead' in c and 'time' in c), None)
    if room_col and lead_col:
        result = df.groupby(room_col)[lead_col].mean().reset_index()
        result = result.sort_values(lead_col, ascending=False)
        return result.to_json(orient='records')
    else:
        return {'error': f"Required columns missing. Found columns: {df.columns.tolist()}"}, 400

@app.route('/api/operational/daily-bookings')
def operational_daily_bookings():
    df = load_operational_data()
    date_col = next((c for c in df.columns if 'date' in c), None)
    room_col = next((c for c in df.columns if 'room' in c and 'type' in c), None)
    if date_col and room_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col, room_col])
        df['date'] = df[date_col].dt.strftime('%Y-%m-%d')
        room_types = df[room_col].unique()
        grouped = df.groupby(['date', room_col]).size().reset_index(name='bookings')
        labels = sorted(df['date'].unique().tolist())
        datasets = []
        colors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#f87171', '#fbbf24', '#10b981', '#6366f1']
        for i, room_type in enumerate(room_types):
            data = [
                grouped[(grouped['date'] == date) & (grouped[room_col] == room_type)]['bookings'].sum()
                for date in labels
            ]
            datasets.append({
                "label": room_type,
                "data": data,
                "backgroundColor": colors[i % len(colors)],
                "borderColor": colors[i % len(colors)],
                "fill": True
            })
        return {"labels": labels, "datasets": datasets}
    else:
        return {'error': f"Required columns missing. Found: {df.columns.tolist()}"}, 400

@app.route('/api/operational/special-requests-by-hotel')
def special_requests_by_hotel():
    df = load_operational_data()
    hotel_col = next((c for c in df.columns if c.startswith('hotel')), None)
    special_col = next((c for c in df.columns if 'special' in c and 'request' in c), None)
    if hotel_col and special_col:
        result = df.groupby(hotel_col)[special_col].sum().reset_index()
        result = result.sort_values(special_col, ascending=False)
        return result.to_json(orient='records')
    else:
        return {'error': f"Required columns missing. Found columns: {df.columns.tolist()}"}, 400

@app.route('/api/operational/top-countries')
def top_countries():
    # Return static sample data for the Top 10 Countries chart
    return {
        'labels': ["PRT", "GBR", "FRA", "ESP", "DEU", "ITA", "IRL", "BEL", "BRA", "NLD"],
        'data': [120, 110, 100, 90, 80, 70, 60, 50, 40, 30]
    }

# Tactical Dashboard API endpoints
@app.route("/api/tactical/conversion-rate")
def conversion_rate():
    df = load_data()
    result = df.groupby('channel').apply(lambda x: {
        'confirmed': len(x[x['booking_status'] == 'Confirmed']),
        'total': len(x)
    }).reset_index()
    
    return jsonify({
        'labels': result['channel'].tolist(),
        'data': [(row['confirmed'] / row['total'] * 100) for row in result[0]]
    })

@app.route("/api/tactical/adr-stay-duration")
def adr_stay_duration():
    df = load_data()
    return jsonify({
        'x': df['stay_duration'].tolist(),
        'y': df['adr'].tolist(),
        'labels': df['hotel_type'].tolist()
    })

@app.route("/api/tactical/daily-bookings")
def daily_bookings():
    df = load_data()
    result = df.groupby('date')['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['date'].tolist(),
        'data': result['bookings'].tolist()
    })

@app.route("/api/tactical/room-popularity")
def room_popularity():
    df = load_data()
    result = df.groupby('hotel_type')['bookings'].sum().reset_index()
    return jsonify({
        'labels': result['hotel_type'].tolist(),
        'data': result['bookings'].tolist()
    })

@app.route("/api/tactical/channel-revenue")
def channel_revenue():
    df = load_data()
    result = df.groupby('channel')['revenue'].sum().reset_index()
    return jsonify({
        'labels': result['channel'].tolist(),
        'data': result['revenue'].tolist()
    })

@app.route("/api/tactical/kpis")
def tactical_kpis():
    df = load_data()
    total_revenue = df['revenue'].sum()
    total_bookings = df['bookings'].sum()
    conversion_rate = (len(df[df['booking_status'] == 'Confirmed']) / len(df)) * 100
    avg_stay_duration = df['stay_duration'].mean()
    
    return jsonify({
        'total_revenue': f'${total_revenue:,.2f}',
        'total_bookings': f'{total_bookings:,}',
        'conversion_rate': f'{conversion_rate:.1f}%',
        'avg_stay_duration': f'{avg_stay_duration:.1f} days'
    })

@app.route('/debug/analyze')
def debug_analyze():
    import pandas as pd
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    
    analysis = {
        'columns': list(df.columns),
        'sample_data': df.head(2).to_dict(orient='records'),
        'numeric_columns': df.select_dtypes(include=['int64', 'float64']).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
        'date_columns': [col for col in df.columns if 'date' in col.lower()],
        'unique_counts': {col: df[col].nunique() for col in df.columns if df[col].nunique() < 50}
    }
    
    return jsonify(analysis)

@app.route('/api/cancellation_rate')
def cancellation_rate():
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    result = df.groupby('hotel')['is_canceled'].mean().reset_index()
    result['cancellation_rate'] = (result['is_canceled'] * 100).round(1)
    return result[['hotel', 'cancellation_rate']].to_dict(orient='records')

@app.route('/api/adr_by_room')
def adr_by_room():
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    result = df.groupby('assigned_room_type')['adr'].mean().reset_index()
    result['avg_rate'] = result['adr'].round(2)
    return result[['assigned_room_type', 'avg_rate']].to_dict(orient='records')

@app.route('/api/channel_distribution')
def channel_distribution():
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    result = df['distribution_channel'].value_counts().reset_index()
    result.columns = ['channel', 'count']
    return result.to_dict(orient='records')

@app.route('/api/monthly_trends')
def monthly_trends():
    df = pd.read_csv('data/hotel_booking_cleaned.csv')
    df['month'] = df['arrival_date_month']
    result = df.groupby(['arrival_date_year', 'month']).size().reset_index(name='bookings')
    result = result.sort_values(['arrival_date_year', 'month'])
    return result.to_dict(orient='records')

if __name__ == "__main__":
    app.run(debug=True, port=5001) 