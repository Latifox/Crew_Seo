package ma.ac.esi.nutritrack.controleur;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import ma.ac.esi.nutritrack.service.IngredientService;
import java.io.IOException;

@WebServlet("/IngredientController")
public class IngredientController extends HttpServlet {
    private static final long serialVersionUID = 1L;
    private IngredientService ingredientService;

    @Override
    public void init() throws ServletException {
        ingredientService = new IngredientService();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String action = request.getParameter("action");
        int mealId = Integer.parseInt(request.getParameter("mealId"));
        
        boolean success = false;
        
        if ("edit".equals(action)) {
            // Récupérer les paramètres pour la modification
            int ingredientId = Integer.parseInt(request.getParameter("ingredientId"));
            String ingredientName = request.getParameter("Nom de l'ingrédient");
            int calories = Integer.parseInt(request.getParameter("Nombre de Calories"));
            
            // Appeler le service pour modifier l'ingrédient
            success = ingredientService.updateIngredient(ingredientId, mealId, ingredientName, calories);
        } else if ("delete".equals(action)) {
            // Récupérer l'ID de l'ingrédient à supprimer
            int ingredientId = Integer.parseInt(request.getParameter("ingredientId"));
            
            // Appeler le service pour supprimer l'ingrédient
            success = ingredientService.deleteIngredient(ingredientId, mealId);
        }

        if (success) {
            // Rediriger vers MealController en cas de succès
            response.sendRedirect("meals");
        } else {
            // Rediriger vers la page d'erreur en cas d'échec
            response.sendRedirect("error.html");
        }
    }
} 