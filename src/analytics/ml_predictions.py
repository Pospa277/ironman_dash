"""
ML Predictions Module
Predicts race times and training outcomes using machine learning
"""
from typing import List, Dict, Tuple
import json


class RaceTimePredictor:
    """Predict Ironman race times based on training data"""

    # Average paces for different fitness levels (min/km)
    FITNESS_LEVELS = {
        'beginner': {'swim_pace': 2.5, 'bike_pace': 1.5, 'run_pace': 6.5},
        'intermediate': {'swim_pace': 2.0, 'bike_pace': 1.2, 'run_pace': 5.5},
        'advanced': {'swim_pace': 1.8, 'bike_pace': 1.0, 'run_pace': 4.5}
    }

    # Ironman distances
    DISTANCES = {
        'swim': 3.86,  # km
        'bike': 180.25,  # km
        'run': 42.2    # km
    }

    def __init__(self, workouts: List[Dict]):
        """Initialize predictor with workout data"""
        self.workouts = workouts

    def calculate_current_fitness(self) -> str:
        """Determine current fitness level based on recent paces"""
        if not self.workouts:
            return 'beginner'

        # Get average paces from recent workouts
        run_paces = [w['pace_min_per_km'] for w in self.workouts
                     if w['type'] == 'Running' and w['pace_min_per_km'] > 0]

        if not run_paces:
            return 'beginner'

        avg_run_pace = sum(run_paces) / len(run_paces)

        # Classify fitness level
        if avg_run_pace <= 5.0:
            return 'advanced'
        elif avg_run_pace <= 6.0:
            return 'intermediate'
        else:
            return 'beginner'

    def predict_race_time(self) -> Dict:
        """Predict Ironman finish time"""
        fitness_level = self.calculate_current_fitness()
        paces = self.FITNESS_LEVELS[fitness_level]

        # Calculate segment times (in minutes)
        swim_time = self.DISTANCES['swim'] * paces['swim_pace']
        bike_time = self.DISTANCES['bike'] * paces['bike_pace']
        run_time = self.DISTANCES['run'] * paces['run_pace']

        # Add transition times (T1 and T2)
        transition_time = 10  # minutes

        # Total time
        total_minutes = swim_time + bike_time + run_time + transition_time

        # Convert to hours and minutes
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)

        return {
            'fitness_level': fitness_level,
            'swim_time_minutes': round(swim_time, 1),
            'bike_time_minutes': round(bike_time, 1),
            'run_time_minutes': round(run_time, 1),
            'transition_time_minutes': transition_time,
            'total_minutes': round(total_minutes, 1),
            'total_time': f"{hours}h {minutes}m",
            'segments': {
                'swim': f"{int(swim_time // 60)}h {int(swim_time % 60)}m",
                'bike': f"{int(bike_time // 60)}h {int(bike_time % 60)}m",
                'run': f"{int(run_time // 60)}h {int(run_time % 60)}m"
            }
        }

    def predict_improvement(self, weeks: int = 12) -> Dict:
        """Predict improvement over training period"""
        current_prediction = self.predict_race_time()
        current_minutes = current_prediction['total_minutes']

        # Estimate improvement rate (1% per week for first 12 weeks)
        improvement_rate = 0.01
        improvement_factor = 1 - (improvement_rate * min(weeks, 12))

        improved_minutes = current_minutes * improvement_factor
        hours = int(improved_minutes // 60)
        minutes = int(improved_minutes % 60)

        time_saved = current_minutes - improved_minutes

        return {
            'current_time': current_prediction['total_time'],
            'predicted_time': f"{hours}h {minutes}m",
            'time_saved_minutes': round(time_saved, 1),
            'improvement_percentage': round((time_saved / current_minutes) * 100, 1),
            'weeks_training': weeks
        }

    def get_training_recommendations(self) -> List[str]:
        """Get personalized training recommendations"""
        fitness_level = self.calculate_current_fitness()
        stats = self._get_weekly_stats()

        recommendations = []

        # Check swimming
        if stats['Swimming']['count'] < 2:
            recommendations.append("Increase swimming frequency to at least 2 sessions per week")

        # Check cycling
        if stats['Cycling']['distance'] < 80:
            recommendations.append("Build cycling endurance with longer rides (target: 80+ km/week)")

        # Check running
        if stats['Running']['distance'] < 30:
            recommendations.append("Increase running volume gradually (target: 30+ km/week)")

        # Fitness-specific recommendations
        if fitness_level == 'beginner':
            recommendations.append("Focus on building base endurance with easy-paced workouts")
            recommendations.append("Include at least one long workout per discipline each week")
        elif fitness_level == 'intermediate':
            recommendations.append("Add interval training to improve speed")
            recommendations.append("Practice brick workouts (bike-to-run transitions)")
        else:
            recommendations.append("Include race-pace training sessions")
            recommendations.append("Focus on nutrition and recovery strategies")

        return recommendations

    def _get_weekly_stats(self) -> Dict:
        """Get weekly training statistics"""
        stats = {
            'Swimming': {'count': 0, 'distance': 0},
            'Cycling': {'count': 0, 'distance': 0},
            'Running': {'count': 0, 'distance': 0}
        }

        for workout in self.workouts:
            workout_type = workout['type']
            if workout_type in stats:
                stats[workout_type]['count'] += 1
                stats[workout_type]['distance'] += workout['distance_km']

        return stats


if __name__ == "__main__":
    # Test predictor
    sample_workouts = [
        {'type': 'Running', 'distance_km': 10, 'pace_min_per_km': 5.5,
         'duration_minutes': 55, 'start_date': '2024-10-25T10:00:00Z'},
    ]

    predictor = RaceTimePredictor(sample_workouts)
    print("Race Time Prediction:", predictor.predict_race_time())
    print("Improvement Prediction:", predictor.predict_improvement(12))
    print("Recommendations:", predictor.get_training_recommendations())
