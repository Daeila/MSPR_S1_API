DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS keys;

-- user_type : 1=revendeur, 2=webshop
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    user_type INTEGER NOT NULL CHECK (user_type IN (1, 2))
);
