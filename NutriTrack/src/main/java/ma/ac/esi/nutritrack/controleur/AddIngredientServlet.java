package ma.ac.esi.nutritrack.controleur;

import ma.ac.esi.nutritrack.model.Ingredient;
import ma.ac.esi.nutritrack.repository.IngredientRepository;
import ma.ac.esi.nutritrack.repository.MealRepository;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/addIngredient")
public class AddIngredientServlet extends HttpServlet {
    private IngredientRepository ingredientRepository;
    private MealRepository mealRepository;

    @Override
    public void init() throws ServletException {
        ingredientRepository = new IngredientRepository();
        mealRepository = new MealRepository();
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        // Récupérer les paramètres du formulaire
        String mealName = request.getParameter("meal");
        String ingredientName = request.getParameter("ingredientName");
        int calories = Integer.parseInt(request.getParameter("calories"));

        try {
            // Créer un nouvel ingrédient
            Ingredient ingredient = new Ingredient(0, ingredientName, calories);
            
            // Obtenir l'ID du repas à partir de son nom
            int mealId = mealRepository.getMealIdByName(mealName);
            
            if (mealId > 0) {
                // Ajouter l'ingrédient au repas
                boolean success = ingredientRepository.addIngredientToMeal(mealId, ingredient);
                
                if (success) {
                    // Rediriger vers la page des repas si l'ajout a réussi
                    response.sendRedirect("meals");
                } else {
                    // Rediriger vers une page d'erreur si l'ajout a échoué
                    response.sendRedirect("error.html");
                }
            } else {
                // Rediriger vers une page d'erreur si le repas n'existe pas
                response.sendRedirect("error.html");
            }
        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("error.html");
        }
    }
}
