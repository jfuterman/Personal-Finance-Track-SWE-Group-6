document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing expenses page...');
    try {
        initializeExpensesChart();
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing expenses page:', error);
    }
});

function initializeExpensesChart() {
    console.log('Initializing expenses chart...');
    const canvas = document.getElementById('expensesChart');
    if (!canvas) {
        console.error('Could not find expenses chart canvas element');
        return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Could not get 2D context from canvas');
        return;
    }

    let graphDataElement = document.getElementById('graphData');
    let yearlyDataElement = document.getElementById('yearlyData');

    if (!graphDataElement || !yearlyDataElement) {
        console.error('Could not find graph data elements');
        return;
    }

    console.log('Parsing graph data...');
    const graphData = JSON.parse(graphDataElement.textContent);
    const yearlyData = JSON.parse(yearlyDataElement.textContent);

    console.log('Monthly data:', graphData);
    console.log('Yearly data:', yearlyData);
    
    let chart = null;

    function createChart(data, type = 'monthly') {
        console.log(`Creating ${type} chart...`);
        if (chart) {
            console.log('Destroying existing chart...');
            chart.destroy();
        }

        const chartConfig = {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: type === 'monthly' ? 'Monthly Expenses' : 'Yearly Expenses',
                    data: data.values,
                    backgroundColor: '#0d6efd',
                    borderColor: '#0d6efd',
                    borderWidth: 1,
                    borderRadius: 4,
                    barThickness: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.raw.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            display: true,
                            color: '#f1f5f9'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            },
                            font: {
                                size: 11
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 11
                            }
                        }
                    }
                }
            }
        };

        console.log('Chart configuration:', chartConfig);
        chart = new Chart(ctx, chartConfig);
    }

    // Initial chart creation
    createChart(graphData);

    // Handle time range changes
    const timeRangeSelect = document.getElementById('timeRangeSelect');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', function(e) {
            console.log('Time range changed:', e.target.value);
            const selectedValue = e.target.value;
            createChart(selectedValue === 'monthly' ? graphData : yearlyData, selectedValue);
        });
    } else {
        console.error('Could not find time range select element');
    }
}

function setupEventListeners() {
    // Add click handlers for expense cards
    const expenseCards = document.querySelectorAll('.expense-card');
    expenseCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            toggleDetails(category);
        });
    });
}

function toggleDetails(category) {
    const detailsElement = document.getElementById(`${category}-details`);
    if (detailsElement) {
        detailsElement.classList.toggle('show');
    }
} 