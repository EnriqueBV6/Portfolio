"""
Recommendation engine for Nutrition & Training Planner.

This module provides functions for generating personalized nutritional
recommendations based on user's metabolic and nutritional data.
Updated with scientific evidence (2015-2025).
"""

from typing import Literal

from models.user_profile import UserProfile
from models.calculation_result import MetabolicResult, NutritionalResult, RecommendationResult
from utils.constants import METABOLIC_EQUATIONS, EDUCATIONAL_MESSAGES


def generate_recommendation(
    balance: float,
    goal: Literal["deficit", "maintenance", "bulk"],
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool
) -> str:
    """
    Generate personalized nutritional recommendation.
    
    Args:
        balance: Current energy balance
        goal: User's goal
        metabolic_result: Metabolic calculation results
        nutritional_result: Nutritional calculation results
        has_current_calories: Whether user provided current calorie intake
        
    Returns:
        Personalized recommendation text
    """
    if goal == "deficit":
        return generate_deficit_recommendation(balance, metabolic_result, nutritional_result, has_current_calories)
    elif goal == "bulk":
        return generate_bulk_recommendation(balance, metabolic_result, nutritional_result, has_current_calories)
    else:
        return generate_maintenance_recommendation(balance, metabolic_result, nutritional_result, has_current_calories)


def generate_deficit_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool
) -> str:
    """Generate recommendation for fat loss goal."""
    
    if not has_current_calories:
        recommendation = (
            f"Tu TDEE (gasto energético total) es de {metabolic_result.tdee:.0f} kcal diarias. "
            f"Para pérdida de grasa sostenible, te recomiendo consumir {nutritional_result.target_calories:.0f} kcal diarias. "
            f"Esto representa un déficit de {metabolic_result.tdee - nutritional_result.target_calories:.0f} kcal, "
            "que es óptimo para perder grasa sin sacrificar masa muscular."
        )
    elif balance < -500:
        recommendation = (
            f"Tu consumo actual te pone en un déficit de {abs(balance):.0f} calorías por debajo de tu gasto. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este nivel de déficit es muy agresivo y puede llevar a pérdida de masa muscular. "
            f"Te recomiendo aumentar a {nutritional_result.target_calories:.0f} kcal diarias "
            "para una pérdida de grasa más sostenible y saludable."
        )
    elif balance < -200:
        recommendation = (
            f"Tu consumo actual te pone en un déficit de {abs(balance):.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este es un buen nivel para pérdida de grasa. "
            f"Tu objetivo de {nutritional_result.target_calories:.0f} kcal es apropiado."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:+.0f} calorías no es suficiente para pérdida de grasa. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            f"Para tu objetivo de déficit, deberías consumir {nutritional_result.target_calories:.0f} kcal diarias."
        )
    
    recommendation += (
        f"\n\nDistribución de macronutrientes recomendada:"
        f"\n• Proteína: {nutritional_result.macro_split['protein']:.1f}g "
        f"({nutritional_result.macro_percentages['protein']:.1f}%)"
        f"\n• Grasas: {nutritional_result.macro_split['fat']:.1f}g "
        f"({nutritional_result.macro_percentages['fat']:.1f}%)"
        f"\n• Carbohidratos: {nutritional_result.macro_split['carbs']:.1f}g "
        f"({nutritional_result.macro_percentages['carbs']:.1f}%)"
    )
    
    return recommendation


def generate_bulk_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool
) -> str:
    """Generate recommendation for muscle gain goal."""
    
    if not has_current_calories:
        recommendation = (
            f"Tu TDEE (gasto energético total) es de {metabolic_result.tdee:.0f} kcal diarias. "
            f"Para ganancia muscular limpia, te recomiendo consumir {nutritional_result.target_calories:.0f} kcal diarias. "
            f"Esto representa un superávit de {nutritional_result.target_calories - metabolic_result.tdee:.0f} kcal, "
            "que es ideal para maximizar la ganancia muscular minimizando la acumulación de grasa."
        )
    elif balance > 500:
        recommendation = (
            f"Tu consumo actual te pone en un superávit de {balance:.0f} calorías por encima de tu gasto. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este nivel puede generar acumulación excesiva de grasa. "
            f"Te recomiendo reducir a {nutritional_result.target_calories:.0f} kcal diarias "
            "para ganancia muscular más limpia."
        )
    elif balance > 200:
        recommendation = (
            f"Tu consumo actual te pone en un superávit de {balance:.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este es un buen nivel para ganancia muscular. "
            f"Tu objetivo de {nutritional_result.target_calories:.0f} kcal es apropiado."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:+.0f} calorías no es suficiente para ganancia muscular. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            f"Para tu objetivo de volumen, deberías consumir {nutritional_result.target_calories:.0f} kcal diarias."
        )
    
    recommendation += (
        f"\n\nDistribución de macronutrientes recomendada:"
        f"\n• Proteína: {nutritional_result.macro_split['protein']:.1f}g "
        f"({nutritional_result.macro_percentages['protein']:.1f}%)"
        f"\n• Grasas: {nutritional_result.macro_split['fat']:.1f}g "
        f"({nutritional_result.macro_percentages['fat']:.1f}%)"
        f"\n• Carbohidratos: {nutritional_result.macro_split['carbs']:.1f}g "
        f"({nutritional_result.macro_percentages['carbs']:.1f}%)"
    )
    
    return recommendation


def generate_maintenance_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool
) -> str:
    """Generate recommendation for maintenance goal."""
    
    if not has_current_calories:
        recommendation = (
            f"Tu TDEE (gasto energético total) es de {metabolic_result.tdee:.0f} kcal diarias. "
            f"Para mantener tu peso actual, te recomiendo consumir {nutritional_result.target_calories:.0f} kcal diarias. "
            "Esto te permitirá mantener tu composición corporal actual."
        )
    elif abs(balance) <= 200:
        recommendation = (
            f"Excelente. Estás manteniendo tu peso con un balance de {balance:+.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            f"Tu consumo actual de {nutritional_result.target_calories:.0f} kcal es ideal para mantenimiento."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:+.0f} calorías te está alejando del mantenimiento. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            f"Para mantener tu peso, deberías consumir aproximadamente {nutritional_result.target_calories:.0f} kcal diarias."
        )
    
    recommendation += (
        f"\n\nDistribución de macronutrientes recomendada:"
        f"\n• Proteína: {nutritional_result.macro_split['protein']:.1f}g "
        f"({nutritional_result.macro_percentages['protein']:.1f}%)"
        f"\n• Grasas: {nutritional_result.macro_split['fat']:.1f}g "
        f"({nutritional_result.macro_percentages['fat']:.1f}%)"
        f"\n• Carbohidratos: {nutritional_result.macro_split['carbs']:.1f}g "
        f"({nutritional_result.macro_percentages['carbs']:.1f}%)"
    )
    
    return recommendation


def generate_actionable_steps(
    goal: Literal["deficit", "maintenance", "bulk"],
    nutritional_result: NutritionalResult,
    user_profile: UserProfile
) -> list[str]:
    """
    Generate actionable steps for the user.
    
    Args:
        goal: User's goal
        nutritional_result: Nutritional calculation results
        user_profile: User's profile
        
    Returns:
        List of actionable steps
    """
    steps = []
    
    # General steps
    steps.append(f"Consume {nutritional_result.target_calories:.0f} kcal diarias")
    steps.append(f"Consume {nutritional_result.macro_split['protein']:.1f}g de proteína diariamente")
    steps.append(f"Consume {nutritional_result.macro_split['fat']:.1f}g de grasas saludables diariamente")
    steps.append(f"Consume {nutritional_result.macro_split['carbs']:.1f}g de carbohidratos diariamente")
    
    # Goal-specific steps
    if goal == "deficit":
        steps.append("Monitorea tu peso semanalmente")
        steps.append("Ajusta calorías si pierdes más de 1kg por semana")
        steps.append("Prioriza proteína para preservar masa muscular")
    elif goal == "bulk":
        steps.append("Monitorea tu peso semanalmente")
        steps.append("Ajusta calorías si ganas más de 0.5kg por semana")
        steps.append("Asegura entrenamiento de fuerza progresivo")
    else:
        steps.append("Mantén consistencia en tu consumo calórico")
        steps.append("Ajusta según fluctuaciones de peso naturales")
    
    # Activity-specific steps
    if user_profile.activity_level in ["sedentary", "light"]:
        steps.append("Considera aumentar actividad física gradualmente")
    elif user_profile.activity_level in ["high", "very_high"]:
        steps.append("Asegura recuperación adecuada con alto nivel de actividad")
    
    return steps


def calculate_confidence_level(
    user_profile: UserProfile,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool
) -> float:
    """
    Calculate confidence level of recommendations based on scientific evidence.
    
    Args:
        user_profile: User's profile
        metabolic_result: Metabolic results
        nutritional_result: Nutritional results
        has_current_calories: Whether user provided current calorie intake
        
    Returns:
        Confidence level between 0 and 1
    """
    confidence = 0.7  # Base confidence for metabolic equations
    
    # Adjust based on equation accuracy
    equation_info = METABOLIC_EQUATIONS[user_profile.metabolic_equation]
    if user_profile.metabolic_equation == "mifflin_st_jeor":
        confidence += 0.1  # Most accurate for general population
    elif user_profile.metabolic_equation == "cunningham":
        confidence += 0.15  # Most accurate for athletes
    
    # Adjust based on profile completeness
    if 18 <= user_profile.age <= 65:
        confidence += 0.05  # Equations most accurate in this range
    
    bmi = user_profile.weight / ((user_profile.height / 100) ** 2)
    if 18.5 <= bmi <= 30:
        confidence += 0.05  # Equations more accurate in normal BMI range
    
    # Adjust based on activity level
    if user_profile.activity_level in ["light", "moderate", "high"]:
        confidence += 0.05  # Better accuracy with moderate activity
    
    # Adjust based on data availability
    if has_current_calories:
        confidence += 0.05  # More complete analysis
    
    return min(confidence, 1.0)


def generate_confidence_explanation(confidence_level: float, equation_used: str) -> str:
    """
    Generate explanation of confidence level for the user.
    
    Args:
        confidence_level: Calculated confidence level (0-1)
        equation_used: Which metabolic equation was used
        
    Returns:
        User-friendly explanation of confidence level
    """
    equation_info = METABOLIC_EQUATIONS[equation_used]
    
    if confidence_level >= 0.9:
        return (
            f"Confianza muy alta ({confidence_level*100:.0f}%). "
            f"Usando la ecuación {equation_info['name']}, que tiene una precisión de {equation_info['accuracy']}. "
            "Tu perfil completo permite recomendaciones muy precisas."
        )
    elif confidence_level >= 0.8:
        return (
            f"Confianza alta ({confidence_level*100:.0f}%). "
            f"Usando la ecuación {equation_info['name']}, que tiene una precisión de {equation_info['accuracy']}. "
            "Las recomendaciones son fiables pero pueden necesitar ajustes menores."
        )
    elif confidence_level >= 0.7:
        return (
            f"Confianza moderada ({confidence_level*100:.0f}%). "
            f"Usando la ecuación {equation_info['name']}. "
            "Las ecuaciones metabólicas tienen variabilidad individual. Monitoriza tus resultados y ajusta según sea necesario."
        )
    else:
        return (
            f"Confianza baja ({confidence_level*100:.0f}%). "
            "Tu perfil está fuera de los rangos óptimos para las ecuaciones metabólicas. "
            "Considera consultar con un profesional para recomendaciones personalizadas."
        )


def generate_educational_messages(goal: Literal["deficit", "maintenance", "bulk"]) -> list[str]:
    """
    Generate educational messages based on user's goal.
    
    Args:
        goal: User's goal
        
    Returns:
        List of educational messages
    """
    messages = EDUCATIONAL_MESSAGES["general"].copy()
    messages.extend(EDUCATIONAL_MESSAGES.get(goal, []))
    return messages


def generate_complete_recommendation(
    user_profile: UserProfile,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    current_calories: float = 0.0
) -> RecommendationResult:
    """
    Generate complete recommendation with actionable steps and confidence.
    
    Args:
        user_profile: User's profile
        metabolic_result: Metabolic results
        nutritional_result: Nutritional results
        current_calories: Current daily calorie intake
        
    Returns:
        Complete recommendation result
    """
    has_current_calories = current_calories > 0
    
    recommendation = generate_recommendation(
        balance=nutritional_result.energy_balance,
        goal=user_profile.goal,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result,
        has_current_calories=has_current_calories
    )
    
    actionable_steps = generate_actionable_steps(
        goal=user_profile.goal,
        nutritional_result=nutritional_result,
        user_profile=user_profile
    )
    
    confidence_level = calculate_confidence_level(
        user_profile=user_profile,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result,
        has_current_calories=has_current_calories
    )
    
    confidence_explanation = generate_confidence_explanation(
        confidence_level=confidence_level,
        equation_used=user_profile.metabolic_equation
    )
    
    educational_messages = generate_educational_messages(user_profile.goal)
    
    equation_info = METABOLIC_EQUATIONS[user_profile.metabolic_equation]
    
    return RecommendationResult(
        recommendation=recommendation,
        actionable_steps=actionable_steps,
        confidence_level=confidence_level,
        confidence_explanation=confidence_explanation,
        educational_messages=educational_messages,
        equation_used=equation_info["name"],
        expected_error_range=equation_info["error_range"]
    )
