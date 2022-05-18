package Persons;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Scanner;

public class Person {
    protected String firstName;
    protected String lastName;
    protected String birthDate;
    protected String phoneNumber;
    protected String city;
    protected int balance;

    public Person(String firstName, String lastName, String birthDate, String phoneNumber, String city, String balance) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.birthDate = birthDate;
        this.phoneNumber = phoneNumber;
        this.city = city;
        this.balance = Integer.parseInt(balance);
    }

    public Person(){
        this.balance = 0;
    }


    public void read(ResultSet in) throws SQLException {
        this.firstName = in.getString("firstName");
        this.lastName = in.getString("lastName");
        this.birthDate = in.getString("birthDate");
        this.phoneNumber = in.getString("phoneNumber");
        this.city = in.getString("city");
        this.balance = Integer.parseInt(in.getString("balance"));
    }

    public void read(Scanner in){
        System.out.println("First Name:");
        this.firstName = in.nextLine();
        System.out.println("Last Name:");
        this.lastName = in.nextLine();
        System.out.println("Birth Date:");
        this.birthDate = in.nextLine();
        System.out.println("Phone Number:");
        this.phoneNumber = in.nextLine();
        System.out.println("City:");
        this.city = in.nextLine();
        System.out.println("Balance:");
        this.balance = Integer.parseInt(in.nextLine());
    }

    public void fillBalance(int money){
        this.balance+=money;
    }
    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getBirthDate() {
        return birthDate;
    }

    public void setBirthDate(String birthDate) {
        this.birthDate = birthDate;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getCity() {
        return city;
    }

    public void setCity(String city) {
        this.city = city;
    }

    public void setBalance(int balance){this.balance = balance;}

    public int getBalance(){return balance;}

    public int getClientId() {
        return 0;
    }

    @Override
    public String toString() {
        return "Person{" +
                "firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", birthDate='" + birthDate + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", city='" + city + '\'' +
                ", balance=" + balance +
                '}';
    }
}
