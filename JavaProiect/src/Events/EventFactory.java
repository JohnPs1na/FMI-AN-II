package Events;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class EventFactory {
    private static int eventId = 0;

    public Event createEvent(Scanner in){
        return new Event(++eventId,in);
    }
    public Event createEvent(ResultSet in) throws SQLException {
        eventId++;
        return new Event(in);
    }
}
