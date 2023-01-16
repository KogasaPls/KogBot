CREATE TABLE main.Chatters
(
    Id INTEGER
        PRIMARY KEY,
    Name TEXT NOT NULL
        UNIQUE,
    LastMessageId INTEGER,
    LastMessageSentAt INT
);

CREATE INDEX main.Chatters_LastMessageSentAt_index
    ON main.Chatters (LastMessageSentAt DESC);
