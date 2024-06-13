-- Creates a table for users with unique email addresses and optional names.
-- If the table exists, the script will not cause an error.

CREATE TABLE IF NOT EXISTS users (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
name VARCHAR(255)
);
