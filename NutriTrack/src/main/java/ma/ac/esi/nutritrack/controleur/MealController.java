package ma.ac.esi.nutritrack.controleur;

import ma.ac.esi.nutritrack.model.Meal;
import ma.ac.esi.nutritrack.repository.MealRepository;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@WebServlet("/meals")
public class MealController extends HttpServlet {
    private MealRepository mealRepository;

    @Override
    public void init() throws ServletException {
        // Initialize the repository in the init method
        mealRepository = new MealRepository();
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Fetch meals from the repository
        List<Meal> meals = mealRepository.getAllMeals();



        // Set the list of meals as an attribute on the request
        request.setAttribute("meals", meals);

        // Forward the request to the JSP page to display the meals
        request.getRequestDispatcher("/home.jsp").forward(request, response);
    }
}