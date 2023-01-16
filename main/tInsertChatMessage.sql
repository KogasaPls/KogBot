CREATE TRIGGER tInsertChatMessage
    AFTER INSERT
    ON ChatMessages
BEGIN
    INSERT OR IGNORE INTO Chatters
        (
            Name
        )
    VALUES
        (
            NEW.ChatterName
        );
    INSERT OR IGNORE INTO ChatRooms
        (
            Name
        )
    VALUES
        (
            NEW.ChatRoomName
        );

    UPDATE ChatMessages
    SET ChatterId = (SELECT Id FROM Chatters WHERE Name = NEW.ChatterName)
      , ChatRoomId = (SELECT Id FROM ChatRooms WHERE Name = NEW.ChatRoomName)
    WHERE Id = NEW.Id;

    UPDATE Chatters
    SET LastMessageId = NEW.Id
      , LastMessageSentAt = NEW.SentAtTime
    WHERE Id = (SELECT Id FROM Chatters WHERE Name = NEW.ChatterName);
END;
