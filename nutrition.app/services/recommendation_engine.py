"""
Recommendation engine for Nutrition & Training Planner.

This module provides functions for generating personalized nutritional
recommendations based on user's metabolic and nutritional data.
"""

from typing import Literal

from models.user_profile import UserProfile
from models.calculation_result import MetabolicResult, NutritionalResult, RecommendationResult


def generate_recommendation(
    balance: float,
    goal: Literal["deficit", "maintenance", "bulk"],
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult
) -> str:
    """
    Generate personalized nutritional recommendation.
    
    Args:
        balance: Current energy balance
        goal: User's goal
        metabolic_result: Metabolic calculation results
        nutritional_result: Nutritional calculation results
        
    Returns:
        Personalized recommendation text
    """
    if goal == "deficit":
        return generate_deficit_recommendation(balance, metabolic_result, nutritional_result)
    elif goal == "bulk":
        return generate_bulk_recommendation(balance, metabolic_result, nutritional_result)
    else:
        return generate_maintenance_recommendation(balance, metabolic_result, nutritional_result)


def generate_deficit_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult
) -> str:
    """Generate recommendation for fat loss goal."""
    
    if balance < -500:
        recommendation = (
            f"Estás en un déficit agresivo de {abs(balance):.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este nivel de déficit puede llevar a pérdida de masa muscular. "
            f"Te recomiendo consumir {nutritional_result.target_calories:.0f} kcal diarias "
            "para una pérdida de grasa sostenible."
        )
    elif balance < -200:
        recommendation = (
            f"Estás en un déficit moderado de {abs(balance):.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este es un buen nivel para pérdida de grasa. "
            f"Tu objetivo de {nutritional_result.target_calories:.0f} kcal es apropiado."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:.0f} calorías no es suficiente para pérdida de grasa. "
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
    nutritional_result: NutritionalResult
) -> str:
    """Generate recommendation for muscle gain goal."""
    
    if balance > 500:
        recommendation = (
            f"Estás en un superávit agresivo de {balance:.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este nivel puede generar acumulación excesiva de grasa. "
            f"Te recomiendo consumir {nutritional_result.target_calories:.0f} kcal diarias "
            "para ganancia muscular limpia."
        )
    elif balance > 200:
        recommendation = (
            f"Estás en un superávit moderado de {balance:.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            "Este es un buen nivel para ganancia muscular. "
            f"Tu objetivo de {nutritional_result.target_calories:.0f} kcal es apropiado."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:.0f} calorías no es suficiente para ganancia muscular. "
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
    nutritional_result: NutritionalResult
) -> str:
    """Generate recommendation for maintenance goal."""
    
    if abs(balance) <= 200:
        recommendation = (
            f"Excelente. Estás manteniendo tu peso con un balance de {balance:.0f} calorías. "
            f"Tu TDEE es de {metabolic_result.tdee:.0f} kcal. "
            f"Tu consumo actual de {nutritional_result.target_calories:.0f} kcal es ideal para mantenimiento."
        )
    else:
        recommendation = (
            f"Tu balance actual de {balance:.0f} calorías te está alejando del mantenimiento. "
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
    nutritional_result: NutritionalResult
) -> float:
    """
    Calculate confidence level of recommendations.
    
    Args:
        user_profile: User's profile
        metabolic_result: Metabolic results
        nutritional_result: Nutritional results
        
    Returns:
        Confidence level between 0 and 1
    """
    confidence = 0.8  # Base confidence
    
    # Adjust based on profile completeness
    if 18 <= user_profile.age <= 65:
        confidence += 0.1
    
    if 18.5 <= user_profile.weight / ((user_profile.height / 100) ** 2) <= 30:
        confidence += 0.05
    
    if user_profile.activity_level in ["light", "moderate", "high"]:
        confidence += 0.05
    
    return min(confidence, 1.0)


def generate_complete_recommendation(
    user_profile: UserProfile,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult
) -> RecommendationResult:
    """
    Generate complete recommendation with actionable steps and confidence.
    
    Args:
        user_profile: User's profile
        metabolic_result: Metabolic results
        nutritional_result: Nutritional results
        
    Returns:
        Complete recommendation result
    """
    recommendation = generate_recommendation(
        balance=nutritional_result.energy_balance,
        goal=user_profile.goal,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result
    )
    
    actionable_steps = generate_actionable_steps(
        goal=user_profile.goal,
        nutritional_result=nutritional_result,
        user_profile=user_profile
    )
    
    confidence_level = calculate_confidence_level(
        user_profile=user_profile,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result
    )
    
    return RecommendationResult(
        recommendation=recommendation,
        actionable_steps=actionable_steps,
        confidence_level=confidence_level
    )
