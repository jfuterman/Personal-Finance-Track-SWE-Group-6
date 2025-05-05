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
    let stackedDataElement = document.getElementById('stackedData');


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
    if (chart) {
        chart.destroy();
    }
    
    const isStacked = type === 'stacked';
    
    const config = {
        type: 'bar',
        data: isStacked ? {
            labels: data.labels,
            datasets: data.datasets
        } : {
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
                    display: true
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
                x: {
                    stacked: isStacked,
                    grid: { display: false }
                },
                y: {
                    stacked: isStacked,
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    };
    
    chart = new Chart(ctx, config);
}
    

    // Initial chart creation
    createChart(graphData);

    // Handle time range changes
    const timeRangeSelect = document.getElementById('timeRangeSelect');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', function(e) {
            const selectedValue = e.target.value;
            if (selectedValue === 'monthly') {
                createChart(graphData, 'monthly');
            } else if (selectedValue === 'yearly') {
                createChart(yearlyData, 'yearly');
            } else if (selectedValue === 'stacked') {
                const stackedData = JSON.parse(stackedDataElement.textContent);
                createChart(stackedData, 'stacked');
            }
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