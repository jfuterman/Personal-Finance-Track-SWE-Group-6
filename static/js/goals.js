// Initialize Savings Chart
document.addEventListener('DOMContentLoaded', function() {
    initializeSavingsChart();
    setupEventListeners();
});

function initializeSavingsChart() {
    const chartCtx = document.getElementById('savingsChart').getContext('2d');
    const gradient = chartCtx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
    gradient.addColorStop(1, 'rgba(37, 99, 235, 0)');

    // Get data from the template
    const chartData = JSON.parse(document.getElementById('chart-data').textContent || '{}');
    const labels = chartData.labels || [];
    const values = chartData.values || [];

    const savingsChart = new Chart(chartCtx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                fill: true,
                borderColor: '#2563EB',
                backgroundColor: gradient,
                tension: 0.4,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return '$' + parseFloat(context.raw).toFixed(2);
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12
                        },
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        },
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: '#f0f0f0'
                    }
                }
            }
        }
    });

    return savingsChart;
}

function setupEventListeners() {
    // Handle period changes
    document.getElementById('savingsPeriod').addEventListener('change', function(e) {
        const period = e.target.value;
        fetchPeriodData(period);
    });

    document.getElementById('summaryPeriod').addEventListener('change', function(e) {
        const period = e.target.value;
        fetchSummaryData(period);
    });
}

function adjustGoal(category) {
    const modal = new bootstrap.Modal(document.getElementById('adjustGoalModal'));
    const form = document.getElementById('adjustGoalForm');
    const progressDiv = document.getElementById('goalProgress');
    
    // Update form action
    form.action = `/adjust-goal/${category}/`;
    
    // Update modal title with category
    document.querySelector('.modal-title').textContent = 
        `Adjust ${category.charAt(0).toUpperCase() + category.slice(1)} Goal`;
    
    // Get current goal data
    const goalCard = document.querySelector(`[data-category="${category}"]`);
    if (goalCard) {
        const monthlyTarget = goalCard.querySelector('.category-amount')?.textContent.replace('$', '') || '0';
        const progress = goalCard.querySelector('.progress-bar')?.style.width || '0%';
        
        // Update form fields
        form.querySelector('[name="monthly_target"]').value = parseFloat(monthlyTarget).toFixed(2);
        form.querySelector('[name="target_amount"]').value = parseFloat(monthlyTarget).toFixed(2);
        
        // Show current progress
        progressDiv.classList.remove('d-none');
        const progressValue = parseFloat(progress).toFixed(2);
        progressDiv.querySelector('.current-progress').textContent = 
            `Current Progress: ${progressValue}%`;
        progressDiv.querySelector('.progress-bar').style.width = progress;
    }
    
    modal.show();
}

async function fetchPeriodData(period) {
    try {
        const response = await fetch(`/goals/data/?period=${period}`);
        const data = await response.json();
        updateChart(data);
    } catch (error) {
        console.error('Error fetching period data:', error);
    }
}

async function fetchSummaryData(period) {
    try {
        const response = await fetch(`/goals/summary/?period=${period}`);
        const data = await response.json();
        updateSummary(data);
    } catch (error) {
        console.error('Error fetching summary data:', error);
    }
}

function updateChart(data) {
    const chart = Chart.getChart('savingsChart');
    if (chart) {
        chart.data.labels = data.labels;
        chart.data.datasets[0].data = data.values;
        chart.update();
    }
}

function updateSummary(data) {
    // Update summary card with new data
    const targetAchieved = document.querySelector('.savings-info .value');
    if (targetAchieved) {
        targetAchieved.textContent = `$${parseFloat(data.target_achieved).toFixed(2)}`;
    }

    const monthlyTarget = document.querySelectorAll('.savings-info .value')[1];
    if (monthlyTarget) {
        monthlyTarget.textContent = `$${parseFloat(data.monthly_target).toFixed(2)}`;
    }

    // Update progress bar
    const progressBar = document.querySelector('.progress-bar');
    const progressLabel = document.querySelector('.progress-labels span:first-child');
    if (progressBar && progressLabel) {
        const progress = parseFloat(data.progress).toFixed(2);
        progressBar.style.width = `${progress}%`;
        progressLabel.textContent = `Progress: ${progress}%`;
    }
} 