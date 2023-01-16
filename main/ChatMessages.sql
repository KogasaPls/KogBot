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

CREATE INDEX main.ChatMessages_ChatRoomId_SentAtTime_index
    ON main.ChatMessages (ChatRoomId ASC, SentAtTime DESC);

CREATE INDEX main.ChatMessages_ChatterId_ChatRoomId_SentAtTime_index
    ON main.ChatMessages (ChatterId ASC, ChatRoomId ASC, SentAtTime DESC);
