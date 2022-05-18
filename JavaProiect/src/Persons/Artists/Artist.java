package Persons.Artists;

import Persons.Person;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Artist extends Person {

    protected String genre;
    protected int artistId;

    public Artist(int artistId,String firstName, String lastName, String birthDate, String phoneNumber, String city, String genre,String balance) {
        super(firstName, lastName, birthDate, phoneNumber, city,balance);
        this.genre = genre;
        this.artistId = artistId;
    }

    public Artist(int artistId,Scanner in){
        super();
        read(artistId,in);
    }

    public Artist(ResultSet in) throws SQLException {
        read(in);
    }

    public void read(ResultSet in) throws SQLException {
        super.read(in);
        this.artistId = Integer.parseInt(in.getString("artistId"));
        this.genre = in.getString("genre");
    }
    public void read(int id, Scanner in){
        super.read(in);
        this.artistId = id;
        System.out.println("Genre:");
        this.genre = in.nextLine();
    }


    public String getGenre() {
        return genre;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public int getArtistId() {
        return artistId;
    }

    public void setArtistId(int artistId) {
        this.artistId = artistId;
    }

    @Override
    public String toString() {
        return "Artist{" +
                "genre='" + genre + '\'' +
                ", artistId=" + artistId +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", birthDate='" + birthDate + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", city='" + city + '\'' +
                '}';
    }
}
