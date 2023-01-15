CREATE TABLE ChatMessages
(
    Id INTEGER NOT NULL
        PRIMARY KEY,
    ChatterId INTEGER NOT NULL
        REFERENCES Chatters,
    ChatRoomId INTEGER NOT NULL
        REFERENCES ChatRooms,
    Message TEXT NOT NULL,
    SentAtTime INT NOT NULL
);
