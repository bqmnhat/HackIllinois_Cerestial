DO
$do$
BEGIN
   -- Check if the database exists, and drop it if it does
   IF EXISTS (
      SELECT FROM pg_catalog.pg_database WHERE datname = 'mydatabase'
   ) THEN
      EXECUTE 'DROP DATABASE IF EXISTS mydatabase';
   END IF;

   -- Create the database
   EXECUTE 'CREATE DATABASE mydatabase';
END
$do$;

\c mydatabase

-- Create user separately (drop and recreate if necessary)
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'myuser'
   ) THEN
      EXECUTE 'DROP USER IF EXISTS myuser';
   END IF;

   -- Create user with a password
   EXECUTE 'CREATE USER myuser WITH ENCRYPTED PASSWORD ''mypassword''';
END
$do$;

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

-- Create CONVERSATION table if it does not exist
CREATE TABLE IF NOT EXISTS CONVERSATION (
    id SERIAL PRIMARY KEY,
    isBot BOOLEAN NOT NULL,
    message TEXT NOT NULL,
    time TIMESTAMP
);
