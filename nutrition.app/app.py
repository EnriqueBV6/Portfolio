from flask import Flask, render_template, request
import os
from services.calories import plot_calories
from services.data_gen import generate_nutrition_data
from services.protein import plot_protein
from models.user_profile import UserProfile
from services.metabolic_service import calculate_metabolic_profile
from services.nutrition_service import calculate_nutritional_profile
from services.recommendation_engine import generate_complete_recommendation
from models.calculation_result import CompleteAnalysis

app = Flask(__name__)

# Configure encoding
app.config['JSON_AS_ASCII'] = False

@app.route("/", methods=["GET", "POST"])
def index():
    image = None
    analysis = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "analyze":
            # Get form data
            try:
                weight = float(request.form.get("weight", 0))
                height = float(request.form.get("height", 0))
                age = int(request.form.get("age", 0))
                sex = request.form.get("sex", "male")
                activity_level = request.form.get("activity_level", "moderate")
                goal = request.form.get("goal", "maintenance")
                current_calories = float(request.form.get("current_calories", 0))
                training_calories = float(request.form.get("training_calories", 0))
                
                # Create user profile
                user_profile = UserProfile(
                    weight=weight,
                    height=height,
                    age=age,
                    sex=sex,
                    activity_level=activity_level,
                    goal=goal
                )
                
                # Calculate metabolic profile
                metabolic_result = calculate_metabolic_profile(user_profile)
                
                # Calculate nutritional profile
                nutritional_result = calculate_nutritional_profile(
                    user_profile=user_profile,
                    metabolic_result=metabolic_result,
                    current_calories=current_calories,
                    training_calories=training_calories
                )
                
                # Generate recommendations
                recommendation_result = generate_complete_recommendation(
                    user_profile=user_profile,
                    metabolic_result=metabolic_result,
                    nutritional_result=nutritional_result
                )
                
                # Create complete analysis
                analysis = CompleteAnalysis(
                    user_profile=user_profile,
                    metabolic=metabolic_result,
                    nutritional=nutritional_result,
                    recommendation=recommendation_result
                )
                
            except (ValueError, TypeError) as e:
                # Handle form validation errors
                pass  # Could add error message to template
                
        elif action in ["calories", "protein"]:
            # Legacy functionality for charts
            days = int(request.form.get("days", 7))
            df = generate_nutrition_data(days)
            
            if action == "calories":
                image = plot_calories(df)
            elif action == "protein":
                image = plot_protein(df)
    
    return render_template("index.html", image=image, analysis=analysis)


if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)