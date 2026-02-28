"""
Body composition analysis service.

This module provides functions for analyzing body composition including
fat mass, lean body mass, FFMI, and waist-hip ratio calculations.
"""

from typing import Optional
from models.body_composition import BodyComposition, BodyCompositionResult
from models.user_profile import UserProfile
from utils.constants import BODY_FAT_RANGES, FFMI_CATEGORIES, WHR_RISK


def generate_body_composition_result(
    user_profile: UserProfile,
    body_composition: Optional[BodyComposition] = None
) -> Optional[BodyCompositionResult]:
    """
    Calcula composición corporal completa basada en %grasa y opcionales circumferencias.
    
    Args:
        user_profile: Datos del usuario (peso, altura, sexo, edad)
        body_composition: Datos de composición (body_fat%, circumferencias, etc.)
    
    Returns:
        BodyCompositionResult con todos los cálculos, o None si no hay composición
    
    Raises:
        ValueError: Si datos incoherentes
    """
    
    if not body_composition:
        return None
    
    # PASO 1: Calcular Masa Magra (LBM)
    pbf = body_composition.body_fat_percentage
    weight_kg = user_profile.weight
    
    fat_mass_kg = weight_kg * (pbf / 100)
    lean_body_mass_kg = weight_kg - fat_mass_kg
    
    # PASO 2: Calcular FFMI
    height_m = user_profile.height / 100  # Convertir cm a metros
    ffmi = lean_body_mass_kg / (height_m ** 2)
    
    # PASO 3: Determinar categoría corporal por %grasa
    sex = user_profile.sex.lower()
    ranges = BODY_FAT_RANGES.get(sex, {})
    body_fat_category = _get_bf_category(pbf, ranges)
    
    # PASO 4: Determinar categoría FFMI
    ffmi_category = _get_ffmi_category(ffmi)
    
    # PASO 5: Calcular WHR si existen medidas
    whr = None
    whr_risk_level = None
    if body_composition.circumference_waist and body_composition.circumference_hip:
        whr = body_composition.circumference_waist / body_composition.circumference_hip
        whr_risk_level = _get_whr_risk_level(whr, sex)
    
    # PASO 6: Determinar calidad de medición
    measurement_quality = "basic"
    if all([body_composition.circumference_biceps, 
            body_composition.circumference_chest,
            body_composition.circumference_waist,
            body_composition.circumference_hip,
            body_composition.circumference_thigh]):
        measurement_quality = "full"
    
    # PASO 7: Crear resultado
    result = BodyCompositionResult(
        body_fat_percentage=round(pbf, 1),
        fat_mass=round(fat_mass_kg, 1),
        lean_body_mass=round(lean_body_mass_kg, 1),
        ffmi=round(ffmi, 1),
        waist_hip_ratio=round(whr, 2) if whr else None,
        waist_circumference=body_composition.circumference_waist,
        hip_circumference=body_composition.circumference_hip,
        body_fat_category=body_fat_category,
        ffmi_category=ffmi_category,
        whr_risk_level=whr_risk_level,
        measurement_quality=measurement_quality
    )
    
    return result


def _get_bf_category(pbf: float, ranges: dict) -> str:
    """
    Retorna categoría de %grasa (Atlético, Normal, Obeso, etc.)
    """
    for category, range_dict in ranges.items():
        if range_dict["min"] <= pbf < range_dict["max"]:
            return range_dict["label"]
    return "Desconocido"


def _get_ffmi_category(ffmi: float) -> str:
    """
    Retorna categoría FFMI
    """
    for category, range_dict in FFMI_CATEGORIES.items():
        if range_dict["min"] <= ffmi <= range_dict["max"]:
            return range_dict["label"]
    return "Desconocido"


def _get_whr_risk_level(whr: float, sex: str) -> str:
    """
    Retorna nivel de riesgo cardiovascular basado en WHR
    """
    risk_table = WHR_RISK.get(sex, {})
    
    for risk_key, risk_dict in risk_table.items():
        if whr <= risk_dict.get("max", float("inf")) and whr > risk_dict.get("min", -1):
            return risk_dict["risk_level"]
    
    return "Muy Alto"  # Default si fuera de rangos

def calculate_protein_requirement_from_lbm(
    lean_body_mass_kg: float,
    goal: str
) -> dict:
    """
    Calcula requerimiento de proteína basado en LBM, no en peso total.
    
    Args:
        lean_body_mass_kg: Masa magra del usuario
        goal: "deficit" / "maintenance" / "bulk"
    
    Returns:
        dict con min_g, max_g, basis
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