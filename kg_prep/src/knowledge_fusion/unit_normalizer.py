import re
import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger("fusion.unit_normalizer")

class UnitNormalizer:
    """Standardizes measurement units (mass, concentrations, temperature) to metric scales."""
    def __init__(self):
        # Conversion to standard base: grams (for mass) or mg/kg (for limits)
        self.mass_conversion = {
            "g": 1.0,
            "gram": 1.0,
            "grams": 1.0,
            "mg": 0.001,
            "milligram": 0.001,
            "milligrams": 0.001,
            "mcg": 0.000001,
            "ug": 0.000001,
            "microgram": 0.000001,
            "micrograms": 0.000001,
            "kg": 1000.0,
            "kilogram": 1000.0,
            "kilograms": 1000.0,
            "oz": 28.3495,
            "ounce": 28.3495,
            "ounces": 28.3495,
            "lb": 453.592,
            "pound": 453.592,
            "pounds": 453.592
        }
        
        self.concentration_conversion = {
            "mg/kg": 1.0,
            "ppm": 1.0,
            "g/kg": 1000.0,
            "%": 10000.0, # 1% = 10,000 mg/kg (ppm)
            "ppb": 0.001
        }

    def normalize_concentration(self, val_str: str) -> Tuple[Optional[float], str]:
        """Parses a concentration string (e.g. '100 mg/kg') and normalizes to mg/kg."""
        if not val_str or not isinstance(val_str, str):
            return None, "mg/kg"
            
        match = re.search(r'([\d\.]+)\s*(mg/kg|ppm|g/kg|%|ppb)?', val_str.lower())
        if not match:
            return None, "mg/kg"
            
        val = float(match.group(1))
        unit = match.group(2) or "mg/kg"
        
        factor = self.concentration_conversion.get(unit, 1.0)
        return val * factor, "mg/kg"

    def normalize_mass(self, val_str: str) -> Tuple[Optional[float], str]:
        """Parses a mass string (e.g. '500 mg') and normalizes to grams (g)."""
        if not val_str or not isinstance(val_str, str):
            return None, "g"
            
        match = re.search(r'([\d\.]+)\s*(g|gram|grams|mg|mcg|ug|kg|oz|ounce|lb|pound)?', val_str.lower())
        if not match:
            return None, "g"
            
        val = float(match.group(1))
        unit = match.group(2) or "g"
        
        factor = self.mass_conversion.get(unit, 1.0)
        return val * factor, "g"
