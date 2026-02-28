"""
Metabolic service for Nutrition & Training Planner.

This module provides functions for calculating Basal Metabolic Rate (BMR)
and Total Daily Energy Expenditure (TDEE) using multiple validated equations.
Updated with scientific evidence (2015-2025).
"""

from typing import Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from models.user_profile import UserProfile
from models.calculation_result import MetabolicResult
from models.body_composition import BodyCompositionResult
from utils.constants import ACTIVITY_FACTORS, METABOLIC_EQUATIONS


def calculate_bmr_mifflin_st_jeor(weight: float, height: float, age: int, sex: Literal["male", "female"]) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation (1990).
    Most accurate for general population.
    
    Formula:
    - Male: BMR = 10 * weight + 6.25 * height - 5 * age + 5
    - Female: BMR = 10 * weight + 6.25 * height - 5 * age - 161
    
    Args:
        weight: Weight in kilograms
        height: Height in centimeters
        age: Age in years
        sex: Biological sex ('male' or 'female')
        
    Returns:
        BMR in calories per day
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")
    if age <= 0 or age > 120:
        raise ValueError("Age must be between 1 and 120")
    if sex not in {"male", "female"}:
        raise ValueError("Sex must be 'male' or 'female'")
    
    bmr = 10 * weight + 6.25 * height - 5 * age
    bmr += 5 if sex == "male" else -161
    
    return round(bmr, 2)


def calculate_bmr_cunningham(lean_body_mass: float) -> float:
    """
    Calculate Basal Metabolic Rate using Cunningham equation (1980).
    Most accurate for athletes with known lean body mass.
    
    Formula: BMR = 370 + 21.6 * lean_body_mass
    
    Args:
        lean_body_mass: Lean body mass in kilograms
        
    Returns:
        BMR in calories per day
        
    Raises:
        ValueError: If lean_body_mass is invalid
    """
    if lean_body_mass <= 0:
        raise ValueError("Lean body mass must be positive")
    
    bmr = 370 + 21.6 * lean_body_mass
    return round(bmr, 2)


def calculate_bmr_harris_benedict(weight: float, height: float, age: int, sex: Literal["male", "female"]) -> float:
    """
    Calculate Basal Metabolic Rate using Harris-Benedict equation (revised 1984).
    Classic equation, less accurate for modern populations.
    
    Formula:
    - Male: BMR = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    - Female: BMR = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    Args:
        weight: Weight in kilograms
        height: Height in centimeters
        age: Age in years
        sex: Biological sex ('male' or 'female')
        
    Returns:
        BMR in calories per day
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if height <= 0:
        raise ValueError("Height must be positive")
    if age <= 0 or age > 120:
        raise ValueError("Age must be between 1 and 120")
    if sex not in {"male", "female"}:
        raise ValueError("Sex must be 'male' or 'female'")
    
    if sex == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return round(bmr, 2)


def calculate_bmr(user_profile: UserProfile) -> float:
    """
    Calculate BMR using the selected metabolic equation.
    
    Args:
        user_profile: User's physical and activity data
        
    Returns:
        BMR in calories per day
        
    Raises:
        ValueError: If parameters are invalid or equation requirements not met
    """
    if user_profile.metabolic_equation == "mifflin_st_jeor":
        return calculate_bmr_mifflin_st_jeor(
            weight=user_profile.weight,
            height=user_profile.height,
            age=user_profile.age,
            sex=user_profile.sex
        )
    elif user_profile.metabolic_equation == "cunningham":
        if user_profile.lean_body_mass is None:
            raise ValueError("Cunningham equation requires lean body mass")
        return calculate_bmr_cunningham(user_profile.lean_body_mass)
    elif user_profile.metabolic_equation == "harris_benedict":
        return calculate_bmr_harris_benedict(
            weight=user_profile.weight,
            height=user_profile.height,
            age=user_profile.age,
            sex=user_profile.sex
        )
    else:
        raise ValueError(f"Unsupported metabolic equation: {user_profile.metabolic_equation}")


def calculate_tdee(bmr: float, activity_factor: float) -> float:
    """
    Calculate Total Daily Energy Expenditure.
    
    Args:
        bmr: Basal Metabolic Rate in calories
        activity_factor: Activity multiplier (1.2 to 1.9)
        
    Returns:
        TDEE in calories per day
        
    Raises:
        ValueError: If parameters are invalid
    """
    if bmr <= 0:
        raise ValueError("BMR must be positive")
    if activity_factor <= 0:
        raise ValueError("Activity factor must be positive")
    
    tdee = bmr * activity_factor
    return round(tdee, 2)


def calculate_metabolic_profile(
    user_profile: UserProfile,
    body_composition_result: Optional[BodyCompositionResult] = None
) -> MetabolicResult:
    """
    Calculate complete metabolic profile for a user.
    
    Si existe body_composition_result (con LBM), usa Cunningham (más preciso).
    Si no, usa la ecuación configurada en user_profile.

    Args:
        user_profile: User's physical and activity data
        body_composition_result: Body composition analysis with lean body mass
        
    Returns:
        MetabolicResult with BMR and TDEE calculations
    """
    # Si tenemos LBM de body composition, usar Cunningham (más preciso)
    if body_composition_result and body_composition_result.lean_body_mass:
        bmr = calculate_bmr_cunningham(body_composition_result.lean_body_mass)
        equation_used = "cunningham"
    else:
        # Usar ecuación seleccionada en user_profile
        bmr = calculate_bmr(user_profile)
        equation_used = user_profile.metabolic_equation
    
    activity_factor = ACTIVITY_FACTORS[user_profile.activity_level]
    tdee = calculate_tdee(bmr, activity_factor)
    
    # Crear resultado con ecuación usada
    result = MetabolicResult(
        bmr=bmr,
        tdee=tdee,
        activity_factor=activity_factor
    )
    
    # Agregar atributo equation_used si es necesario (compatibilidad)
    result.equation_used = equation_used
    
    return result
