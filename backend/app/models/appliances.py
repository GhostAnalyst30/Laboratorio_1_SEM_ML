from enum import Enum


class ApplianceCategory(str, Enum):
    HVAC = "hvac"
    KITCHEN = "kitchen"
    LAUNDRY = "laundry"
    ENTERTAINMENT = "entertainment"
    COMPUTING = "computing"
    LIGHTING = "lighting"
    WATER_HEATING = "water_heating"
    OTHER = "other"


APPLIANCE_POWER_WATTS = {
    "refrigerator": {"wattage": 150, "category": ApplianceCategory.KITCHEN, "runtime_min": 1440},
    "stove": {"wattage": 2500, "category": ApplianceCategory.KITCHEN, "runtime_min": 60},
    "oven": {"wattage": 3000, "category": ApplianceCategory.KITCHEN, "runtime_min": 45},
    "microwave": {"wattage": 1200, "category": ApplianceCategory.KITCHEN, "runtime_min": 15},
    "dishwasher": {"wattage": 1800, "category": ApplianceCategory.KITCHEN, "runtime_min": 90},
    "washing_machine": {"wattage": 1500, "category": ApplianceCategory.LAUNDRY, "runtime_min": 60},
    "dryer": {"wattage": 3000, "category": ApplianceCategory.LAUNDRY, "runtime_min": 60},
    "tv": {"wattage": 120, "category": ApplianceCategory.ENTERTAINMENT, "runtime_min": 240},
    "computer": {"wattage": 200, "category": ApplianceCategory.COMPUTING, "runtime_min": 480},
    "laptop": {"wattage": 60, "category": ApplianceCategory.COMPUTING, "runtime_min": 480},
    "ac_unit": {"wattage": 1500, "category": ApplianceCategory.HVAC, "runtime_min": 360},
    "heater": {"wattage": 2000, "category": ApplianceCategory.HVAC, "runtime_min": 240},
    "water_heater": {"wattage": 4500, "category": ApplianceCategory.WATER_HEATING, "runtime_min": 90},
    "gaming_console": {"wattage": 200, "category": ApplianceCategory.ENTERTAINMENT, "runtime_min": 120},
    "lighting": {"wattage": 30, "category": ApplianceCategory.LIGHTING, "runtime_min": 360},
    "router": {"wattage": 10, "category": ApplianceCategory.OTHER, "runtime_min": 1440},
}

WATER_FLOW_RATES = {
    "shower": 10.0,
    "faucet": 4.0,
    "washing_machine": 65.0,
    "dishwasher": 15.0,
    "toilet": 6.0,
}

GAS_CONSUMPTION = {
    "stove_burner_per_min": 0.003,
    "water_heater_per_min": 0.008,
    "heater_per_min": 0.005,
}
