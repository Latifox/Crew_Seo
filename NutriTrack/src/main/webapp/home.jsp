<%@ page language="java" contentType="text/html; charset=UTF-8"
         pageEncoding="UTF-8"%>
<%@ page import="java.util.List" %>
<%@ page import="ma.ac.esi.nutritrack.model.Meal" %>
<%@ page import="ma.ac.esi.nutritrack.model.Ingredient" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meal Plan - Gain Weight</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .sidebar { height: 100vh; background-color: #2c2c54; color: white; padding-top: 20px; }
        .sidebar a { color: white; display: block; padding: 15px; text-decoration: none; text-align: center; }
        .sidebar a:hover { background-color: #57577d; }
        .meal-card { border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .kcal-box { background-color: #fff; padding: 20px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .meal-item { border-radius: 10px; background-color: #fff; padding: 10px; margin-bottom: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: relative; }
        .meal-item img { width: 40px; height: 40px; display: block; margin: 0 auto 5px; }
        .ingredient-actions { position: absolute; top: 5px; right: 5px; }
        .ingredient-actions i { margin-left: 5px; cursor: pointer; }
        .ingredient-actions i.bi-pencil { color: #0d6efd; }
        .ingredient-actions i.bi-trash { color: #dc3545; }
    </style>
</head>
<body>
<div class="container-fluid">
    <div class="row">
        <!-- Sidebar -->
        <div class="col-md-2 sidebar d-flex flex-column align-items-center" style="overflow-y: auto; position: sticky; top: 0;">
            <div class="py-2">
                <a href="#"><i class="bi bi-grid"></i></a>
                <a href="#"><i class="bi bi-search"></i></a>
                <a href="#"><i class="bi bi-people"></i></a>
                <a href="#"><i class="bi bi-star"></i></a>
                <a href="#"><i class="bi bi-calendar"></i></a>
                <a href="#"><i class="bi bi-check-square"></i></a>
                <a href="#"><i class="bi bi-chat"></i></a>
                <a href="#"><i class="bi bi-envelope"></i></a>
            </div>
        </div>

        <!-- Main Content -->
        <div class="col-md-10 p-4">
            <!-- Ajout du header avec le bouton -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><strong>Meal plans</strong> / Gain weight</h2>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addIngredientModal">
                    + Ajouter un ingrédient
                </button>
            </div>

            <!-- Modal pour ajouter un ingrédient -->
            <div class="modal fade" id="addIngredientModal" tabindex="-1" aria-labelledby="addIngredientModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="addIngredientModalLabel">Ajouter un nouvel ingrédient</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form action="addIngredient" method="POST">
                                <div class="mb-3">
                                    <label for="meal" class="form-label">Repas</label>
                                    <select class="form-select" id="meal" name="meal" required>
                                        <option value="Breakfast">Breakfast</option>
                                        <option value="Lunch">Lunch</option>
                                        <option value="Snacks">Snacks</option>
                                        <option value="Dinner">Dinner</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label for="ingredientName" class="form-label">Nom de l'ingrédient</label>
                                    <input type="text" class="form-control" id="ingredientName" name="ingredientName" required>
                                </div>
                                <div class="mb-3">
                                    <label for="calories" class="form-label">Calories</label>
                                    <input type="number" class="form-control" id="calories" name="calories" required>
                                </div>
                                <button type="submit" class="btn btn-success">Ajouter</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row my-4">
                <div class="col-md-6">
                    <img src="img/Meal.jpg" style="width:90px; height:90px;border-radius:10px;" alt="Meal Image">
                </div>
                <div class="col-md-6 kcal-box">
                    <h3><strong>823 kcal</strong></h3>
                    <div class="progress my-3">
                        <div class="progress-bar" role="progressbar" style="width: 60%" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <p><i class="bi bi-fire"></i> 283 kcal burned</p>
                </div>
            </div>

            <!-- Dynamic Meal Sections -->
            <div class="row">
                <%
                    List<Meal> meals = (List<Meal>) request.getAttribute("meals");
                    if (meals != null && !meals.isEmpty()) {
                        for (Meal meal : meals) {
                %>
                <div class="col-md-3">
                    <h5><%= meal.getName() %></h5>
                    <%
                        List<Ingredient> ingredients = meal.getIngredients();
                        for (Ingredient ingredient : ingredients) {
                    %>
                    <div class="meal-item">
                        <div class="ingredient-actions">
                            <i class="bi bi-pencil" onclick="openEditModal(<%= meal.getId() %>, <%= ingredient.getId() %>, '<%= ingredient.getName() %>', <%= ingredient.getCalories() %>)"></i>
                            <i class="bi bi-trash" onclick="confirmDelete(<%= meal.getId() %>, <%= ingredient.getId() %>)"></i>
                        </div>
                        <img src="img/<%= ingredient.getName().replaceAll(" ", "") %>.jpg" alt="<%= ingredient.getName() %>">
                        <%= ingredient.getName() %><br>
                        <small><%= ingredient.getCalories() %> kcal</small>
                    </div>
                    <% } %>
                </div>
                <%
                    }
                } else {
                %>
                <p>No meals found in the database.</p>
                <% } %>
            </div>
        </div>
    </div>
</div>

<!-- Modal pour modifier un ingrédient -->
<div class="modal fade" id="editIngredientModal" tabindex="-1" aria-labelledby="editIngredientModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="editIngredientModalLabel">Modifier l'ingrédient</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="editIngredientForm" action="IngredientController" method="POST">
                    <input type="hidden" id="editMealId" name="mealId">
                    <input type="hidden" id="editIngredientId" name="ingredientId">
                    <input type="hidden" name="action" value="edit">
                    <div class="mb-3">
                        <label for="editIngredientName" class="form-label">Nom de l'ingrédient</label>
                        <input type="text" class="form-control" id="editIngredientName" name="Nom de l'ingrédient" required>
                    </div>
                    <div class="mb-3">
                        <label for="editCalories" class="form-label">Calories</label>
                        <input type="number" class="form-control" id="editCalories" name="Nombre de Calories" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Sauvegarder</button>
                </form>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    // Fonction pour ouvrir le modal de modification
    function openEditModal(mealId, ingredientId, ingredientName, calories) {
        document.getElementById('editMealId').value = mealId;
        document.getElementById('editIngredientId').value = ingredientId;
        document.getElementById('editIngredientName').value = ingredientName;
        document.getElementById('editCalories').value = calories;
        
        new bootstrap.Modal(document.getElementById('editIngredientModal')).show();
    }

    // Fonction pour confirmer la suppression
    function confirmDelete(mealId, ingredientId) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cet ingrédient ?')) {
            // Créer un formulaire dynamique pour la suppression
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = 'IngredientController';

            const mealIdInput = document.createElement('input');
            mealIdInput.type = 'hidden';
            mealIdInput.name = 'mealId';
            mealIdInput.value = mealId;

            const ingredientIdInput = document.createElement('input');
            ingredientIdInput.type = 'hidden';
            ingredientIdInput.name = 'ingredientId';
            ingredientIdInput.value = ingredientId;

            const actionInput = document.createElement('input');
            actionInput.type = 'hidden';
            actionInput.name = 'action';
            actionInput.value = 'delete';

            form.appendChild(mealIdInput);
            form.appendChild(ingredientIdInput);
            form.appendChild(actionInput);
            document.body.appendChild(form);
            form.submit();
        }
    }
</script>
</body>
</html>