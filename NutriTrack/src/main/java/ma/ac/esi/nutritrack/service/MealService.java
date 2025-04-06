package ma.ac.esi.nutritrack.service;

import ma.ac.esi.nutritrack.model.Meal;
import ma.ac.esi.nutritrack.repository.MealRepository;

import java.util.List;

public class MealService {
    private final MealRepository mealRepository;

    public MealService() {
        this.mealRepository = new MealRepository();
    }

    public List<Meal> getAllMeals() {
        return mealRepository.getAllMeals();
    }
}