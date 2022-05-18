package Tickets;

import Persons.Clients.Client;
import com.sun.jdi.event.ExceptionEvent;
import option_function.option_function;
import option_function.runMenu;

import javax.swing.plaf.nimbus.State;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.*;

public class TicketService extends runMenu {
    private static TicketService ticketService_instance = null;
    private final HashMap<Integer,Ticket> ticketList = new HashMap<>();
    private final TicketFactory ticketFactory = new TicketFactory();

    private TicketService(){

        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("select * from tickets");
            while(resultSet.next()){
                Ticket t = ticketFactory.createTicket(resultSet);
                ticketList.put(t.getIdTicket(),t);
            }
        } catch (Exception e){
            e.printStackTrace();
        }

        operations.add(
                new option_function(
                        "Add Ticket",
                        ()-> {
                            Scanner in = new Scanner(System.in);
                            Ticket t = ticketFactory.createTicket(in);
                            createTicket(t);
                        }));
        operations.add(
                new option_function(
                        "Delete ticket by id",
                        ()-> {
                            for(Ticket ticket : ticketList.values()){
                                System.out.println(ticket);
                            }
                            System.out.println("Insert the id of the ticket you want to delete");
                            Scanner in = new Scanner(System.in);
                            int id = Integer.parseInt(in.nextLine());
                            for(int i : ticketList.keySet()) {
                                Ticket t = ticketList.get(i);
                                if (t.getIdTicket() == id) {
                                    ticketList.remove(i);
                                    deleteTicketById(id);
                                    break;
                                }
                            }
                        }));

        operations.add(
                new option_function(
                        "Search",
                        () -> {
                            Scanner in  = new Scanner(System.in);
                            System.out.println("Search for a ticket");
                            String str = in.nextLine();
                            List<Ticket> sortedList = getSortedTickets(str);
                            for (Ticket t : sortedList){
                                System.out.println(t.toString());
                            }
                        }
                )
        );
        operations.add(new option_function(
                "Get All Tickets",
                ()-> {
                    for(Ticket ticket : ticketList.values()){
                        System.out.println(ticket);
                    }
                }));
    }

    public static TicketService getInstance(){
        if (ticketService_instance == null){
            ticketService_instance = new TicketService();
        }
        return ticketService_instance;
    }

    public void showTickets(){
        for (Ticket ticket : ticketList.values()){
            System.out.println(ticket);
        }
    }
    public void createTicket(Ticket ticket){
        try{
            String eventQ = "select eventId from events where title = ?";
            PreparedStatement stmtE = connection.prepareStatement(eventQ);
            stmtE.setString(1,ticket.getEventTitle());
            ResultSet res = stmtE.executeQuery();
            int eventId=0;
            while(res.next()){
                eventId = Integer.parseInt(res.getString("eventId"));
                break;
            }
            String s = "Insert into tickets (ticketId,eventId,eventTitle,cost,startTime,endTime,status) values (?,?,?,?,?,?,?)";
            PreparedStatement stmt = connection.prepareStatement(s);
            stmt.setInt(1,ticket.getIdTicket() + 1);
            stmt.setInt(2,eventId);
            stmt.setString(3,ticket.getEventTitle());
            stmt.setString(4,ticket.getCost());
            stmt.setString(5,ticket.getStartTime());
            stmt.setString(6,ticket.getEndTime());
            stmt.setString(7,ticket.getStatus());
            stmt.executeUpdate();
            stmt.close();
            ticket.setIdTicket(ticket.getIdTicket() + 1);
            ticket.setEventId(eventId);
            ticketList.put(ticket.getIdTicket(),ticket);
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    public void createDefaultTicket(int eventId,String cost,String eventTitle, String startTime){
        try{
            Ticket t = ticketFactory.createDefaultTicket(eventId,cost,eventTitle,startTime);
            ticketList.put(t.getIdTicket(),t);
            String s = "Insert into tickets (ticketId,eventId,eventTitle,cost,startTime,endTime,status) values (?,?,?,?,?,?,?)";
            PreparedStatement stmt = connection.prepareStatement(s);
            stmt.setInt(1,ticketFactory.getTicketId());
            stmt.setInt(2,eventId);
            stmt.setString(3,eventTitle);
            stmt.setString(4,cost);
            stmt.setString(5,startTime);
            stmt.setString(6,"-");
            stmt.setString(7,"normal");
            stmt.executeUpdate();
            stmt.close();

        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public Ticket getTicketById(int ticketId){
        try{
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("select * from tickets where ticketId = "+ticketId);
            while(resultSet.next()) {
                Ticket t = ticketFactory.createTicket(resultSet);
                return t;
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        return null;
    }

    public List<Ticket> getSortedTickets(String str){
        List<Ticket> sortedList = new ArrayList<>();
        try{
            String q = "Select * from tickets where LOWER(eventTitle) LIKE '%" + str + "%' order by cost asc";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(q);
            while (resultSet.next()){
                sortedList.add(ticketFactory.createTicket(resultSet));
            }

        } catch (Exception e){
            e.printStackTrace();
            return null;
        }
        return sortedList;
    }
    public void deleteTicketById(int id){
        try {
            String q = "delete from tickets where ticketId = ?";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setInt(1,id);
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public void deleteTicketByEventId(int eventId){
        try {
//            ticketList.removeIf(ticket -> eventId == ticket.getEventId());
            for(Ticket t : ticketList.values()){
                if (t.getEventId() == eventId){
                    ticketList.remove(t.getIdTicket());
                }
            }
            String s = "Delete from tickets where eventId = ?";
            PreparedStatement stmt = connection.prepareStatement(s);
            stmt.setInt(1,eventId);
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

}
