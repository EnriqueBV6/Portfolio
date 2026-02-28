"""
Constants for Nutrition & Training Planner.

This module contains all the constant values used throughout the application,
including activity factors, macro ranges, and decision thresholds.
Updated based on scientific evidence (2015-2025).
"""

from typing import Dict

# Activity factors for TDEE calculation (validated with doubly labeled water studies)
ACTIVITY_FACTORS: Dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "high": 1.725,
    "very_high": 1.9,
}

# Protein requirements (g per kg body weight) - Based on meta-analysis 2015-2025
PROTEIN_REQUIREMENTS: Dict[str, Dict[str, float]] = {
    "deficit": {"min": 1.8, "max": 2.2},  # Higher to preserve muscle during deficit
    "maintenance": {"min": 1.6, "max": 2.0},  # Optimal for maintenance
    "bulk": {"min": 1.6, "max": 1.8},  # Sufficient for muscle growth
}

# Fat requirements (percentage of total calories) - Updated to percentage-based
FAT_REQUIREMENTS_PERCENT: Dict[str, float] = {
    "min": 0.20,  # 20% minimum for hormonal function
    "max": 0.35,  # 35% maximum
}

# Caloric adjustment recommendations (kcal) - Evidence-based ranges
CALORIC_ADJUSTMENTS: Dict[str, Dict[str, float]] = {
    "deficit": {"min": -500, "max": -300},  # Sustainable fat loss
    "maintenance": {"min": -100, "max": 100},  # Tight maintenance range
    "bulk": {"min": 200, "max": 400},  # Lean bulk range
}

# Caloric values per gram
CALORIES_PER_GRAM: Dict[str, float] = {
    "protein": 4.0,
    "carbs": 4.0,
    "fat": 9.0,
}

# Metabolic equations information
METABOLIC_EQUATIONS: Dict[str, Dict[str, any]] = {
    "mifflin_st_jeor": {
        "name": "Mifflin-St Jeor",
        "accuracy": "±10% for ~55-57% of population",
        "year": 1990,
        "best_for": "General population",
        "error_range": "±200 kcal"
    },
    "cunningham": {
        "name": "Cunningham",
        "accuracy": "±10% for ~80% of athletes",
        "year": 1980,
        "best_for": "Athletes with known lean body mass",
        "error_range": "±150 kcal"
    },
    "harris_benedict": {
        "name": "Harris-Benedict (1919, revised 1984)",
        "accuracy": "±10% for ~55% of population",
        "year": 1984,
        "best_for": "Historical comparison",
        "error_range": "±250 kcal"
    }
}

# Educational messages
EDUCATIONAL_MESSAGES: Dict[str, list[str]] = {
    "general": [
        "Las ecuaciones metabólicas son estimaciones basadas en poblaciones.",
        "El gasto energético real puede variar ±10% incluso con las mejores ecuaciones.",
        "Monitoriza tu peso y ajusta las calorías según tus resultados reales.",
        "Factores individuales (genética, hormonas, salud) afectan tu metabolismo."
    ],
    "deficit": [
        "Un déficit de 300-500 kcal/día es óptimo para pérdida de grasa sostenible.",
        "Déficits agresivos (>500 kcal) pueden causar pérdida de masa muscular.",
        "Prioriza proteína (1.8-2.2g/kg) durante déficit para preservar músculo."
    ],
    "bulk": [
        "Un superávit de 200-400 kcal/día es ideal para ganancia muscular limpia.",
        "Superávits mayores (>500 kcal) pueden aumentar acumulación de grasa.",
        "Combina superávit calórico con entrenamiento de fuerza progresivo."
    ]
}

# Valid goals
VALID_GOALS = {"deficit", "maintenance", "bulk"}

# Valid sexes for BMR calculation
VALID_SEXES = {"male", "female"}

# Valid metabolic equations
VALID_EQUATIONS = {"mifflin_st_jeor", "cunningham", "harris_benedict"}
