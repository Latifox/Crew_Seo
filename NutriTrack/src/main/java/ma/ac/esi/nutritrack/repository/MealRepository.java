package ma.ac.esi.nutritrack.repository;

import ma.ac.esi.nutritrack.model.Ingredient;
import ma.ac.esi.nutritrack.model.Meal;
import ma.ac.esi.nutritrack.util.DBUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class MealRepository {
    public List<Meal> getAllMeals() {
        List<Meal> meals = new ArrayList<>();
        String mealQuery = "SELECT * FROM meals";
        String ingredientQuery = "SELECT * FROM ingredients WHERE meal_id = ?";
        try (Connection connection= DBUtil.getConnection();
             PreparedStatement mealStmt = connection.prepareStatement(mealQuery);
             ResultSet mealRs = mealStmt.executeQuery()) {
            while (mealRs.next()) {
                int mealId = mealRs.getInt("id");
                String mealName = mealRs.getString("name");
                List<Ingredient> ingredients = new ArrayList<>();
                try (PreparedStatement ingStmt = connection.prepareStatement(ingredientQuery))
                {
                    ingStmt.setInt(1, mealId);
                    ResultSet ingRs = ingStmt.executeQuery();
                    while (ingRs.next()) {
                        ingredients.add(new Ingredient(
                                ingRs.getInt("id"),
                                ingRs.getString("name"),
                                ingRs.getInt("calories")
                        ));
                    }
                }
                meals.add(new Meal(mealId, mealName, ingredients));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return meals;
    }

    public void addIngredient(Ingredient ingredient, String mealName) {
        String sql = "INSERT INTO ingredients (name, calories, meal_id) VALUES (?, ?, (SELECT id FROM meals WHERE name = ?))";
        try (Connection connection = DBUtil.getConnection();
             PreparedStatement stmt = connection.prepareStatement(sql)) {
            
            stmt.setString(1, ingredient.getName());
            stmt.setInt(2, ingredient.getCalories());
            stmt.setString(3, mealName);
            
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("Error adding ingredient", e);
        }
    }

    public int getMealIdByName(String mealName) {
        String sql = "SELECT id FROM meals WHERE name = ?";
        try (Connection connection = DBUtil.getConnection();
             PreparedStatement stmt = connection.prepareStatement(sql)) {
            
            stmt.setString(1, mealName);
            ResultSet rs = stmt.executeQuery();
            
            if (rs.next()) {
                return rs.getInt("id");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return -1; // Retourne -1 si le repas n'est pas trouvé
    }
}