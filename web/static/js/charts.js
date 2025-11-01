// Charts initialization for Ironman Training Dashboard

// Check if Chart.js is loaded
if (typeof Chart !== 'undefined') {
    initializeCharts();
} else {
    console.error('Chart.js not loaded');
}

async function initializeCharts() {
    try {
        // Fetch chart data from API
        const response = await fetch('/api/chart-data');
        if (!response.ok) {
            console.log('No chart data available yet');
            return;
        }

        const data = await response.json();

        // Initialize Progress Chart
        const progressCtx = document.getElementById('progressChart');
        if (progressCtx && data.weekly_progress) {
            createProgressChart(progressCtx, data.weekly_progress);
        }

        // Initialize Pace Trend Chart
        const paceCtx = document.getElementById('paceChart');
        if (paceCtx && data.pace_trend) {
            createPaceTrendChart(paceCtx, data.pace_trend);
        }
    } catch (error) {
        console.error('Error loading chart data:', error);
    }
}

function createProgressChart(ctx, progressData) {
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: progressData.labels || ['Swimming', 'Cycling', 'Running'],
            datasets: [
                {
                    label: 'Current Week (km)',
                    data: progressData.current || [0, 0, 0],
                    backgroundColor: 'rgba(26, 115, 232, 0.8)',
                    borderColor: 'rgba(26, 115, 232, 1)',
                    borderWidth: 2
                },
                {
                    label: 'Ironman Target (km)',
                    data: progressData.target || [3.86, 180.25, 42.2],
                    backgroundColor: 'rgba(234, 67, 53, 0.8)',
                    borderColor: 'rgba(234, 67, 53, 1)',
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            label += context.parsed.y.toFixed(2) + ' km';
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Distance (km)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value + ' km';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Activity'
                    }
                }
            }
        }
    });
}

function createPaceTrendChart(ctx, paceData) {
    const labels = paceData.labels || [];
    const data = paceData.data || [];

    // If no data, show message
    if (labels.length === 0) {
        ctx.getContext('2d').font = '16px Arial';
        ctx.getContext('2d').fillText('No pace data available yet', 10, 50);
        return;
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Pace (min/km)',
                data: data,
                borderColor: 'rgba(52, 168, 83, 1)',
                backgroundColor: 'rgba(52, 168, 83, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: 'rgba(52, 168, 83, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Pace: ' + context.parsed.y.toFixed(2) + ' min/km';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    reverse: true, // Lower pace is better
                    title: {
                        display: true,
                        text: 'Pace (min/km)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1) + ' min/km';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            }
        }
    });
}

// Export functions for use in dashboard
window.initializeCharts = initializeCharts;
