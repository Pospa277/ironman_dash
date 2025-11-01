# Ironman Training Dashboard 🏊‍♂️🚴‍♂️🏃‍♂️

A comprehensive web-based training tracker and analyzer for Ironman triathletes. Upload your Apple Health data to get instant insights, race predictions, and personalized training analytics.

![Ironman Dashboard](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

## Features

### 📊 Training Analytics
- Track weekly progress across swimming, cycling, and running
- Compare your training volume to Ironman race distances
- View detailed statistics and metrics for each workout

### 🎯 Race Time Predictions
- ML-powered predictions for your Ironman finish time
- Segment-by-segment time estimates (swim, bike, run)
- Fitness level assessment based on your training data

### 📈 Progress Tracking
- Interactive charts using Chart.js
- Pace trend analysis
- Weekly progress visualization

### 📱 Google Sheets Integration
- Automatic synchronization of workout data
- Cloud-based backup of training logs
- Easy sharing with coaches or training partners

### 📄 PDF Reports
- Professional training reports
- Summary statistics and predictions
- Exportable for offline viewing

### 🏃 Training Plans
- 12-week progressive Ironman training plan
- Structured weekly schedules
- Tips and recommendations for each discipline

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pospa277/ironman_dash.git
   cd ironman_dash
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   cd web
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

### 1. Export Apple Health Data

On your iPhone:
1. Open the **Health** app
2. Tap your profile picture (top right)
3. Scroll down and tap **Export All Health Data**
4. Save the `export.zip` file
5. Unzip and locate the `export.xml` file

### 2. Upload to Dashboard

1. Visit the dashboard home page
2. Drag and drop your `export.xml` file
3. Click "Upload & Analyze"
4. Wait for processing (this may take a minute for large files)

### 3. View Your Analytics

After upload, you'll be redirected to your dashboard where you can:
- View your race time prediction
- Explore weekly progress charts
- Check recent workouts
- Export reports as PDF
- Sync data to Google Sheets

## Project Structure

```
ironman_dash/
├── src/
│   ├── parsers/
│   │   └── apple_health_parser.py    # Parse Apple Health XML
│   ├── sync/
│   │   └── google_sheets_sync.py     # Google Sheets integration
│   ├── analytics/
│   │   ├── charts.py                 # Analytics and chart data
│   │   └── ml_predictions.py         # ML race predictions
│   └── export/
│       └── pdf_generator.py          # PDF report generation
├── web/
│   ├── app.py                        # Flask application
│   ├── templates/                    # HTML templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   └── training_plan.html
│   └── static/                       # CSS, JS, and assets
│       ├── css/style.css
│       └── js/charts.js
├── data/                             # Data storage (gitignored)
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **ML**: scikit-learn (for predictions)
- **PDF**: ReportLab
- **API**: Google Sheets API
- **Parser**: xml.etree.ElementTree

## Configuration

### Google Sheets Setup (Optional)

To enable Google Sheets sync:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create service account credentials
5. Download credentials as `credentials.json`
6. Place in project root directory

### Environment Variables

Create a `.env` file (optional):
```bash
FLASK_ENV=development
FLASK_DEBUG=True
```

## Features Deep Dive

### Apple Health Parser
- Extracts workout data from Apple Health XML export
- Filters for triathlon-relevant activities (swim, bike, run)
- Calculates pace, distance, duration, and energy metrics
- Handles large XML files efficiently

### ML Predictions
- Analyzes recent training data
- Classifies fitness level (beginner, intermediate, advanced)
- Predicts race finish times based on current training pace
- Estimates improvement over training period

### Training Analytics
- Weekly volume tracking
- Progress towards Ironman distances
- Pace trend analysis
- "On track" checker for race readiness

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
cd web
python app.py
```

### Running Tests

```bash
python -m pytest tests/
```

## Roadmap

- [ ] User authentication and multi-user support
- [ ] Mobile app (iOS/Android)
- [ ] Strava integration
- [ ] Advanced ML models for injury prevention
- [ ] Social features (share workouts, compete with friends)
- [ ] Race calendar integration
- [ ] Nutrition tracking
- [ ] Weather data integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Apple Health for providing comprehensive health data export
- Chart.js for beautiful visualizations
- Flask community for excellent documentation
- All the triathletes who inspired this project

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your Email]

## Disclaimer

This dashboard is for informational and training purposes only. Always consult with a qualified coach or medical professional before starting any intensive training program.

---

**Built with ❤️ for triathletes**

Train smart. Race strong. Finish proud. 🏁
