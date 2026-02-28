from flask import Flask, render_template, request
import os
from services.calories import plot_calories
from services.data_gen import generate_nutrition_data
from services.protein import plot_protein
from models.user_profile import UserProfile
from models.body_composition import BodyComposition
from services.body_composition_service import generate_body_composition_result
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
                    goal=goal,
                    metabolic_equation="mifflin_st_jeor"  # Default equation
                )
                
                # NUEVO: Extraer datos de body composition si existen
                body_fat_percentage = request.form.get("body_fat_percentage")
                body_composition = None
                body_composition_result = None
                
                if body_fat_percentage:
                    try:
                        body_composition = BodyComposition(
                            body_fat_percentage=float(body_fat_percentage),
                            circumference_biceps=float(request.form.get("circumference_biceps")) 
                                                if request.form.get("circumference_biceps") else None,
                            circumference_chest=float(request.form.get("circumference_chest"))
                                               if request.form.get("circumference_chest") else None,
                            circumference_waist=float(request.form.get("circumference_waist"))
                                               if request.form.get("circumference_waist") else None,
                            circumference_hip=float(request.form.get("circumference_hip"))
                                             if request.form.get("circumference_hip") else None,
                            circumference_thigh=float(request.form.get("circumference_thigh"))
                                               if request.form.get("circumference_thigh") else None,
                        )
                        user_profile.body_composition = body_composition
                        
                        # Calcular resultados de composición corporal
                        body_composition_result = generate_body_composition_result(
                            user_profile=user_profile,
                            body_composition=body_composition
                        )
                    except ValueError as e:
                        # Error en datos corporales - continuar sin ellos
                        body_composition = None
                        body_composition_result = None
                
                # Calcular perfil metabólico (MODIFICADO para pasar body_composition_result)
                metabolic_result = calculate_metabolic_profile(
                    user_profile=user_profile,
                    body_composition_result=body_composition_result
                )
                
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
                    nutritional_result=nutritional_result,
                    current_calories=current_calories,
                    body_composition_result=body_composition_result
                )
                
                # Create complete analysis (MODIFICADO para incluir body_composition_result)
                analysis = CompleteAnalysis(
                    user_profile=user_profile,
                    metabolic=metabolic_result,
                    nutritional=nutritional_result,
                    recommendation=recommendation_result
                )
                
                # NUEVO: Agregar body composition result al analysis
                analysis.body_composition = body_composition_result
                
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
    # Production-ready configuration for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)