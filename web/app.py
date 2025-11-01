"""
Flask Web Application for Ironman Training Dashboard
"""
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.apple_health_parser import AppleHealthParser
from src.sync.google_sheets_sync import MockGoogleSheetsSync
from src.analytics.charts import TrainingAnalytics
from src.analytics.ml_predictions import RaceTimePredictor
from src.export.pdf_generator import TrainingReportGenerator


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'data')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Global data store (in production, use a database)
training_data = {
    'workouts': [],
    'analytics': None,
    'prediction': None,
    'last_updated': None
}


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    has_data = len(training_data['workouts']) > 0

    if has_data:
        return render_template('dashboard.html',
                             workouts=training_data['workouts'][:10],
                             analytics=training_data['analytics'],
                             prediction=training_data['prediction'],
                             last_updated=training_data['last_updated'])
    else:
        return render_template('dashboard.html',
                             workouts=[],
                             analytics=None,
                             prediction=None,
                             last_updated=None)


@app.route('/training-plan')
def training_plan():
    """Training plan page"""
    # Generate sample training plan
    plan = generate_training_plan()
    return render_template('training_plan.html', plan=plan)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle Apple Health XML upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and file.filename.endswith('.xml'):
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'export.xml')
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        # Parse data
        try:
            parser = AppleHealthParser(filepath)
            data = parser.parse()

            # Store workouts
            training_data['workouts'] = data['workouts']

            # Generate analytics
            analytics = TrainingAnalytics(data['workouts'])
            training_data['analytics'] = analytics.get_chart_data()

            # Generate predictions
            predictor = RaceTimePredictor(data['workouts'])
            training_data['prediction'] = predictor.predict_race_time()

            training_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            return jsonify({
                'success': True,
                'message': f"Parsed {data['total_workouts']} workouts",
                'redirect': url_for('dashboard')
            })
        except Exception as e:
            return jsonify({'error': f'Error parsing file: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file format. Please upload an XML file.'}), 400


@app.route('/api/chart-data')
def get_chart_data():
    """API endpoint for chart data"""
    if training_data['analytics']:
        return jsonify(training_data['analytics'])
    else:
        return jsonify({'error': 'No data available'}), 404


@app.route('/api/prediction')
def get_prediction():
    """API endpoint for race prediction"""
    if training_data['prediction']:
        return jsonify(training_data['prediction'])
    else:
        return jsonify({'error': 'No data available'}), 404


@app.route('/export/pdf')
def export_pdf():
    """Export training report as PDF"""
    if not training_data['workouts']:
        return jsonify({'error': 'No data to export'}), 400

    try:
        generator = TrainingReportGenerator()
        analytics = TrainingAnalytics(training_data['workouts'])

        filepath = generator.generate_report(
            workouts=training_data['workouts'],
            analytics={'weekly_progress': analytics.get_weekly_progress()},
            prediction=training_data['prediction']
        )

        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Error generating PDF: {str(e)}'}), 500


@app.route('/sync-sheets', methods=['POST'])
def sync_to_sheets():
    """Sync data to Google Sheets"""
    if not training_data['workouts']:
        return jsonify({'error': 'No data to sync'}), 400

    try:
        sync = MockGoogleSheetsSync()
        spreadsheet_id = sync.create_spreadsheet(f"Ironman Training {datetime.now().year}")
        sync.sync_workouts(spreadsheet_id, training_data['workouts'])

        url = sync.get_spreadsheet_url(spreadsheet_id)
        return jsonify({
            'success': True,
            'spreadsheet_url': url,
            'message': 'Data synced to Google Sheets'
        })
    except Exception as e:
        return jsonify({'error': f'Error syncing to sheets: {str(e)}'}), 500


def generate_training_plan():
    """Generate a sample 12-week Ironman training plan"""
    plan = []

    for week in range(1, 13):
        week_plan = {
            'week': week,
            'monday': 'Rest or easy swim (30 min)',
            'tuesday': f'Run intervals {3 + week} km',
            'wednesday': f'Bike endurance {30 + week * 5} km',
            'thursday': 'Swim technique (45 min)',
            'friday': f'Easy run {5 + week} km',
            'saturday': f'Long bike {50 + week * 10} km',
            'sunday': f'Long run {10 + week * 2} km',
            'total_volume': f'{100 + week * 15} km'
        }
        plan.append(week_plan)

    return plan


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
