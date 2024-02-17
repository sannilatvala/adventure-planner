CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE adventures (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    duration TEXT,
    cost INTEGER,
    difficulty_level TEXT,
    environment TEXT,
    group_size TEXT,
    season TEXT
);

CREATE TABLE preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    duration_preference TEXT,
    budget_preference INTEGER,
    difficulty_preference TEXT,
    environment_preference TEXT,
    group_size_preference TEXT,
    season_preference TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    adventure_id INTEGER REFERENCES adventures,
    stars INTEGER,
    comment TEXT
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    adventure_id INTEGER REFERENCES adventures
);