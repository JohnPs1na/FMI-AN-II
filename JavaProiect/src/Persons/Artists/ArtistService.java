package Persons.Artists;

import Persons.Clients.Client;
import Persons.Person;
import Persons.PersonFactory;
import option_function.*;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.util.logging.LoggingPermission;

public class ArtistService extends runMenu {

    static ArtistService artistService_instance = null;
    private final List<Person> artistList = new ArrayList<>();
    private PersonFactory personFactory = new PersonFactory();

    private ArtistService() {
        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("select * from artists");
            while (resultSet.next()) {
                artistList.add(personFactory.createPerson("ARTIST", resultSet));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        operations.add(
                new option_function(
                        "Add artist",
                        () -> {
                            Scanner in = new Scanner(System.in);
                            Person artist = personFactory.createPerson("ARTIST", in);
                            Artist a = (Artist) artist;
                            artistList.add(artist);
                            create(a);
                        }));
        operations.add(
                new option_function(
                        "Delete artist",
                        () -> {
                            for (Person artist : artistList) {
                                Artist a = (Artist) artist;
                                if (a.getArtistId() == 0) {
                                    continue;
                                }
                                System.out.println(artist);
                            }

                            System.out.println("Insert the id of artist you want to remove:");
                            Scanner in = new Scanner(System.in);
                            int id = Integer.parseInt(in.nextLine());

                            for (Person artist : artistList){
                                Artist a = (Artist) artist;
                                if (a.getArtistId() == id){
                                    artistList.remove(artist);
                                    deleteArtistById(id);
                                    break;
                                }
                            }
                        }));

        operations.add(new option_function(
                "Get All Artists",
                () -> {
                    for (Person artist : artistList) {
                        Artist a = (Artist) artist;
                        if (a.getArtistId() == 0) {
                            continue;
                        }
                        System.out.println(artist);
                    }
                }));


    }


    public void create(Artist artist) {
        try {
            String q = "Insert into artists (artistId, firstname,lastname,birthDate,phoneNumber,city,genre,balance) values (?,?,?,?,?,?,?,?)";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setInt(1, artist.getArtistId());
            stmt.setString(2, artist.getFirstName());
            stmt.setString(3, artist.getLastName());
            stmt.setString(4, artist.getBirthDate());
            stmt.setString(5, artist.getPhoneNumber());
            stmt.setString(6, artist.getCity());
            stmt.setString(7, artist.getGenre());
            stmt.setInt(8, artist.getBalance());
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void deleteArtistById(int id){
        try {
            String q = "delete from artists where artistId = ?";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setInt(1,id);
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public static ArtistService getInstance() {
        if (artistService_instance == null) {
            artistService_instance = new ArtistService();
        }
        return artistService_instance;
    }
}

