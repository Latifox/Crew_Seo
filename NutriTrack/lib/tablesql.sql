-- Enable the pgcrypto extension for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Table of users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Table of meals
CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table of ingredients
CREATE TABLE ingredients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    calories INT NOT NULL,
    meal_id INT,
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE
);

-- Insert an admin user with a hashed password
INSERT INTO users (email, password) 
VALUES ('admin@esi.ac.ma', crypt('admin', gen_salt('bf')));

-- Insert meals
INSERT INTO meals (name) VALUES 
('Breakfast'), 
('Lunch'), 
('Snacks'), 
('Dinner');

-- Insert ingredients associated with meals
INSERT INTO ingredients (name, calories, meal_id) VALUES 

('Bread', 130, (SELECT id FROM meals WHERE name = 'Breakfast')), 
('Egg', 155, (SELECT id FROM meals WHERE name = 'Breakfast')), 
('Cheese', 402, (SELECT id FROM meals WHERE name = 'Breakfast')),


('Lettuce', 2, (SELECT id FROM meals WHERE name = 'Lunch')), 
('Tomato', 18, (SELECT id FROM meals WHERE name = 'Lunch')), 
('Mais', 86, (SELECT id FROM meals WHERE name = 'Lunch')),

('Apple', 52, (SELECT id FROM meals WHERE name = 'Snacks')), 
('Hummus Rice Cake', 166, (SELECT id FROM meals WHERE name = 'Snacks')), 
('Carrot', 88, (SELECT id FROM meals WHERE name = 'Snacks')),


('Sweet Potato', 86, (SELECT id FROM meals WHERE name = 'Dinner')), 
('Spinach', 23, (SELECT id FROM meals WHERE name = 'Dinner')), 
('Arugula Cookies', 120, (SELECT id FROM meals WHERE name = 'Dinner'));
