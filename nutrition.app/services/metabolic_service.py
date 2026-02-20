"""
Metabolic service for Nutrition & Training Planner.

This module provides functions for calculating Basal Metabolic Rate (BMR)
and Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor equation.
"""

from typing import Literal

from models.user_profile import UserProfile
from models.calculation_result import MetabolicResult
from utils.constants import ACTIVITY_FACTORS


def calculate_bmr(weight: float, height: float, age: int, sex: Literal["male", "female"]) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.
    
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


def calculate_metabolic_profile(user_profile: UserProfile) -> MetabolicResult:
    """
    Calculate complete metabolic profile for a user.
    
    Args:
        user_profile: User's physical and activity data
        
    Returns:
        MetabolicResult with BMR and TDEE calculations
    """
    bmr = calculate_bmr(
        weight=user_profile.weight,
        height=user_profile.height,
        age=user_profile.age,
        sex=user_profile.sex
    )
    
    activity_factor = ACTIVITY_FACTORS[user_profile.activity_level]
    tdee = calculate_tdee(bmr, activity_factor)
    
    return MetabolicResult(
        bmr=bmr,
        tdee=tdee,
        activity_factor=activity_factor
    )
