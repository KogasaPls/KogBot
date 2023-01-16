CREATE TABLE main.Chatters
(
    Id INTEGER
        PRIMARY KEY,
    Name TEXT NOT NULL
        UNIQUE,
    LastMessageId INTEGER,
    LastMessageSentAt INT
);
