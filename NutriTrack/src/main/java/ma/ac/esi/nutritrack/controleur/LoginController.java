package ma.ac.esi.nutritrack.controleur;

import java.io.IOException;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import ma.ac.esi.nutritrack.service.UserService;

@WebServlet("/LoginController")
public class LoginController extends HttpServlet {
    private static final long serialVersionUID = 1L;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String login = request.getParameter("uname");
        String password = request.getParameter("psw");

        UserService userService = new UserService();

        if (userService.findUserByCredentials(login, password)) {
            response.sendRedirect("meals");
        } else {
            response.sendRedirect("error.html");

        }
    }
}