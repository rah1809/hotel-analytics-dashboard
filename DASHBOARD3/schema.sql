-- Hotel Table
CREATE TABLE hotel (
    hotel_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT CHECK (type IN ('City', 'Resort')),
    continent TEXT,
    country TEXT
);

-- Room Type Table
CREATE TABLE room_type (
    room_type_id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotel(hotel_id),
    name TEXT NOT NULL,
    capacity INTEGER
);

-- Guest Table
CREATE TABLE guest (
    guest_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT
);

-- Booking Table
CREATE TABLE booking (
    booking_id INTEGER PRIMARY KEY,
    guest_id INTEGER REFERENCES guest(guest_id),
    hotel_id INTEGER REFERENCES hotel(hotel_id),
    room_type_id INTEGER REFERENCES room_type(room_type_id),
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    booking_date DATE NOT NULL,
    status TEXT CHECK (status IN ('Confirmed', 'Cancelled'))
);

-- Channel Table
CREATE TABLE channel (
    channel_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Booking Channel Table
CREATE TABLE booking_channel (
    booking_id INTEGER REFERENCES booking(booking_id),
    channel_id INTEGER REFERENCES channel(channel_id),
    PRIMARY KEY (booking_id, channel_id)
);

-- Special Request Table
CREATE TABLE special_request (
    request_id INTEGER PRIMARY KEY,
    booking_id INTEGER REFERENCES booking(booking_id),
    request_type TEXT,
    created_at DATE
);

-- Meal Plan Table
CREATE TABLE meal_plan (
    meal_plan_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Booking Meal Plan Table
CREATE TABLE booking_meal_plan (
    booking_id INTEGER REFERENCES booking(booking_id),
    meal_plan_id INTEGER REFERENCES meal_plan(meal_plan_id),
    PRIMARY KEY (booking_id, meal_plan_id)
);

-- Rate Table
CREATE TABLE rate (
    rate_id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotel(hotel_id),
    room_type_id INTEGER REFERENCES room_type(room_type_id),
    date DATE NOT NULL,
    adr FLOAT
); 