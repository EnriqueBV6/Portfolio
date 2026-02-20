"""
Constants for Nutrition & Training Planner.

This module contains all the constant values used throughout the application,
including activity factors, macro ranges, and decision thresholds.
"""

from typing import Dict

# Activity factors for TDEE calculation
ACTIVITY_FACTORS: Dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "high": 1.725,
    "very_high": 1.9,
}

# Protein requirements (g per kg body weight)
PROTEIN_REQUIREMENTS: Dict[str, Dict[str, float]] = {
    "deficit": {"min": 1.8, "max": 2.2},
    "maintenance": {"min": 1.6, "max": 2.0},
    "bulk": {"min": 1.6, "max": 1.8},
}

# Fat requirements (g per kg body weight)
FAT_REQUIREMENTS: Dict[str, float] = {
    "min": 0.8,
    "max": 1.0,
}

# Caloric adjustment recommendations (kcal)
CALORIC_ADJUSTMENTS: Dict[str, Dict[str, float]] = {
    "deficit": {"min": -500, "max": -300},
    "maintenance": {"min": -200, "max": 200},
    "bulk": {"min": 250, "max": 400},
}

# Caloric values per gram
CALORIES_PER_GRAM: Dict[str, float] = {
    "protein": 4.0,
    "carbs": 4.0,
    "fat": 9.0,
}

# Valid goals
VALID_GOALS = {"deficit", "maintenance", "bulk"}

# Valid sexes for BMR calculation
VALID_SEXES = {"male", "female"}
