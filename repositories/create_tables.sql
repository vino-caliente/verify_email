-- registration_db

CREATE TABLE IF NOT EXISTS Users (
    usr_id SERIAL,
    usr_login VARCHAR(100),
    usr_email VARCHAR(100) UNIQUE,
    usr_password_hash VARCHAR(100),
    usr_is_verified BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (usr_id)
);

CREATE TABLE IF NOT EXISTS Tokens (
    tkn_token VARCHAR(100) UNIQUE,
    usr_id INT NOT NULL,
    tkn_expires_at TIMESTAMPTZ,
    PRIMARY KEY (usr_id),
    FOREIGN KEY (usr_id) REFERENCES Users(usr_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);