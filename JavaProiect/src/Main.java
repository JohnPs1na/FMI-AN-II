import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class Main {

    public static void main(String[] args) {
        MainService mainServiceInstance = MainService.getInstance();
        mainServiceInstance.run();
    }
}