package option_function;

import Users.User;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Objects;
import java.util.Scanner;


public class runMenu{

    protected ArrayList operations = new ArrayList();
    protected static Connection connection;
    protected static User user = null;
    protected static AuditService auditService = null;

    public runMenu(){
        try {
            auditService = AuditService.getInstance();
            connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/proiect_pao", "root", "qwe123456");
        } catch (Exception e){
            e.printStackTrace();
        }
    }


    public void run(){

        boolean running = true;

        while (running){

            try{
                int op;

                System.out.println("==================================");
                System.out.println("Chose your operation");
                for(int i = 0;i<operations.size();i++){
                    option_function of = (option_function) operations.get(i);
                    System.out.println(Integer.toString(i+1) + ")" + of.getOption());
                }
                System.out.println(Integer.toString(operations.size() + 1) + ")" + "Close");
                System.out.println("==================================");

                Scanner in = new Scanner(System.in);
                op = Integer.parseInt(in.nextLine());

                if (op < 0 || op > operations.size() + 1){
                    throw new RuntimeException("Invalid Option");
                }

                if (op == operations.size() + 1){
                    running = false;
                    continue;
                }

                option_function final_of = (option_function) operations.get(op - 1);
                if(User.getUserInstance() != null || Objects.equals(final_of.getOption(), "LOG IN") || Objects.equals(final_of.getOption(), "REGISTER")) {
                    final_of.getFunction().function();
                    if (this.getClass().toString().equals("class MainService")){
                        continue;
                    }
                    auditService.register(final_of.getOption());
                } else {
                    System.out.println("You Have to be logged in");
                }

            } catch (Exception e){
                System.out.println("Error occured: " + e);
            }
        }

    }
}
