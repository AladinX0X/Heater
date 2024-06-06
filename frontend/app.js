document.addEventListener("DOMContentLoaded", function () {
    const homeButton = document.getElementById("homeButton");
    const aboutButton = document.getElementById("aboutButton");
    const contactButton = document.getElementById("contactButton");
    const infoText = document.getElementById("infoText");

    const currentTemp = document.getElementById("currentTemp");
    const status = document.getElementById("status");
    const doorStatus = document.getElementById("doorStatus");
    const currentTime = document.getElementById("currentTime");

    const ctx = document.getElementById("chart").getContext("2d");
    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Temperature in °C",
                data: [],
                borderColor: "rgba(75, 192, 192, 1)",
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: "time",
                    time: {
                        unit: 'second',  // Ensure it matches the data frequency
                        tooltipFormat: 'HH:mm:ss',
                        displayFormats: {
                            second: 'HH:mm:ss',
                            minute: 'HH:mm'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Temperature (°C)'
                    }
                }
            }
        }
    });

    homeButton.addEventListener("click", function () {
        location.reload();
    });

    aboutButton.addEventListener("click", function () {
        infoText.textContent = "This is a simple Air conditioning simulation web interface.";
    });

    contactButton.addEventListener("click", function () {
        infoText.textContent = "Email: airconditioner@simulation.com\nPhone: (123) 456-7890";
    });

    function updateData() {
        fetch("/data.json")
            .then(response => {
                console.log("Fetching data.json...");
                return response.json();
            })
            .then(data => {
                console.log("Data fetched:", data);

                currentTemp.textContent = `${data.Temperature} °C`;
                status.textContent = data.Status;
                doorStatus.textContent = data['Door Status'];
                currentTime.textContent = data.Time;

                const timeNow = new Date();  // Use the current time for labels
                chart.data.labels.push(timeNow);
                chart.data.datasets[0].data.push(parseFloat(data.Temperature));

                console.log("Chart data:", chart.data);
                chart.update();
            })
            .catch(error => {
                console.error("Error updating data:", error);
            });
    }

    updateData();
    setInterval(updateData, 1000);
});
