package Tickets;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Ticket implements Comparable<Ticket> {
    public int idTicket;
    public int eventId;
    public String eventTitle;
    public String cost;
    public String startTime;
    public String endTime;
    public String status;

    //va fi conectat cu evenimentele


    public Ticket(int idTicket,int eventId, String eventTitle, String cost, String startTime, String endTime, String status) {
        this.idTicket = idTicket;
        this.eventId = eventId;
        this.eventTitle = eventTitle;
        this.cost = cost;
        this.startTime = startTime;
        this.endTime = endTime;
        this.status = status;
    }


    public Ticket(int idTicket,Scanner in){
        read(idTicket,in);
    }
    public Ticket(ResultSet in) throws SQLException {
        read(in);
    }
    public void read(ResultSet in) throws SQLException {
        this.idTicket = Integer.parseInt(in.getString("ticketId"));
        this.eventTitle = in.getString("eventTitle");
        this.cost = in.getString("cost");
        this.startTime = in.getString("startTime");
        this.endTime = in.getString("endTime");
        this.status = in.getString("status");
        this.eventId = Integer.parseInt(in.getString("eventId"));
    }

    public void read(int ticketId, Scanner in){
        this.idTicket = ticketId;
        System.out.println("Event Title: ");
        this.eventTitle = in.nextLine();
        System.out.println("Cost: ");
        this.cost = in.nextLine();
        System.out.println("Start Time: ");
        this.startTime = in.nextLine();
        System.out.println("End Time: ");
        this.endTime = in.nextLine();
        System.out.println("Status: ");
        this.status = in.nextLine();
    }

    @Override
    public String toString() {
        return "Ticket{" +
                "idTicket='" + idTicket + '\'' +
                ", eventTitle='" + eventTitle + '\'' +
                ", cost='" + cost + '\'' +
                ", startTime='" + startTime + '\'' +
                ", endTime='" + endTime + '\'' +
                ", status='" + status + '\'' +
                ", eventId='" + eventId + '\'' +
                '}';
    }

    public int getIdTicket() {
        return idTicket;
    }

    public void setIdTicket(int idTicket) {
        this.idTicket = idTicket;
    }

    public String getEventTitle() {
        return eventTitle;
    }

    public void setEventTitle(String eventTitle) {
        this.eventTitle = eventTitle;
    }

    public String getCost() {
        return cost;
    }

    public void setCost(String cost) {
        this.cost = cost;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }

    public String getEndTime() {
        return endTime;
    }

    public void setEndTime(String endTime) {
        this.endTime = endTime;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public int getEventId() {
        return eventId;
    }

    public void setEventId(int eventId) {
        this.eventId = eventId;
    }

    public int getIntCost(){
        int idx = 0;
        String intCost = "";
        do {
            intCost+=cost.charAt(idx);
            idx+=1;
        }while(cost.charAt(idx+1) != ' ');

        intCost+=cost.charAt(idx);
        return Integer.parseInt(intCost);
    }

    @Override
    public int compareTo(Ticket o) {
        return this.cost.compareTo(o.getCost());
    }
}
