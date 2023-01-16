CREATE TABLE main.ChatMessages
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

CREATE INDEX ChatMessages_ChatRoomId_SentAtTime_index
    ON ChatMessages (ChatRoomId ASC, SentAtTime DESC);

CREATE INDEX ChatMessages_ChatterId_ChatRoomId_SentAtTime_index
    ON ChatMessages (ChatterId ASC, ChatRoomId ASC, SentAtTime DESC);
