"""
Calculation result models for Nutrition & Training Planner.

This module defines the data structures that store the results of metabolic
and nutritional calculations.
"""

from dataclasses import dataclass
from typing import Dict, Literal


@dataclass
class MetabolicResult:
    """
    Stores the results of metabolic calculations.
    
    Attributes:
        bmr: Basal Metabolic Rate in calories
        tdee: Total Daily Energy Expenditure in calories
        activity_factor: The activity factor used in TDEE calculation
    """
    
    bmr: float
    tdee: float
    activity_factor: float


@dataclass
class NutritionalResult:
    """
    Stores the results of nutritional calculations.
    
    Attributes:
        energy_balance: Daily energy balance (calories_in - tdee - training_calories)
        status: Current metabolic status ('deficit', 'maintenance', 'surplus')
        target_calories: Recommended daily caloric intake
        macro_split: Macronutrient distribution in grams
        macro_percentages: Macronutrient distribution as percentages
    """
    
    energy_balance: float
    status: Literal["deficit", "maintenance", "surplus"]
    target_calories: float
    macro_split: Dict[str, float]
    macro_percentages: Dict[str, float]


@dataclass
class RecommendationResult:
    """
    Stores the results of recommendation engine.
    
    Attributes:
        recommendation: Textual recommendation based on calculations
        actionable_steps: List of actionable steps for the user
        confidence_level: Confidence level of the recommendation (0-1)
    """
    
    recommendation: str
    actionable_steps: list[str]
    confidence_level: float


@dataclass
class CompleteAnalysis:
    """
    Complete analysis result combining all calculation results.
    
    Attributes:
        user_profile: The user profile used for calculations
        metabolic: Metabolic calculation results
        nutritional: Nutritional calculation results
        recommendation: Recommendation engine results
    """
    
    user_profile: "UserProfile"
    metabolic: MetabolicResult
    nutritional: NutritionalResult
    recommendation: RecommendationResult
