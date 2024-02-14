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

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    adventure_id INTEGER REFERENCES adventures,
    stars INTEGER,
    comment TEXT
);