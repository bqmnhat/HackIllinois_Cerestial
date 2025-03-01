DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_database WHERE datname = 'mydatabase'
   ) THEN
      EXECUTE 'CREATE DATABASE mydatabase';
   END IF;
END
$do$;

\c mydatabase

-- Create user separately
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'myuser'
   ) THEN
      EXECUTE 'CREATE USER myuser WITH ENCRYPTED PASSWORD ''mypassword''';
   END IF;
END
$do$;

GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

-- Create CONVERSATION table if it does not exist
CREATE TABLE IF NOT EXISTS CONVERSATION (
    id SERIAL PRIMARY KEY,
    isBot BOOLEAN NOT NULL,
    message TEXT NOT NULL,
    time TIMESTAMP
);
