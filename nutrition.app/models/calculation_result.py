"""
Calculation result models for Nutrition & Training Planner.

This module defines the data structures that store the results of metabolic
and nutritional calculations.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


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
        confidence_explanation: Explanation of what the confidence level means
        educational_messages: Educational messages about metabolic calculations
        equation_used: Which metabolic equation was used
        expected_error_range: Expected error range for the predictions
    """
    
    recommendation: str
    actionable_steps: List[str]
    confidence_level: float
    confidence_explanation: str
    educational_messages: List[str]
    equation_used: str
    expected_error_range: str


@dataclass
class CompleteAnalysis:
    """
    Complete analysis result combining all calculation results.
    
    Attributes:
        user_profile: The user profile used for calculations
        metabolic: Metabolic calculation results
        nutritional: Nutritional calculation results
        recommendation: Recommendation engine results
        body_composition: Body composition analysis results (optional)
    """
    
    user_profile: "UserProfile"
    metabolic: MetabolicResult
    nutritional: NutritionalResult
    recommendation: RecommendationResult
    body_composition: Optional["BodyCompositionResult"] = None
