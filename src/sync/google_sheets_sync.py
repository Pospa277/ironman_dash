"""
Google Sheets Sync Module
Syncs workout data to Google Sheets for tracking and analysis
"""
import os
import json
from typing import List, Dict
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    print("Google API libraries not available. Install with: pip install google-api-python-client")


class GoogleSheetsSync:
    """Sync workout data to Google Sheets"""

    # Google Sheets API scopes
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, credentials_path: str = 'credentials.json'):
        """Initialize Google Sheets sync"""
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google API libraries not installed")

        self.credentials_path = credentials_path
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if os.path.exists(self.credentials_path):
                creds = service_account.Credentials.from_service_account_file(
                    self.credentials_path, scopes=self.SCOPES)
                self.service = build('sheets', 'v4', credentials=creds)
                print("Successfully authenticated with Google Sheets API")
            else:
                print(f"Credentials file not found: {self.credentials_path}")
                print("Please download credentials from Google Cloud Console")
                self.service = None
        except Exception as e:
            print(f"Authentication error: {e}")
            self.service = None

    def create_spreadsheet(self, title: str) -> str:
        """Create a new spreadsheet"""
        if not self.service:
            return None

        try:
            spreadsheet = {
                'properties': {'title': title},
                'sheets': [
                    {'properties': {'title': 'Workouts'}},
                    {'properties': {'title': 'Weekly Summary'}},
                    {'properties': {'title': 'Progress'}}
                ]
            }

            result = self.service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()

            spreadsheet_id = result.get('spreadsheetId')
            print(f"Created spreadsheet: {spreadsheet_id}")
            return spreadsheet_id
        except HttpError as e:
            print(f"Error creating spreadsheet: {e}")
            return None

    def sync_workouts(self, spreadsheet_id: str, workouts: List[Dict]):
        """Sync workout data to Google Sheets"""
        if not self.service or not workouts:
            return False

        try:
            # Prepare header row
            headers = [['Date', 'Type', 'Distance (km)', 'Duration (min)',
                       'Pace (min/km)', 'Energy (kcal)']]

            # Prepare data rows
            rows = []
            for workout in workouts:
                row = [
                    workout.get('start_date', ''),
                    workout.get('type', ''),
                    round(workout.get('distance_km', 0), 2),
                    round(workout.get('duration_minutes', 0), 2),
                    round(workout.get('pace_min_per_km', 0), 2),
                    round(workout.get('energy_kcal', 0), 2)
                ]
                rows.append(row)

            # Combine headers and data
            values = headers + rows

            # Update sheet
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Workouts!A1',
                valueInputOption='RAW',
                body=body
            ).execute()

            print(f"Updated {result.get('updatedCells')} cells")
            return True
        except HttpError as e:
            print(f"Error syncing workouts: {e}")
            return False

    def sync_weekly_summary(self, spreadsheet_id: str, summary: Dict):
        """Sync weekly summary to Google Sheets"""
        if not self.service:
            return False

        try:
            headers = [['Activity', 'Count', 'Total Distance (km)', 'Total Duration (min)']]
            rows = []

            for activity, data in summary.items():
                row = [
                    activity,
                    data.get('count', 0),
                    round(data.get('distance', 0), 2),
                    round(data.get('duration', 0), 2)
                ]
                rows.append(row)

            values = headers + rows
            body = {'values': values}

            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Weekly Summary!A1',
                valueInputOption='RAW',
                body=body
            ).execute()

            print(f"Updated weekly summary: {result.get('updatedCells')} cells")
            return True
        except HttpError as e:
            print(f"Error syncing summary: {e}")
            return False

    def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        """Get the URL for a spreadsheet"""
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"


# Mock version for testing without credentials
class MockGoogleSheetsSync:
    """Mock version for development/testing"""

    def __init__(self, credentials_path: str = 'credentials.json'):
        print("Using mock Google Sheets sync (no credentials)")

    def create_spreadsheet(self, title: str) -> str:
        mock_id = f"MOCK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Mock: Created spreadsheet '{title}' with ID: {mock_id}")
        return mock_id

    def sync_workouts(self, spreadsheet_id: str, workouts: List[Dict]):
        print(f"Mock: Synced {len(workouts)} workouts to {spreadsheet_id}")
        return True

    def sync_weekly_summary(self, spreadsheet_id: str, summary: Dict):
        print(f"Mock: Synced weekly summary to {spreadsheet_id}")
        return True

    def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"


if __name__ == "__main__":
    # Test sync
    sync = MockGoogleSheetsSync()
    spreadsheet_id = sync.create_spreadsheet("Ironman Training 2024")
    print(f"Spreadsheet URL: {sync.get_spreadsheet_url(spreadsheet_id)}")
