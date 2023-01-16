CREATE TRIGGER tInsertChatMessage
    AFTER UPDATE OF ChatterName
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
END;