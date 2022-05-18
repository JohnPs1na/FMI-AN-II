package Tickets;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class TicketFactory {
    private static int ticketId;

    public Ticket createDefaultTicket(int eventId, String cost, String eventTitle, String startTime){
        return new Ticket(++ticketId,eventId,eventTitle,cost,startTime,"-","normal");
    }
    public Ticket createTicket(Scanner in){
        return new Ticket(ticketId++,in);
    }
    public Ticket createTicket(ResultSet in) throws SQLException {
        ticketId++;
        return new Ticket(in);
    }

    public int getTicketId(){
        return ticketId;
    }
}
