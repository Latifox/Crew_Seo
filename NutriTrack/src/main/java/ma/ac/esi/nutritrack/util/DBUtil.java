package ma.ac.esi.nutritrack.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;


public class DBUtil {

    private static final String URL = "jdbc:postgresql://ep-sweet-meadow-abfcmsjy-pooler.eu-west-2.aws.neon.tech/nutriwise-db?sslmode=require";
    private static final String USER = "nutriwise-db_owner";
    private static final String PASSWORD = "npg_z3BU5pdeShJK";


    public static Connection getConnection() {
        try {
            Class.forName("org.postgresql.Driver");

            return DriverManager.getConnection(URL, USER, PASSWORD);



        } catch (SQLException e) {
            System.err.println("Erreur lors de la connexion à la base de données !");
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        return null;
    }


}