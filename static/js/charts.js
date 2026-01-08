let vitalsChart = null;

/* Initialize empty chart */
function initChart() {
    const ctx = document.getElementById("vitalsChart");
    if (!ctx) return;

    vitalsChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [
                "Pregnancies",
                "Glucose",
                "Blood Pressure",
                "Skin Thickness",
                "Insulin",
                "BMI",
                "DPF",
                "Age"
            ],
            datasets: [{
                label: "Patient Values",
                data: [],
                backgroundColor: [
                    "#00ff9c",
                    "#ff4b4b",
                    "#00ff9c",
                    "#00ff9c",
                    "#00ff9c",
                    "#ff4b4b",
                    "#ffd84d",
                    "#00ff9c"
                ],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "#9fffe0",
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#9fffe0",
                        font: { size: 11 }
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#9fffe0"
                    },
                    grid: {
                        color: "rgba(0,255,156,0.15)"
                    }
                }
            }
        }
    });
}

/* Update chart with patient values */
function updateChartFromInputs(values) {
    if (!vitalsChart) return;

    vitalsChart.data.datasets[0].data = values;
    vitalsChart.update();
}
