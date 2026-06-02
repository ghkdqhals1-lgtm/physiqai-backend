from experta import Fact


class UserFact(Fact):
    """사용자 기본 정보"""
    # age: int
    # weight_kg: float
    # height_cm: float
    # goal: str  — weight_loss | muscle_gain | maintenance
    # fitness_level: str  — beginner | intermediate | advanced
    # gender: str  — male | female


class SleepFact(Fact):
    """수면 데이터 (7일 평균)"""
    # avg_duration_hours: float
    # avg_quality: float  — 1~5
    # consistency_score: float  — 0~1 (취침/기상 시간 일관성)


class NutritionFact(Fact):
    """영양 데이터 (7일 평균) + 파생 지표"""
    # avg_daily_calories: float
    # avg_protein_g: float
    # avg_carbs_g: float
    # avg_fat_g: float
    # protein_per_kg: float  — avg_protein_g / weight_kg (엔진에서 계산)
    # calorie_balance: float  — avg_daily_calories - TDEE (엔진에서 계산)


class AlcoholFact(Fact):
    """알코올 섭취 데이터"""
    # weekly_units: float  — 표준 음주 단위 (1단위 ≈ 알코올 14g)
    # frequency_per_week: int  — 주당 음주 횟수


class MenstrualFact(Fact):
    """생리주기 데이터"""
    # cycle_day: int   — 생리 시작 후 몇 번째 날 (1-based)
    # cycle_length: int  — 평균 주기 길이 (기본 28)
    # cycle_phase: str  — menstrual | follicular | ovulation | luteal (엔진에서 계산)


class WorkoutFact(Fact):
    """운동볼륨 데이터 (최근 7일)"""
    # sessions_per_week: int
    # avg_duration_minutes: float
    # total_weekly_minutes: float
    # has_strength: bool
    # has_cardio: bool


class VisceralFatFact(Fact):
    """내장지방 데이터 (인바디)"""
    # visceral_fat_level: int  — 1~20 (인바디 기준)
    # body_fat_percent: float


class HealthAlert(Fact):
    """건강 경고 팩트 — 규칙 실행 결과"""
    # category: str
    # severity: str  — info | warning | danger
    # message: str


class Recommendation(Fact):
    """권고사항 팩트 — 규칙 실행 결과"""
    # category: str
    # message: str
    # priority: int  — 1(높음) ~ 3(낮음)
