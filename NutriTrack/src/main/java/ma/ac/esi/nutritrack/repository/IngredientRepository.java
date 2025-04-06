package ma.ac.esi.nutritrack.repository;

import ma.ac.esi.nutritrack.model.Ingredient;
import ma.ac.esi.nutritrack.util.DBUtil;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class IngredientRepository {
    
    /**
     * Ajoute un nouvel ingrédient à un repas spécifique
     * @param mealId L'ID du repas auquel ajouter l'ingrédient
     * @param ingredient L'ingrédient à ajouter
     * @return true si l'ajout a réussi, false sinon
     */
    public boolean addIngredientToMeal(int mealId, Ingredient ingredient) {
        String sql = "INSERT INTO ingredients (name, calories, meal_id) VALUES (?, ?, ?)";
        
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, ingredient.getName());
            pstmt.setInt(2, ingredient.getCalories());
            pstmt.setInt(3, mealId);
            
            int rowsAffected = pstmt.executeUpdate();
            return rowsAffected > 0;
            
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean updateIngredient(int mealId, Ingredient ingredient) {
        String sql = "UPDATE ingredients SET name = ?, calories = ? WHERE id = ? AND meal_id = ?";
        
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setString(1, ingredient.getName());
            pstmt.setInt(2, ingredient.getCalories());
            pstmt.setInt(3, ingredient.getId());
            pstmt.setInt(4, mealId);
            
            int rowsAffected = pstmt.executeUpdate();
            return rowsAffected > 0;
            
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean deleteIngredient(int ingredientId, int mealId) {
        String sql = "DELETE FROM ingredients WHERE id = ? AND meal_id = ?";
        
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, ingredientId);
            pstmt.setInt(2, mealId);
            
            int rowsAffected = pstmt.executeUpdate();
            return rowsAffected > 0;
            
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }
}
