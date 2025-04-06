package ma.ac.esi.nutritrack.service;

import ma.ac.esi.nutritrack.model.Ingredient;
import ma.ac.esi.nutritrack.repository.IngredientRepository;

public class IngredientService {
    private final IngredientRepository ingredientRepository;

    public IngredientService() {
        this.ingredientRepository = new IngredientRepository();
    }

    public boolean addIngredientToMeal(int mealId, String name, int calories) {
        try {
            // Créer un nouvel objet Ingredient
            Ingredient ingredient = new Ingredient(0, name, calories);
            
            // Appeler la méthode du repository pour ajouter l'ingrédient
            return ingredientRepository.addIngredientToMeal(mealId, ingredient);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean updateIngredient(int ingredientId, int mealId, String name, int calories) {
        try {
            Ingredient ingredient = new Ingredient(ingredientId, name, calories);
            return ingredientRepository.updateIngredient(mealId, ingredient);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean deleteIngredient(int ingredientId, int mealId) {
        try {
            return ingredientRepository.deleteIngredient(ingredientId, mealId);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
} 