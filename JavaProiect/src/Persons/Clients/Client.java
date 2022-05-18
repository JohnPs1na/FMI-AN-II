package Persons.Clients;

import Persons.Person;
import groovy.sql.Sql;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Client extends Person {

    private int clientId;
    private String preferredGenre;

    public Client(int clientId, String firstName, String lastName, String birthDate, String phoneNumber, String city,String preferredGenre,String balance) {
        super(firstName, lastName, birthDate, phoneNumber, city,balance);
        this.preferredGenre = preferredGenre;
        this.clientId = clientId;
    }

    public Client(int clientId,Scanner in){
        super();
        read(clientId,in);
    }

    public Client(ResultSet in) throws SQLException {
        read(in);
    }
    public void read(ResultSet in) throws SQLException{
        super.read(in);
        this.clientId = Integer.parseInt(in.getString("clientId"));
        this.preferredGenre = in.getString("preferredGenre");
    }
    public void read(int id, Scanner in){
        super.read(in);
        this.clientId = id;
        System.out.println("Preferred Genre");
        this.preferredGenre = in.nextLine();
    }


    @Override
    public String toString() {
        return "Client{" +
                "clientId=" + clientId +
                ", preferredGenre='" + preferredGenre + '\'' +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", birthDate='" + birthDate + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", city='" + city + '\'' +
                ", balance='"+balance +'\''+
                '}';
    }

    @Override
    public int getClientId() {
        return clientId;
    }

    public void setClientId(int clientId) {
        this.clientId = clientId;
    }

    public String getPreferredGenre() {
        return preferredGenre;
    }

    public void setPreferredGenre(String preferredGenre) {
        this.preferredGenre = preferredGenre;
    }

}
