(function () {
    const ctx = document.getElementById('activityChart').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(255, 99, 132, 0.4)');
    gradient.addColorStop(1, 'rgba(255, 99, 132, 0)');

    const data = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
        datasets: [{
            label: 'Activity',
            data: [200, 458, 588, 697, 825, 1055, 1760],
            backgroundColor: gradient,
            borderColor: '#ff5470',
            pointBackgroundColor: '#ff5470',
            pointBorderColor: '#ffffff',
            pointRadius: 5,
            pointHoverRadius: 7,
            pointHoverBorderWidth: 3,
            tension: 0.4, // Smooth curve
            borderWidth: 2,
            fill: true,
        }]
    };

    const options = {
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: '#3c3b45',
                titleColor: '#ffffff',
                bodyColor: '#ffffff',
                borderColor: '#ff5470',
                borderWidth: 1,
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    display: false
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: '#3c3b45'
                },
                ticks: {
                    color: '#a0a0a0'
                }
            }
        }
    };

    const activityChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });
})();
