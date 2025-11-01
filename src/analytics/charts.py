"""
Charts and Analytics Module
Generates charts and analytics for training progress
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict
import os


class TrainingAnalytics:
    """Analytics for training data"""

    # Ironman target distances
    IRONMAN_DISTANCES = {
        'Swimming': 3.86,  # km
        'Cycling': 180.25,  # km
        'Running': 42.2    # km
    }

    def __init__(self, workouts: List[Dict]):
        """Initialize analytics with workout data"""
        self.workouts = workouts

    def get_weekly_progress(self) -> Dict:
        """Calculate weekly progress towards Ironman goals"""
        weekly_totals = {
            'Swimming': 0,
            'Cycling': 0,
            'Running': 0
        }

        # Calculate last 7 days
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        for workout in self.workouts:
            try:
                workout_date = datetime.fromisoformat(workout['start_date'].replace('Z', '+00:00'))
                if workout_date >= week_ago:
                    workout_type = workout['type']
                    if workout_type in weekly_totals:
                        weekly_totals[workout_type] += workout['distance_km']
            except:
                continue

        # Calculate percentages
        progress = {}
        for activity, distance in weekly_totals.items():
            target = self.IRONMAN_DISTANCES[activity]
            percentage = (distance / target) * 100 if target > 0 else 0
            progress[activity] = {
                'distance': round(distance, 2),
                'target': target,
                'percentage': round(percentage, 2),
                'remaining': round(target - distance, 2)
            }

        return progress

    def get_pace_trend(self, activity: str = 'Running', days: int = 30) -> List[Dict]:
        """Get pace trend for specific activity"""
        pace_data = []
        now = datetime.now()
        cutoff_date = now - timedelta(days=days)

        for workout in self.workouts:
            if workout['type'] == activity:
                try:
                    workout_date = datetime.fromisoformat(workout['start_date'].replace('Z', '+00:00'))
                    if workout_date >= cutoff_date:
                        pace_data.append({
                            'date': workout['start_date'],
                            'pace': workout['pace_min_per_km'],
                            'distance': workout['distance_km']
                        })
                except:
                    continue

        return sorted(pace_data, key=lambda x: x['date'])

    def get_total_stats(self) -> Dict:
        """Get total training statistics"""
        stats = {
            'Swimming': {'count': 0, 'distance': 0, 'duration': 0},
            'Cycling': {'count': 0, 'distance': 0, 'duration': 0},
            'Running': {'count': 0, 'distance': 0, 'duration': 0}
        }

        for workout in self.workouts:
            workout_type = workout['type']
            if workout_type in stats:
                stats[workout_type]['count'] += 1
                stats[workout_type]['distance'] += workout['distance_km']
                stats[workout_type]['duration'] += workout['duration_minutes']

        return stats

    def get_chart_data(self) -> Dict:
        """Prepare data for Chart.js visualization"""
        # Weekly distance by activity
        weekly_data = self.get_weekly_progress()

        # Pace trend for running
        pace_trend = self.get_pace_trend('Running', days=30)

        # Total stats
        total_stats = self.get_total_stats()

        return {
            'weekly_progress': {
                'labels': list(weekly_data.keys()),
                'current': [weekly_data[k]['distance'] for k in weekly_data.keys()],
                'target': [weekly_data[k]['target'] for k in weekly_data.keys()],
                'percentage': [weekly_data[k]['percentage'] for k in weekly_data.keys()]
            },
            'pace_trend': {
                'labels': [p['date'][:10] for p in pace_trend],
                'data': [p['pace'] for p in pace_trend]
            },
            'total_stats': total_stats
        }

    def is_on_track(self, weeks_until_race: int = 12) -> Dict:
        """Check if training is on track for Ironman"""
        current_weekly = self.get_weekly_progress()

        on_track = {}
        for activity, data in current_weekly.items():
            # Calculate required weekly distance
            target_total = self.IRONMAN_DISTANCES[activity]
            # Assume need to reach 80% of race distance in training
            required_weekly = (target_total * 0.8) / weeks_until_race
            current_weekly_avg = data['distance']

            on_track[activity] = {
                'current_weekly': round(current_weekly_avg, 2),
                'required_weekly': round(required_weekly, 2),
                'on_track': current_weekly_avg >= required_weekly,
                'percentage_of_required': round((current_weekly_avg / required_weekly * 100) if required_weekly > 0 else 0, 2)
            }

        return on_track


def generate_progress_chart_js(analytics: TrainingAnalytics) -> str:
    """Generate Chart.js configuration"""
    chart_data = analytics.get_chart_data()

    config = {
        'type': 'bar',
        'data': {
            'labels': chart_data['weekly_progress']['labels'],
            'datasets': [
                {
                    'label': 'Current Week',
                    'data': chart_data['weekly_progress']['current'],
                    'backgroundColor': 'rgba(54, 162, 235, 0.8)'
                },
                {
                    'label': 'Ironman Target',
                    'data': chart_data['weekly_progress']['target'],
                    'backgroundColor': 'rgba(255, 99, 132, 0.8)'
                }
            ]
        },
        'options': {
            'responsive': True,
            'plugins': {
                'title': {
                    'display': True,
                    'text': 'Weekly Progress vs Ironman Distances'
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {
                        'display': True,
                        'text': 'Distance (km)'
                    }
                }
            }
        }
    }

    return json.dumps(config)


if __name__ == "__main__":
    # Test analytics
    sample_workouts = [
        {'type': 'Running', 'distance_km': 10, 'pace_min_per_km': 5.5,
         'duration_minutes': 55, 'start_date': '2024-10-25T10:00:00Z'},
        {'type': 'Cycling', 'distance_km': 50, 'pace_min_per_km': 0,
         'duration_minutes': 120, 'start_date': '2024-10-26T10:00:00Z'},
    ]

    analytics = TrainingAnalytics(sample_workouts)
    print("Weekly Progress:", analytics.get_weekly_progress())
    print("On Track:", analytics.is_on_track(12))
