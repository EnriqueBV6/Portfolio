"""
Nutrition service for Nutrition & Training Planner.

This module provides functions for calculating energy balance,
macronutrient distribution, and nutritional targets.
Updated with scientific evidence (2015-2025).
"""

from typing import Dict, Tuple, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from models.user_profile import UserProfile
from models.calculation_result import MetabolicResult, NutritionalResult
from models.body_composition import BodyCompositionResult
from utils.constants import (
    PROTEIN_REQUIREMENTS,
    FAT_REQUIREMENTS_PERCENT,
    CALORIC_ADJUSTMENTS,
    CALORIES_PER_GRAM
)


def calculate_energy_balance(
    calories_in: float,
    tdee: float,
    calories_out_training: float = 0.0
) -> float:
    """
    Calculate daily energy balance.
    
    Args:
        calories_in: Calories consumed
        tdee: Total Daily Energy Expenditure
        calories_out_training: Additional calories burned through training
        
    Returns:
        Energy balance (positive for surplus, negative for deficit)
        
    Raises:
        ValueError: If any parameter is negative
    """
    if calories_in < 0:
        raise ValueError("Calories in cannot be negative")
    if tdee < 0:
        raise ValueError("TDEE cannot be negative")
    if calories_out_training < 0:
        raise ValueError("Training calories cannot be negative")
    
    return round(calories_in - tdee - calories_out_training, 2)


def determine_energy_status(balance: float) -> Literal["deficit", "maintenance", "surplus"]:
    """
    Determine energy status based on balance.
    
    Args:
        balance: Energy balance in calories
        
    Returns:
        Energy status category
    """
    if balance < -200:
        return "deficit"
    elif balance > 200:
        return "surplus"
    else:
        return "maintenance"


def calculate_macro_split(
    calories: float,
    weight: float,
    goal: Literal["deficit", "maintenance", "bulk"]
) -> Dict[str, float]:
    """
    Calculate macronutrient distribution based on calories, weight, and goal.
    Uses evidence-based ranges from meta-analysis (2015-2025).
    
    Args:
        calories: Target calories
        weight: Body weight in kg
        goal: User's goal
        
    Returns:
        Dictionary with macro amounts in grams
        
    Raises:
        ValueError: If parameters are invalid
    """
    if calories <= 0:
        raise ValueError("Calories must be positive")
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if goal not in {"deficit", "maintenance", "bulk"}:
        raise ValueError("Invalid goal")
    
    # Calculate protein based on goal (evidence-based ranges)
    protein_range = PROTEIN_REQUIREMENTS[goal]
    protein_g = weight * ((protein_range["min"] + protein_range["max"]) / 2)
    
    # Calculate fat based on percentage of total calories
    fat_percentage = (FAT_REQUIREMENTS_PERCENT["min"] + FAT_REQUIREMENTS_PERCENT["max"]) / 2
    fat_calories = calories * fat_percentage
    fat_g = fat_calories / CALORIES_PER_GRAM["fat"]
    
    # Calculate remaining calories for carbs
    protein_calories = protein_g * CALORIES_PER_GRAM["protein"]
    remaining_calories = calories - protein_calories - fat_calories
    
    # Ensure we don't get negative carbs
    if remaining_calories < 0:
        # Adjust fat to minimum if needed
        min_fat_calories = calories * FAT_REQUIREMENTS_PERCENT["min"]
        if protein_calories + min_fat_calories <= calories:
            fat_calories = min_fat_calories
            fat_g = fat_calories / CALORIES_PER_GRAM["fat"]
            remaining_calories = calories - protein_calories - fat_calories
        else:
            # Reduce protein to minimum
            protein_g = weight * protein_range["min"]
            protein_calories = protein_g * CALORIES_PER_GRAM["protein"]
            remaining_calories = calories - protein_calories - (fat_g * CALORIES_PER_GRAM["fat"])
    
    carbs_g = max(0, remaining_calories / CALORIES_PER_GRAM["carbs"])
    
    return {
        "protein": round(protein_g, 1),
        "fat": round(fat_g, 1),
        "carbs": round(carbs_g, 1)
    }


def calculate_macro_percentages(macro_split: Dict[str, float]) -> Dict[str, float]:
    """
    Convert macro grams to percentages.
    
    Args:
        macro_split: Macro amounts in grams
        
    Returns:
        Macro percentages
    """
    protein_calories = macro_split["protein"] * CALORIES_PER_GRAM["protein"]
    fat_calories = macro_split["fat"] * CALORIES_PER_GRAM["fat"]
    carbs_calories = macro_split["carbs"] * CALORIES_PER_GRAM["carbs"]
    
    total_calories = protein_calories + fat_calories + carbs_calories
    
    if total_calories == 0:
        return {"protein": 0.0, "fat": 0.0, "carbs": 0.0}
    
    return {
        "protein": round((protein_calories / total_calories) * 100, 1),
        "fat": round((fat_calories / total_calories) * 100, 1),
        "carbs": round((carbs_calories / total_calories) * 100, 1)
    }


def calculate_target_calories(tdee: float, goal: Literal["deficit", "maintenance", "bulk"]) -> float:
    """
    Calculate target calories based on TDEE and goal.
    Uses evidence-based adjustment ranges.
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal: User's goal
        
    Returns:
        Target daily calories
    """
    adjustment_range = CALORIC_ADJUSTMENTS[goal]
    adjustment = (adjustment_range["min"] + adjustment_range["max"]) / 2
    
    return round(tdee + adjustment, 2)


def calculate_nutritional_profile(
    user_profile: UserProfile,
    metabolic_result: MetabolicResult,
    current_calories: float = 0.0,
    training_calories: float = 0.0
) -> NutritionalResult:
    """
    Calculate complete nutritional profile for a user.
    
    Args:
        user_profile: User's profile data
        metabolic_result: Metabolic calculation results
        current_calories: Current daily calorie intake
        training_calories: Calories burned through training
        
    Returns:
        NutritionalResult with complete nutritional analysis
    """
    # Calculate energy balance (will be 0 if current_calories is 0)
    energy_balance = calculate_energy_balance(
        calories_in=current_calories,
        tdee=metabolic_result.tdee,
        calories_out_training=training_calories
    )
    
    # Determine status
    status = determine_energy_status(energy_balance)
    
    # Calculate target calories
    target_calories = calculate_target_calories(metabolic_result.tdee, user_profile.goal)
    
    # Calculate macro split
    macro_split = calculate_macro_split(
        calories=target_calories,
        weight=user_profile.weight,
        goal=user_profile.goal
    )
    
    # Calculate macro percentages
    macro_percentages = calculate_macro_percentages(macro_split)
    
    return NutritionalResult(
        energy_balance=energy_balance,
        status=status,
        target_calories=target_calories,
        macro_split=macro_split,
        macro_percentages=macro_percentages
    )


def calculate_protein_requirement(
    lean_body_mass_kg: float,
    goal: str
) -> dict:
    """
    Calcula requerimiento de proteína basado en LBM, no en peso total.
    
    Args:
        lean_body_mass_kg: Masa magra del usuario
        goal: "deficit" / "maintenance" / "bulk"
    
    Returns:
        dict con min_g, max_g, explanation
    """
    
    protein_ranges = {
        "deficit": {"min": 1.8, "max": 2.2},     # Preservar LBM en déficit
        "maintenance": {"min": 1.6, "max": 2.0},
        "bulk": {"min": 1.6, "max": 2.0}
    }
    
    range_g_per_kg = protein_ranges.get(goal, {"min": 1.6, "max": 2.0})
    
    return {
        "min_g": round(lean_body_mass_kg * range_g_per_kg["min"], 1),
        "max_g": round(lean_body_mass_kg * range_g_per_kg["max"], 1),
        "basis": f"Basado en {lean_body_mass_kg}kg de LBM, no peso total"
    }

