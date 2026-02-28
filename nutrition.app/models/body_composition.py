"""
Body composition analysis models.

This module defines the data structures for analyzing body composition,
including body fat percentage and circumference measurements.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BodyComposition:
    """Composición corporal basada en %grasa y circunferencias"""
    
    # OBLIGATORIOS
    body_fat_percentage: float  # 5-60%
    
    # OPCIONALES - Circunferencias en cm
    circumference_biceps: Optional[float] = None  # Brazo relajado
    circumference_chest: Optional[float] = None   # A la altura de los pezones
    circumference_waist: Optional[float] = None   # Punto medio entre costilla y cresta iliaca
    circumference_hip: Optional[float] = None     # Máxima prominencia glútea
    circumference_thigh: Optional[float] = None   # Punto medio muslo
    
    def __post_init__(self):
        # VALIDACIONES
        
        # 1. Rango de %grasa
        if self.body_fat_percentage < 5 or self.body_fat_percentage > 60:
            raise ValueError(f"Body fat % debe estar entre 5-60%, recibido {self.body_fat_percentage}")
        
        # 2. Validar coherencia: si circumferences existen, todas deben estar en rango
        if any([self.circumference_biceps, self.circumference_chest, self.circumference_waist, 
                self.circumference_hip, self.circumference_thigh]):
            if self.circumference_biceps and (self.circumference_biceps < 15 or self.circumference_biceps > 50):
                raise ValueError(f"Biceps circumference {self.circumference_biceps}cm fuera de rango")
            if self.circumference_chest and (self.circumference_chest < 70 or self.circumference_chest > 150):
                raise ValueError(f"Chest circumference {self.circumference_chest}cm fuera de rango")
            if self.circumference_waist and (self.circumference_waist < 50 or self.circumference_waist > 150):
                raise ValueError(f"Waist circumference {self.circumference_waist}cm fuera de rango")
            if self.circumference_hip and (self.circumference_hip < 60 or self.circumference_hip > 150):
                raise ValueError(f"Hip circumference {self.circumference_hip}cm fuera de rango")
            if self.circumference_thigh and (self.circumference_thigh < 30 or self.circumference_thigh > 80):
                raise ValueError(f"Thigh circumference {self.circumference_thigh}cm fuera de rango")


@dataclass
class BodyCompositionResult:
    """Resultados del análisis de composición corporal"""
    
    body_fat_percentage: float  # %
    fat_mass: float             # kg
    lean_body_mass: float       # kg
    ffmi: float                 # Fat-Free Mass Index (kg/m²)
    
    # Índices de riesgo
    waist_hip_ratio: Optional[float] = None      # Si hay medidas de caderas
    waist_circumference: Optional[float] = None  # cm
    hip_circumference: Optional[float] = None    # cm
    
    # Interpretaciones (strings para mostrar)
    body_fat_category: str = ""      # "Atlético", "Normal", etc.
    ffmi_category: str = ""          # "Sedentario", "Trained", etc.
    whr_risk_level: Optional[str] = None  # "Bajo", "Moderado", etc.
    
    # Confidencialidad
    measurement_quality: str = "basic"  # "basic" (sin medidas) / "full" (con circunferencias)
    
    def __post_init__(self):
        # Validar coherencia
        if self.fat_mass < 0 or self.lean_body_mass < 0:
            raise ValueError("Fat mass y LBM no pueden ser negativos")
        
        if self.ffmi < 10 or self.ffmi > 50:
            raise ValueError(f"FFMI {self.ffmi} fuera de rango biológico")
        
        if self.waist_hip_ratio and (self.waist_hip_ratio < 0.5 or self.waist_hip_ratio > 1.5):
            raise ValueError(f"WHR {self.waist_hip_ratio} fuera de rango posible")
