package Persons.Clients;

import Events.Event;
import Events.EventsService;
import Persons.Artists.ArtistService;
import Persons.Person;
import Persons.PersonFactory;
import Tickets.Ticket;
import Tickets.TicketService;
import Users.User;
import option_function.option_function;
import option_function.runMenu;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class ClientService extends runMenu {

    static ClientService clientService_instance = null;
    private final HashMap<Integer,Person> clientList = new HashMap<>();
    private PersonFactory personFactory = new PersonFactory();

    private ClientService(){
        try {
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery("select * from clients");
            while(resultSet.next()){
                Person client = personFactory.createPerson("CLIENT",resultSet);
                Client c = (Client) client;
                clientList.put(c.getClientId(),client);
            }
        } catch (Exception e){
            e.printStackTrace();
        }
        operations.add(
                new option_function(
                        "Add Client",
                        ()-> {
                            Scanner in = new Scanner(System.in);
                            Person client = personFactory.createPerson("CLIENT",in);
                            Client c = (Client) client;
                            clientList.put(c.getClientId(),client);
                            create((Client) client);
                        }));
        operations.add(
                new option_function(
                        "Fill Balance",
                        ()-> {
                            Scanner in = new Scanner(System.in);
                            System.out.println("Insert Money (int)");
                            int money = Integer.parseInt(in.nextLine());
                            for(int i = 0;i<clientList.size();i++){
                                Client p = (Client) clientList.get(i);
                                if (p.getClientId() == user.getClientId()){
                                    clientList.get(i).fillBalance(money);
                                    try {
                                        Statement statement = connection.createStatement();
                                        update((Client) clientList.get(i));
                                    } catch (SQLException e) {
                                        e.printStackTrace();
                                    }
                                }
                            }
                        }));
        operations.add(
                new option_function(
                        "Purchase Ticket",
                        ()-> {
                            TicketService ticketService = TicketService.getInstance();
                            EventsService eventsService = EventsService.getInstance();
                            ticketService.showTickets();

                            Scanner in = new Scanner(System.in);
                            System.out.println("Insert id of the ticket you want to purchase");
                            int ticketId = Integer.parseInt(in.nextLine());

                            Ticket t = ticketService.getTicketById(ticketId);
                            int eventId = t.getEventId();

                            Event e = eventsService.getEventByIdFromHashMap(eventId);

                            System.out.println("Insert how many tickets you want to purchase");
                            int ticketToPurchase = Integer.parseInt(in.nextLine());

                            Client c = (Client) clientList.get(user.getClientId());
                            int total = ticketToPurchase * t.getIntCost();

                            if (e.getTicketNum() == 0){
                                System.out.println("All tickets have been sold out");
                            }
                            else if(total > c.getBalance()){
                                System.out.println("You dont have enough money");
                            }
                            else {
                                eventsService.updateEventTicketNum(ticketToPurchase,eventId);
                                c.setBalance(c.getBalance() - total);
                                update(c);
                            }
                        }));

        operations.add(new option_function(
                "Delete Client",
                ()-> {
                    for(Person client : clientList.values()){
                        if (client.getClientId() == 0){
                            continue;
                        }
                        System.out.println(client);
                    }

                    Scanner in = new Scanner(System.in);
                    System.out.println("Insert id of the client you want to delete");
                    int id = Integer.parseInt(in.nextLine());
                    for(int i : clientList.keySet()){
                        Client c = (Client) clientList.get(i);
                        if (c.getClientId() == id){
                            clientList.remove(i);
                            deleteById(id);
                            break;
                        }
                    }
                }));

        operations.add(new option_function(
                "View Balance",
                ()-> {
                    User user = User.getUserInstance();
                    for (Person client : clientList.values()){
                        if (((Client) client).getClientId() == user.getClientId()){
                            System.out.println("You have "+ client.getBalance()+ " lei");
                        }
                    }
                }));

        operations.add(new option_function(
                "Get All Clients",
                ()-> {
                    for(Person client : clientList.values()){
                        if (client.getClientId() == 0){
                            continue;
                        }
                        System.out.println(client);
                    }
                }));
    }

    public Person registerClient(Scanner in){
        Person client = personFactory.createPerson("CLIENT",in);
        clientList.put(client.getClientId(),client);
        create((Client) client);
        return client;
    }

    public void create(Client client){
        try{
            String q = "Insert into clients (clientId, firstname,lastname,birthDate,phoneNumber,city,preferredGenre,balance) values (?,?,?,?,?,?,?,?)";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setInt(1,client.getClientId());
            stmt.setString(2,client.getFirstName());
            stmt.setString(3,client.getLastName());
            stmt.setString(4, client.getBirthDate());
            stmt.setString(5,client.getPhoneNumber());
            stmt.setString(6,client.getCity());
            stmt.setString(7,client.getPreferredGenre());
            stmt.setInt(8,client.getBalance());
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    public void update(Client client){
        try{
            String q = "Update clients SET firstname = ?, lastName = ?, birthDate = ?, phoneNumber = ?, city = ?,preferredGenre = ?,balance = ? where clientId = ?";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setString(1,client.getFirstName());
            stmt.setString(2,client.getLastName());
            stmt.setString(3,client.getBirthDate());
            stmt.setString(4,client.getPhoneNumber());
            stmt.setString(5,client.getCity());
            stmt.setString(6,client.getPreferredGenre());
            stmt.setInt(7,client.getBalance());
            stmt.setInt(8,client.getClientId());
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }

    public void deleteById(int clientId){
        try{
            String q = "Delete from clients where clientId = ?";
            PreparedStatement stmt = connection.prepareStatement(q);
            stmt.setInt(1,clientId);
            stmt.executeUpdate();
            stmt.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    public static ClientService getInstance(){
        if (clientService_instance == null){
            clientService_instance = new ClientService();
        }
        return clientService_instance;
    }
}
