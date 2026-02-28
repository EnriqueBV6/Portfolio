"""
Recommendation engine for Nutrition & Training Planner.

This module provides functions for generating personalized nutritional
recommendations based on user's metabolic and nutritional data.
Updated with scientific evidence (2015-2025).
"""

try:
    from typing import Literal, Optional
except ImportError:
    from typing_extensions import Literal
    from typing import Optional

from models.user_profile import UserProfile
from models.body_composition import BodyCompositionResult
from models.calculation_result import MetabolicResult, NutritionalResult, RecommendationResult
from utils.constants import METABOLIC_EQUATIONS, EDUCATIONAL_MESSAGES


def generate_recommendation(
    balance: float,
    goal: Literal["deficit", "maintenance", "bulk"],
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool,
    body_composition_result: Optional[BodyCompositionResult] = None
) -> str:
    """
    Generate personalized nutritional recommendation.
    
    Args:
        balance: Current energy balance
        goal: User's goal
        metabolic_result: Metabolic calculation results
        nutritional_result: Nutritional calculation results
        has_current_calories: Whether user provided current calorie intake
        body_composition_result: Optional body composition analysis
        
    Returns:
        Personalized recommendation text
    """
    if goal == "deficit":
        return generate_deficit_recommendation(balance, metabolic_result, nutritional_result, has_current_calories, body_composition_result)
    elif goal == "bulk":
        return generate_bulk_recommendation(balance, metabolic_result, nutritional_result, has_current_calories, body_composition_result)
    else:
        return generate_maintenance_recommendation(balance, metabolic_result, nutritional_result, has_current_calories, body_composition_result)


def generate_deficit_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool,
    body_composition_result: Optional[BodyCompositionResult] = None
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
    
    # Integrar análisis de composición corporal
    if body_composition_result:
        composition_context = _generate_composition_context_deficit(
            body_composition_result=body_composition_result,
            target_calories=nutritional_result.target_calories,
            metabolic_tdee=metabolic_result.tdee,
            protein_g=nutritional_result.macro_split['protein']
        )
        recommendation += f"\n\n{composition_context}"
    
    return recommendation


def generate_bulk_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool,
    body_composition_result: Optional[BodyCompositionResult] = None
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
    
    # Integrar análisis de composición corporal
    if body_composition_result:
        composition_context = _generate_composition_context_bulk(body_composition_result)
        recommendation += f"\n\n{composition_context}"
    
    return recommendation


def generate_maintenance_recommendation(
    balance: float,
    metabolic_result: MetabolicResult,
    nutritional_result: NutritionalResult,
    has_current_calories: bool,
    body_composition_result: Optional[BodyCompositionResult] = None
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
    
    # Integrar análisis de composición corporal
    if body_composition_result:
        composition_context = _generate_composition_context_maintenance(body_composition_result)
        recommendation += f"\n\n{composition_context}"
    
    return recommendation


def generate_actionable_steps(
    goal: Literal["deficit", "maintenance", "bulk"],
    nutritional_result: NutritionalResult,
    user_profile: UserProfile,
    body_composition_result: Optional[BodyCompositionResult] = None
) -> list[str]:
    """
    Generate actionable steps for the user.
    
    Args:
        goal: User's goal
        nutritional_result: Nutritional calculation results
        user_profile: User's profile
        body_composition_result: Optional body composition analysis
        
    Returns:
        List of actionable steps
    """
    steps = []
    
    # General steps
    steps.append(f"Consume {nutritional_result.target_calories:.0f} kcal diarias")
    steps.append(f"Consume {nutritional_result.macro_split['protein']:.1f}g de proteína diariamente")
    steps.append(f"Consume {nutritional_result.macro_split['fat']:.1f}g de grasas saludables diariamente")
    steps.append(f"Consume {nutritional_result.macro_split['carbs']:.1f}g de carbohidratos diariamente")
    
    # Goal-specific steps with composition-aware enhancements
    if goal == "deficit":
        # Check for high body fat
        high_bf_threshold_male = 25
        high_bf_threshold_female = 32
        threshold = high_bf_threshold_female if user_profile.sex.lower() == "female" else high_bf_threshold_male
        
        if body_composition_result and body_composition_result.body_fat_percentage > threshold:
            steps.append("Prioriza proteína para preservar masa muscular durante reducción de grasa")
            steps.append("Enfócate en entrenamiento de fuerza para mantener musculatura")
            steps.append("Espera pérdida de 0.5-1kg por semana; si es más rápido, aumenta calorías")
        else:
            steps.append("Prioriza proteína para preservar masa muscular")
            steps.append("Monitorea tu peso semanalmente")
            steps.append("Ajusta calorías si pierdes más de 1kg por semana")
        
        # Composition-specific insight
        if body_composition_result:
            steps.append(_get_composition_strategy_step(body_composition_result, goal))
    
    elif goal == "bulk":
        # Check for high body fat already
        high_bf_threshold_male = 20
        high_bf_threshold_female = 28
        threshold = high_bf_threshold_female if user_profile.sex.lower() == "female" else high_bf_threshold_male
        
        if body_composition_result and body_composition_result.body_fat_percentage > threshold:
            steps.append("Asegura entrenamiento de fuerza progresivo")
            steps.append("Prioriza ganancia de músculo sobre grasa; aumenta gradualmente calorías")
            steps.append("Monitorea composición (no solo peso) durante volumen")
        else:
            steps.append("Monitorea tu peso semanalmente")
            steps.append("Ajusta calorías si ganas más de 0.5kg por semana")
            steps.append("Asegura entrenamiento de fuerza progresivo")
        
        if body_composition_result:
            steps.append(_get_composition_strategy_step(body_composition_result, goal))
    
    else:  # maintenance
        steps.append("Mantén consistencia en tu consumo calórico")
        steps.append("Ajusta según fluctuaciones de peso naturales")
        
        # If composition needs improvement
        recompose_threshold_male = 25
        recompose_threshold_female = 32
        threshold = recompose_threshold_female if user_profile.sex.lower() == "female" else recompose_threshold_male
        
        if body_composition_result and body_composition_result.body_fat_percentage > threshold:
            steps.append(_get_composition_strategy_step(body_composition_result, goal))
        elif body_composition_result and body_composition_result.ffmi_category in ["Sedentario/Débil", "Moderado sin entrenar"]:
            steps.append("Incorpora entrenamiento de fuerza para mejorar composición")
    
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
    current_calories: float = 0.0,
    body_composition_result: Optional[BodyCompositionResult] = None
) -> RecommendationResult:
    """
    Generate complete recommendation with actionable steps and confidence.
    
    Args:
        user_profile: User's profile
        metabolic_result: Metabolic results
        nutritional_result: Nutritional results
        current_calories: Current daily calorie intake
        body_composition_result: Optional body composition analysis
        
    Returns:
        Complete recommendation result
    """
    has_current_calories = current_calories > 0
    
    recommendation = generate_recommendation(
        balance=nutritional_result.energy_balance,
        goal=user_profile.goal,
        metabolic_result=metabolic_result,
        nutritional_result=nutritional_result,
        has_current_calories=has_current_calories,
        body_composition_result=body_composition_result
    )
    
    actionable_steps = generate_actionable_steps(
        goal=user_profile.goal,
        nutritional_result=nutritional_result,
        user_profile=user_profile,
        body_composition_result=body_composition_result
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


# FUNCIONES AUXILIARES PARA ANÁLISIS DE COMPOSICIÓN CORPORAL


def _generate_composition_context_deficit(
    body_composition_result: BodyCompositionResult,
    target_calories: float,
    metabolic_tdee: float,
    protein_g: float
) -> str:
    """
    Generate contextualized recommendation for deficit with body composition insights.
    """
    deficit_kcal = metabolic_tdee - target_calories
    weekly_loss_kg = (deficit_kcal * 7) / 7700 if deficit_kcal > 0 else 0.5  # 7700 kcal = 1kg fat
    weeks_to_goal = _calculate_weeks_to_composition_goal(
        current_bf=body_composition_result.body_fat_percentage,
        target_bf=20 if body_composition_result.lean_body_mass > 30 else 25,
        weekly_loss_rate=weekly_loss_kg
    )
    
    context = f"**Contexto de Composición Corporal:**\n"
    context += f"Tu masa grasa actual es {body_composition_result.fat_mass:.1f}kg ({body_composition_result.body_fat_percentage:.1f}%). "
    context += f"Tu masa magra (músculo) es {body_composition_result.lean_body_mass:.1f}kg.\n"
    context += f"A un ritmo de pérdida de {weekly_loss_kg:.2f}kg/semana, podrías alcanzar alrededor del 20% de grasa en aprox. {weeks_to_goal} semanas.\n"
    context += f"Con {protein_g:.0f}g de proteína diaria ({protein_g/body_composition_result.lean_body_mass:.2f}g/kg LBM), protegerás tu músculo durante el déficit."
    
    return context


def _generate_composition_context_bulk(
    body_composition_result: BodyCompositionResult
) -> str:
    """
    Generate contextualized recommendation for bulk with body composition insights.
    """
    context = f"**Contexto de Composición Corporal:**\n"
    
    if body_composition_result.body_fat_percentage > 20:
        context += f"Tu grasa corporal actual es {body_composition_result.body_fat_percentage:.1f}%, "
        context += "lo que es moderado para fase de aumento. Enfócate en ganancia muscular limpia: "
        context += "incrementa calorías gradualmente y alinéalas con entrenamiento de fuerza progresivo. "
        context += "Espera ganar ~0.3-0.4kg/semana de músculo puro."
    else:
        context += f"Tu composición actual es favorable ({body_composition_result.body_fat_percentage:.1f}% grasa). "
        context += "Puedes aprovechar bien el superávit calórico. Asegura entrenamiento de fuerza intenso para maximizar ganancia muscular."
    
    context += f"\nTu masa magra es {body_composition_result.lean_body_mass:.1f}kg ({body_composition_result.ffmi:.1f} FFMI - {body_composition_result.ffmi_category})."
    
    return context


def _generate_composition_context_maintenance(
    body_composition_result: BodyCompositionResult
) -> str:
    """
    Generate contextualized recommendation for maintenance with body composition insights.
    """
    context = f"**Contexto de Composición Corporal:**\n"
    context += f"Tu composición actual: {body_composition_result.body_fat_percentage:.1f}% grasa, {body_composition_result.lean_body_mass:.1f}kg de masa magra.\n"
    
    if 25 < body_composition_result.body_fat_percentage <= 50:
        context += "Aunque mantienes peso, puedes mejorar tu composición mediante recomposición (perder grasa ganando músculo). "
        context += "Entrena fuerza intensamente mientras mantienes calorías estables: el efecto de recomposición hará que pierdas grasa y ganes músculo simultáneamente."
    else:
        context += "Tu composición es saludable. Mantén entrenamiento de fuerza consistente para preservar y desarrollar masa muscular a largo plazo."
    
    return context


def _get_composition_strategy_step(
    body_composition_result: BodyCompositionResult,
    goal: str
) -> str:
    """
    Generate a specific actionable step based on composition profile.
    """
    if goal == "deficit":
        if body_composition_result.ffmi_category in ["Sedentario/Débil", "Moderado sin entrenar"]:
            return f"Entrena fuerza 3-4 veces/semana para preservar músculo (actual: {body_composition_result.ffmi:.1f} FFMI)"
        elif body_composition_result.whr_risk_level and body_composition_result.whr_risk_level in ["Riesgo elevado", "Riesgo muy elevado"]:
            return "Prioriza reducción de grasa visceral (cintura): el entrenamiento de fuerza es especialmente eficaz"
        else:
            return f"Mantén composición favorable priorizando proteína (LBM: {body_composition_result.lean_body_mass:.1f}kg)"
    
    elif goal == "bulk":
        if body_composition_result.ffmi_category in ["Elite natural", "Probablemente potenciado"]:
            return "Eres muy musculoso; enfócate en ganancia limpia sin exceso graso incrementando gradualmente"
        elif body_composition_result.ffmi_category in ["Sedentario/Débil", "Moderado sin entrenar"]:
            return f"Tienes potencial muscular alto (FFMI: {body_composition_result.ffmi:.1f}); aprovecha el superávit para construcción"
        else:
            return f"Concéntrate en ganancia muscular limpia (FFMI: {body_composition_result.ffmi:.1f})"
    
    else:  # maintenance
        if body_composition_result.body_fat_percentage > 25:
            return "Aunque mantienes calorías, busca recomposición corporal: entrena fuerza y la grasa bajará mientras ganas músculo"
        else:
            return f"Tu composición es buena; mantén entrenamiento que preserve/aumente FFMI (actual: {body_composition_result.ffmi:.1f})"


def _calculate_weeks_to_composition_goal(
    current_bf: float,
    target_bf: float,
    weekly_loss_rate: float
) -> int:
    """
    Calculate approximate weeks to reach body fat target.
    
    Args:
        current_bf: Current body fat percentage
        target_bf: Target body fat percentage
        weekly_loss_rate: Expected weekly weight loss in kg
        
    Returns:
        Approximate weeks (rounded)
    """
    if weekly_loss_rate <= 0:
        return 0
    
    bf_change_per_week = (weekly_loss_rate * 0.75) / 70
    bf_percentage_change_per_week = bf_change_per_week
    
    weeks = abs(current_bf - target_bf) / max(bf_percentage_change_per_week, 0.1)
    return max(int(round(weeks)), 1)
