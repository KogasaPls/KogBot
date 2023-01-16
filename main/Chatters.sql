CREATE TABLE Chatters
(
    Id INTEGER
        PRIMARY KEY,
    Name TEXT NOT NULL
        UNIQUE,
    LastMessageId INTEGER,
    LastMessageSentAt INT
);

CREATE INDEX Chatters_LastMessageSentAt_index
    ON Chatters (LastMessageSentAt DESC);
