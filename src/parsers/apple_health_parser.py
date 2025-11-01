"""
Apple Health XML Parser
Parses Apple Health export.xml file and extracts workout data
"""
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
import os


class AppleHealthParser:
    """Parser for Apple Health XML export"""

    def __init__(self, xml_path: str):
        """Initialize parser with XML file path"""
        self.xml_path = xml_path
        self.workouts = []
        self.records = []

    def parse(self) -> Dict:
        """Parse the XML file and extract workout data"""
        if not os.path.exists(self.xml_path):
            raise FileNotFoundError(f"XML file not found: {self.xml_path}")

        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        # Parse workouts
        for workout in root.findall('.//Workout'):
            workout_data = self._parse_workout(workout)
            if workout_data:
                self.workouts.append(workout_data)

        # Parse health records (heart rate, etc.)
        for record in root.findall('.//Record'):
            record_data = self._parse_record(record)
            if record_data:
                self.records.append(record_data)

        return {
            'workouts': self.workouts,
            'records': self.records,
            'total_workouts': len(self.workouts),
            'total_records': len(self.records)
        }

    def _parse_workout(self, workout) -> Dict:
        """Parse individual workout element"""
        try:
            workout_type = workout.get('workoutActivityType', '')

            # Filter for triathlon activities
            triathlon_types = ['Running', 'Cycling', 'Swimming',
                             'HKWorkoutActivityTypeRunning',
                             'HKWorkoutActivityTypeCycling',
                             'HKWorkoutActivityTypeSwimming']

            if not any(t in workout_type for t in triathlon_types):
                return None

            start_date = workout.get('startDate', '')
            end_date = workout.get('endDate', '')
            duration = float(workout.get('duration', 0))
            distance = float(workout.get('totalDistance', 0))
            energy = float(workout.get('totalEnergyBurned', 0))

            # Convert distance from meters to km
            distance_km = distance / 1000 if distance > 0 else 0

            return {
                'type': self._normalize_workout_type(workout_type),
                'start_date': start_date,
                'end_date': end_date,
                'duration_minutes': duration / 60,
                'distance_km': distance_km,
                'energy_kcal': energy,
                'pace_min_per_km': (duration / 60) / distance_km if distance_km > 0 else 0
            }
        except Exception as e:
            print(f"Error parsing workout: {e}")
            return None

    def _parse_record(self, record) -> Dict:
        """Parse individual health record"""
        try:
            record_type = record.get('type', '')

            # Filter for relevant metrics
            relevant_types = ['HKQuantityTypeIdentifierHeartRate',
                            'HKQuantityTypeIdentifierRestingHeartRate',
                            'HKQuantityTypeIdentifierVO2Max']

            if not any(t in record_type for t in relevant_types):
                return None

            return {
                'type': record_type,
                'value': float(record.get('value', 0)),
                'unit': record.get('unit', ''),
                'start_date': record.get('startDate', ''),
                'end_date': record.get('endDate', '')
            }
        except Exception as e:
            print(f"Error parsing record: {e}")
            return None

    def _normalize_workout_type(self, workout_type: str) -> str:
        """Normalize workout type names"""
        if 'Running' in workout_type:
            return 'Running'
        elif 'Cycling' in workout_type:
            return 'Cycling'
        elif 'Swimming' in workout_type:
            return 'Swimming'
        return workout_type

    def get_weekly_summary(self) -> Dict:
        """Get weekly workout summary"""
        summary = {
            'Running': {'count': 0, 'distance': 0, 'duration': 0},
            'Cycling': {'count': 0, 'distance': 0, 'duration': 0},
            'Swimming': {'count': 0, 'distance': 0, 'duration': 0}
        }

        for workout in self.workouts:
            workout_type = workout['type']
            if workout_type in summary:
                summary[workout_type]['count'] += 1
                summary[workout_type]['distance'] += workout['distance_km']
                summary[workout_type]['duration'] += workout['duration_minutes']

        return summary

    def export_to_dict(self) -> List[Dict]:
        """Export workouts as list of dictionaries for Google Sheets"""
        return self.workouts


if __name__ == "__main__":
    # Test parser
    parser = AppleHealthParser("data/export.xml")
    data = parser.parse()
    print(f"Parsed {data['total_workouts']} workouts")
    print(f"Weekly summary: {parser.get_weekly_summary()}")
