CREATE TABLE ChatMessages
(
    Id INTEGER
        PRIMARY KEY,
    ChatterName TEXT NOT NULL,
    ChatRoomName TEXT NOT NULL,
    Message TEXT NOT NULL,
    SentAtTime INT NOT NULL,
    ChatterId INTEGER,
    ChatRoomId INTEGER
);
