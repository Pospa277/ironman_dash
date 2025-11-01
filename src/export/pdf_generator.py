"""
PDF Report Generator
Generates PDF training reports with charts and analytics
"""
from datetime import datetime
from typing import Dict, List
import os

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab not available. Install with: pip install reportlab")


class TrainingReportGenerator:
    """Generate PDF training reports"""

    def __init__(self, output_dir: str = "data"):
        """Initialize PDF generator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_report(self,
                       workouts: List[Dict],
                       analytics: Dict,
                       prediction: Dict,
                       filename: str = None) -> str:
        """Generate complete training report PDF"""

        if not REPORTLAB_AVAILABLE:
            print("ReportLab not installed. Generating text report instead.")
            return self._generate_text_report(workouts, analytics, prediction, filename)

        if not filename:
            filename = f"ironman_training_report_{datetime.now().strftime('%Y%m%d')}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=12,
            spaceBefore=12
        )

        # Title
        title = Paragraph("Ironman Training Report", title_style)
        story.append(title)

        date_text = Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            styles['Normal']
        )
        story.append(date_text)
        story.append(Spacer(1, 0.3 * inch))

        # Summary Section
        story.append(Paragraph("Training Summary", heading_style))
        summary_data = self._create_summary_table(workouts)
        story.append(summary_data)
        story.append(Spacer(1, 0.2 * inch))

        # Weekly Progress
        story.append(Paragraph("Weekly Progress", heading_style))
        progress_table = self._create_progress_table(analytics.get('weekly_progress', {}))
        story.append(progress_table)
        story.append(Spacer(1, 0.2 * inch))

        # Race Prediction
        story.append(Paragraph("Race Time Prediction", heading_style))
        prediction_table = self._create_prediction_table(prediction)
        story.append(prediction_table)
        story.append(Spacer(1, 0.2 * inch))

        # Recent Workouts
        story.append(Paragraph("Recent Workouts", heading_style))
        workouts_table = self._create_workouts_table(workouts[:10])  # Last 10 workouts
        story.append(workouts_table)

        # Build PDF
        doc.build(story)
        print(f"PDF report generated: {filepath}")
        return filepath

    def _create_summary_table(self, workouts: List[Dict]) -> Table:
        """Create summary statistics table"""
        stats = {
            'Swimming': {'count': 0, 'distance': 0, 'duration': 0},
            'Cycling': {'count': 0, 'distance': 0, 'duration': 0},
            'Running': {'count': 0, 'distance': 0, 'duration': 0}
        }

        for workout in workouts:
            workout_type = workout['type']
            if workout_type in stats:
                stats[workout_type]['count'] += 1
                stats[workout_type]['distance'] += workout['distance_km']
                stats[workout_type]['duration'] += workout['duration_minutes']

        data = [
            ['Activity', 'Workouts', 'Total Distance (km)', 'Total Time (hours)']
        ]

        for activity, stat in stats.items():
            data.append([
                activity,
                str(stat['count']),
                f"{stat['distance']:.1f}",
                f"{stat['duration'] / 60:.1f}"
            ])

        table = Table(data, colWidths=[2 * inch, 1.5 * inch, 2 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table

    def _create_progress_table(self, progress: Dict) -> Table:
        """Create weekly progress table"""
        data = [
            ['Activity', 'This Week (km)', 'Target (km)', 'Progress (%)']
        ]

        for activity, stats in progress.items():
            data.append([
                activity,
                f"{stats.get('distance', 0):.1f}",
                f"{stats.get('target', 0):.1f}",
                f"{stats.get('percentage', 0):.1f}%"
            ])

        table = Table(data, colWidths=[2 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table

    def _create_prediction_table(self, prediction: Dict) -> Table:
        """Create race prediction table"""
        data = [
            ['Metric', 'Value'],
            ['Fitness Level', prediction.get('fitness_level', 'N/A').title()],
            ['Predicted Finish Time', prediction.get('total_time', 'N/A')],
            ['Swim Time', prediction.get('segments', {}).get('swim', 'N/A')],
            ['Bike Time', prediction.get('segments', {}).get('bike', 'N/A')],
            ['Run Time', prediction.get('segments', {}).get('run', 'N/A')]
        ]

        table = Table(data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        return table

    def _create_workouts_table(self, workouts: List[Dict]) -> Table:
        """Create recent workouts table"""
        data = [
            ['Date', 'Type', 'Distance', 'Duration', 'Pace']
        ]

        for workout in workouts:
            date = workout.get('start_date', '')[:10]
            data.append([
                date,
                workout.get('type', 'N/A'),
                f"{workout.get('distance_km', 0):.1f} km",
                f"{workout.get('duration_minutes', 0):.0f} min",
                f"{workout.get('pace_min_per_km', 0):.1f} min/km"
            ])

        table = Table(data, colWidths=[1.3 * inch, 1.3 * inch, 1.3 * inch, 1.3 * inch, 1.3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))

        return table

    def _generate_text_report(self, workouts, analytics, prediction, filename) -> str:
        """Generate plain text report as fallback"""
        if not filename:
            filename = f"ironman_training_report_{datetime.now().strftime('%Y%m%d')}.txt"

        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("IRONMAN TRAINING REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%B %d, %Y')}\n\n")

            f.write("RACE TIME PREDICTION\n")
            f.write("-" * 60 + "\n")
            f.write(f"Fitness Level: {prediction.get('fitness_level', 'N/A').title()}\n")
            f.write(f"Predicted Finish Time: {prediction.get('total_time', 'N/A')}\n\n")

            f.write(f"Total Workouts: {len(workouts)}\n\n")

        print(f"Text report generated: {filepath}")
        return filepath


if __name__ == "__main__":
    # Test PDF generator
    generator = TrainingReportGenerator()
    sample_workouts = [
        {'type': 'Running', 'distance_km': 10, 'pace_min_per_km': 5.5,
         'duration_minutes': 55, 'start_date': '2024-10-25T10:00:00Z'},
    ]
    sample_prediction = {
        'fitness_level': 'intermediate',
        'total_time': '12h 30m',
        'segments': {'swim': '1h 15m', 'bike': '6h 45m', 'run': '4h 0m'}
    }
    print("PDF generator ready")
