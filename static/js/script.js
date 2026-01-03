function showLoader() {
    document.getElementById("loader").style.display = "block";
}

if (document.getElementById("chart")) {
    new Chart(document.getElementById("chart"), {
        type: 'bar',
        data: {
            labels: ['Yield'],
            datasets: [{
                label: 'Predicted Yield',
                data: [parseFloat(document.querySelector("h3").innerText)],
            }]
        }
    });
}
