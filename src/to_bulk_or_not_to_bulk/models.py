from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class UnitSystem(str, Enum):
    METRIC = "m"       # Metric (kg, cm)
    IMPERIAL = "i"     # Imperial (lbs, in)


class Sex(str, Enum):
    MALE = "m"
    FEMALE = "f"


class GoalType(str, Enum):
    GAIN = "gain"   # Naik berat (bulking)
    LOSS = "loss"   # Turun berat (cutting)


class ActivityLevel(str, Enum):
    SEDENTARY = "1.2"
    LIGHTLY_ACTIVE = "1.375"
    MODERATELY_ACTIVE = "1.55"
    VERY_ACTIVE = "1.725"
    EXTREMELY_ACTIVE = "1.9"


ACTIVITY_DESCRIPTIONS: Dict[str, str] = {
    "1.2": "Hampir tidak berolahraga, misalnya kerja di meja tanpa aktivitas fisik tambahan.",
    "1.375": "Olahraga ringan 1-2 hari per minggu.",
    "1.55": "Olahraga sedang 3-5 hari per minggu.",
    "1.725": "Olahraga berat 6-7 hari per minggu.",
    "1.9": "Olahraga berat setiap hari dengan pekerjaan fisik, atau latihan dua kali sehari.",
}

ACTIVITY_TITLES: Dict[str, str] = {
    "1.2": "Sedenter | x1,2",
    "1.375": "Ringan | x1,375",
    "1.55": "Sedang | x1,55",
    "1.725": "Aktif | x1,725",
    "1.9": "Sangat aktif | x1,9",
}


class SurplusDeficitLevel(str, Enum):
    RECOMMENDED = "0.1"
    AGGRESSIVE = "0.15"
    VERY_AGGRESSIVE = "0.2"
    CUSTOM = "c"


class UserInput(BaseModel):
    unit: UnitSystem = Field(default=UnitSystem.METRIC, description="Unit: m (metric) or i (imperial)")
    weight: float = Field(..., gt=0, description="Berat badan (kg or lbs)")
    height: float = Field(..., gt=0, description="Tinggi badan (cm or in)")
    age: int = Field(..., ge=15, le=90, description="Usia (tahun)")
    sex: Sex = Field(default=Sex.MALE, description="Jenis kelamin: m (pria) or f (wanita)")
    activity_level: ActivityLevel = Field(default=ActivityLevel.MODERATELY_ACTIVE, description="Olahraga dalam seminggu")
    goal: GoalType = Field(default=GoalType.GAIN, description="Tujuan: gain (bulking) or loss (cutting)")
    target_days: int = Field(default=180, ge=7, le=1095, description="Target waktu (hari)")
    level: SurplusDeficitLevel = Field(default=SurplusDeficitLevel.RECOMMENDED, description="Level surplus/defisit")
    custom_calories: Optional[float] = Field(default=None, ge=50, le=1500, description="Kalori surplus/defisit kustom (kcal/hari)")


class MilestonePoint(BaseModel):
    day: int
    change: float
    weight: float


class MacroRecommendation(BaseModel):
    protein_g: float
    protein_per_kg: float
    fat_g: float
    fat_pct: float
    carb_g: float


class CalculationResult(BaseModel):
    unit: str
    weight: float
    target_days: int
    goal: GoalType
    bmi: float
    bmi_category: str
    bmr: float
    tdee: float
    activity_multiplier: float
    surplus_deficit: float
    surplus_deficit_pct: float
    target_calories: float
    ewc: float
    weight_change: float
    final_weight: float
    final_bmi: float
    macros: MacroRecommendation
    milestones: List[MilestonePoint]
    warnings: List[str]
