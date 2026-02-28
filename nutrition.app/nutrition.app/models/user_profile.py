"""
User profile model for Nutrition & Training Planner.

This module defines the UserProfile class that contains all the necessary
information for metabolic and nutritional calculations.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class UserProfile:
    """
    Represents a user's profile with physical and activity characteristics.
    
    Attributes:
        weight: Weight in kilograms
        height: Height in centimeters
        age: Age in years
        sex: Biological sex ('male' or 'female')
        activity_level: Activity factor ('sedentary', 'light', 'moderate', 'high', 'very_high')
        goal: User's goal ('deficit', 'maintenance', 'bulk')
        metabolic_equation: Equation to use for BMR calculation ('mifflin_st_jeor', 'cunningham', 'harris_benedict')
        lean_body_mass: Lean body mass in kg (optional, for Cunningham equation)
    """
    
    weight: float
    height: float
    age: int
    sex: Literal["male", "female"]
    activity_level: Literal["sedentary", "light", "moderate", "high", "very_high"]
    goal: Literal["deficit", "maintenance", "bulk"]
    metabolic_equation: Literal["mifflin_st_jeor", "cunningham", "harris_benedict"] = "mifflin_st_jeor"
    lean_body_mass: float | None = None
    
    def __post_init__(self) -> None:
        """Validate input parameters after initialization."""
        if self.weight <= 0:
            raise ValueError("Weight must be positive")
        if self.height <= 0:
            raise ValueError("Height must be positive")
        if self.age <= 0 or self.age > 120:
            raise ValueError("Age must be between 1 and 120")
        if self.sex not in {"male", "female"}:
            raise ValueError("Sex must be 'male' or 'female'")
        if self.activity_level not in {"sedentary", "light", "moderate", "high", "very_high"}:
            raise ValueError("Invalid activity level")
        if self.goal not in {"deficit", "maintenance", "bulk"}:
            raise ValueError("Goal must be 'deficit', 'maintenance', or 'bulk'")
        if self.metabolic_equation not in {"mifflin_st_jeor", "cunningham", "harris_benedict"}:
            raise ValueError("Invalid metabolic equation")
        if self.lean_body_mass is not None and self.lean_body_mass <= 0:
            raise ValueError("Lean body mass must be positive")
        if self.metabolic_equation == "cunningham" and self.lean_body_mass is None:
            raise ValueError("Cunningham equation requires lean body mass")
