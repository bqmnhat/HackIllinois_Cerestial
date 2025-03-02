-- Create user with password and database creation privileges
CREATE USER myuser WITH PASSWORD 'mypassword';

-- Create database
CREATE DATABASE mydatabase;

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

-- Connect to the newly created database
\c mydatabase


-- Create conversation table
CREATE TABLE CONVERSATION (
    id SERIAL PRIMARY KEY,
    isBot BOOLEAN NOT NULL,
    message TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant privileges on the table to the user
GRANT ALL PRIVILEGES ON TABLE conversation TO myuser;
GRANT USAGE, SELECT ON SEQUENCE conversation_id_seq TO myuser;