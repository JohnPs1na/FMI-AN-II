
import Events.Event;
import Events.EventsService;
import Persons.Artists.ArtistService;
import Persons.Clients.Client;
import Persons.Clients.ClientService;
import Persons.Person;
import Persons.PersonFactory;
import Tickets.Ticket;

import java.io.File;
import java.sql.*;
import java.util.*;

import Tickets.TicketService;
import Users.User;
import option_function.*;


public class MainService extends runMenu{

    static MainService MainService_instance = null;

    private ArtistService artistMenu;
    private ClientService clientMenu;
    private EventsService eventsMenu;
    private TicketService ticketMenu;

    private MainService(){
        System.out.println(this.getClass().toString());
        artistMenu = ArtistService.getInstance();
        clientMenu = ClientService.getInstance();
        eventsMenu = EventsService.getInstance();
        ticketMenu = TicketService.getInstance();

        operations.add(
                new option_function(
                        "Open Artists Menu",
                        ()-> {
                            System.out.println("intru la artisti in menu");
                            artistMenu.run();
                        }));
        operations.add(
                new option_function(
                        "Open Clients Menu",
                        ()-> {
                            System.out.println("intru la Clienti in menu");
                            clientMenu.run();
                        }));
        operations.add(
                new option_function(
                        "Open Tickets Menu",
                        ()-> {
                            System.out.println("intru la Bilete in menu");
                            ticketMenu.run();
                        }));
        operations.add(
                new option_function(
                        "Open Events Menu",
                        ()-> {
                            System.out.println("intru la Events in menu");
                            eventsMenu.run();
                        }));

        operations.add(
                new option_function(
                        "REGISTER",
                        () -> {
                            Scanner in = new Scanner(System.in);
                            ClientService clientService = ClientService.getInstance();
                            Person client = clientService.registerClient(in);

                            System.out.println("insert login: ");
                            String username = in.nextLine();
                            System.out.println("insert password: ");
                            String password = in.nextLine();
                            System.out.println("confirm password: ");
                            String confirmed= in.nextLine();

                            if (!Objects.equals(password, confirmed)){
                                System.out.println("passwords do not match!");
                                while (!Objects.equals(password, confirmed)){
                                    System.out.println("confirm password: ");
                                    confirmed= in.nextLine();
                                }
                            }

                            try{
                                Statement statement = connection.createStatement();
                                ResultSet resultSet = statement.executeQuery("select max(userId) as 'id' from users");
                                resultSet.next();
                                int id = Integer.parseInt(resultSet.getString("id")) + 1;

                                String query = "insert into users (userId,artistId,clientId,username,password,label) values (?,?,?,?,?,?)";
                                PreparedStatement stmt = connection.prepareStatement(query);
                                stmt.setInt(1,id);
                                stmt.setInt(2,0);
                                stmt.setInt(3,client.getClientId());
                                stmt.setString(4,username);
                                stmt.setString(5,password);
                                stmt.setString(6,"client");
                                stmt.executeUpdate();
                                stmt.close();
                                statement.close();

                            } catch (Exception e){
                                e.printStackTrace();
                            }
                        }));
        operations.add(
                new option_function(
                        "LOG IN",
                        () -> {
                            Scanner in = new Scanner(System.in);
                            System.out.println("Login:");
                            String username = in.nextLine();
                            System.out.println("Password:");
                            String password = in.nextLine();
                            try {
                                Statement statement = connection.createStatement();
                                ResultSet resultSet = statement.executeQuery("select * from users");
                                while(resultSet.next()){
                                    if (Objects.equals(resultSet.getString("username"), username) &&
                                            Objects.equals(resultSet.getString("password"),password)){
                                        user = User.getUserInstance(
                                                username,
                                                password,
                                                resultSet.getString("label"),
                                                Integer.parseInt(resultSet.getString("clientId")),
                                                Integer.parseInt(resultSet.getString("artistId")),
                                                Integer.parseInt(resultSet.getString("userId")));
                                    }
                                }
                                statement.close();
                            } catch (Exception e){
                                e.printStackTrace();
                            }
                            if (user != null) {
                                System.out.println("LOGGED IN AS " + user.getUsername() + " " + user.getLabel());
                            } else {
                                System.out.println("FAILED TO LOG IN TRY AGAIN");
                            }

                        }));

        operations.add(
                new option_function(
                        "LOG OUT",
                        ()-> {
                            System.out.println("Logged out");
                            User.deleteInstance();
                        }));

    }

    public static MainService getInstance(){
        if (MainService_instance == null){
            MainService_instance = new MainService();
        }
        return MainService_instance;
    }

}
