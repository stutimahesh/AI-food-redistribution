CREATE TABLE users (
    id SERIAL PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    phone VARCHAR(15),

    role VARCHAR(20) NOT NULL
        CHECK(role IN ('donor','ngo','driver','admin')),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--------------------------------------------------------

CREATE TABLE donors (

    id SERIAL PRIMARY KEY,

    user_id INTEGER UNIQUE NOT NULL,

    organization_name VARCHAR(150),

    address TEXT,

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

--------------------------------------------------------

CREATE TABLE ngos (

    id SERIAL PRIMARY KEY,

    user_id INTEGER UNIQUE NOT NULL,

    ngo_name VARCHAR(150),

    address TEXT,

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    max_capacity INTEGER,

    current_capacity INTEGER DEFAULT 0,

    active BOOLEAN DEFAULT TRUE,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

--------------------------------------------------------

CREATE TABLE drivers (

    id SERIAL PRIMARY KEY,

    user_id INTEGER UNIQUE NOT NULL,

    vehicle_type VARCHAR(50),

    vehicle_number VARCHAR(30),

    available BOOLEAN DEFAULT TRUE,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

--------------------------------------------------------

CREATE TABLE donations (

    id SERIAL PRIMARY KEY,

    donor_id INTEGER NOT NULL,

    food_name VARCHAR(100),

    food_type VARCHAR(50),

    quantity INTEGER,

    cooked_time TIMESTAMP,

    expiry_time TIMESTAMP,

    pickup_address TEXT,

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    status VARCHAR(30)
        DEFAULT 'Pending',

    created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(donor_id)
        REFERENCES donors(id)
        ON DELETE CASCADE
);

--------------------------------------------------------

CREATE TABLE recommendations (

    id SERIAL PRIMARY KEY,

    donation_id INTEGER,

    ngo_id INTEGER,

    score DOUBLE PRECISION,

    acceptance_probability DOUBLE PRECISION,

    distance DOUBLE PRECISION,

    eta INTEGER,

    created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(donation_id)
        REFERENCES donations(id)
        ON DELETE CASCADE,

    FOREIGN KEY(ngo_id)
        REFERENCES ngos(id)
        ON DELETE CASCADE
);

--------------------------------------------------------

CREATE TABLE deliveries (

    id SERIAL PRIMARY KEY,

    donation_id INTEGER,

    driver_id INTEGER,

    ngo_id INTEGER,

    pickup_time TIMESTAMP,

    delivered_time TIMESTAMP,

    delivery_status VARCHAR(30)
        DEFAULT 'Assigned',

    FOREIGN KEY(donation_id)
        REFERENCES donations(id),

    FOREIGN KEY(driver_id)
        REFERENCES drivers(id),

    FOREIGN KEY(ngo_id)
        REFERENCES ngos(id)
);

--------------------------------------------------------

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_donations_status
ON donations(status);

CREATE INDEX idx_ngo_location
ON ngos(latitude, longitude);

CREATE INDEX idx_donor_location
ON donors(latitude, longitude);