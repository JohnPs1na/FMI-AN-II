package Persons;

import Persons.Artists.Artist;
import Persons.Clients.Client;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class PersonFactory {

    private int artistId = 0;
    private int clientId = 0;

    public Person createPerson(String personType, Scanner in){

        if (personType == null)
            return null;

        if (personType.equalsIgnoreCase("ARTIST")){
            return new Artist(artistId++,in);
        }

        if (personType.equalsIgnoreCase("CLIENT")){
            return new Client(clientId++,in);
        }
        return null;
    }

    public Person createPerson(String personType, ResultSet in) throws SQLException {

        if (personType == null)
            return null;

        if (personType.equalsIgnoreCase("ARTIST")){
            ++artistId;
            return new Artist(in);
        }

        if (personType.equalsIgnoreCase("CLIENT")){
            ++clientId;
            return new Client(in);
        }
        return null;
    }

}
