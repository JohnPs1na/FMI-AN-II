package Events;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Event {

    private int eventId;
    private int ticketNum;
    private String title;
    private String genre;
    private String status;
    private String startTime;
    private String location;

    public Event(int eventId, int ticketNum, String title, String genre, String status, String startTime, String location) {
        this.eventId = eventId;
        this.ticketNum = ticketNum;
        this.title = title;
        this.genre = genre;
        this.status = status;
        this.startTime = startTime;
        this.location = location;
    }

    public Event(int eventId, Scanner in){
        this.eventId = eventId;
        read(in);
    }

    public Event(ResultSet in) throws SQLException {
        read(in);
    }
    public void read(ResultSet in) throws SQLException {
        this.eventId = Integer.parseInt(in.getString("eventId"));
        this.ticketNum = Integer.parseInt(in.getString("ticketNum"));
        this.title = in.getString("title");
        this.genre = in.getString("genre");
        this.status = in.getString("status");
        this.startTime = in.getString("startTime");
        this.location = in.getString("location");
    }
    public void read(Scanner in){
        System.out.println("Event Title:");
        this.title = in.nextLine();
        System.out.println("Ticket number:");
        this.ticketNum = Integer.parseInt(in.nextLine());
        System.out.println("Genre:");
        this.genre = in.nextLine();
        System.out.println("Status:");
        this.status = in.nextLine();
        System.out.println("Start Time:");
        this.startTime = in.nextLine();
        System.out.println("Location:");
        this.location = in.nextLine();
    }


    @Override
    public String toString() {
        return "Event{" +
                "eventId=" + eventId +
                ", ticketNum=" + ticketNum +
                ", title='" + title + '\'' +
                ", genre='" + genre + '\'' +
                ", status='" + status + '\'' +
                ", startTime='" + startTime + '\'' +
                ", Location='" + location + '\'' +
                '}';
    }

    public int getEventId() {
        return eventId;
    }

    public void setEventId(int eventId) {
        this.eventId = eventId;
    }

    public int getTicketNum() {
        return ticketNum;
    }

    public void setTicketNum(int ticketNum) {
        this.ticketNum = ticketNum;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }
}
