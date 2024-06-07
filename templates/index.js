let conversationText = '';
let myChart;

function uploadFile() {
    const input = document.getElementById('fileInput');
    const file = input.files[0];
    const reader = new FileReader();
    
    reader.onload = function (e) {
        conversationText = e.target.result;
        document.getElementById('conversationContent').textContent = conversationText;
        document.getElementById('conversation').style.display = 'block';
        classifyData(conversationText);
    };
    
    reader.readAsText(file);
}

function classifyData(data) {
    fetch('http://localhost:5000/classify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: data }),
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('result').innerText = JSON.stringify(result.result, null, 2);
        displayChart(result.result);
    });
}

function displayChart(result) {
    const labels = Object.keys(result);
    const values = Object.values(result);
    
    const ctx = document.getElementById('myChart').getContext('2d');

    if (myChart) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Voice Phishing Cases',
                data: values,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function toggleConversation() {
    const conversationDiv = document.getElementById('conversationContent');
    if (conversationDiv.style.display === 'none') {
        conversationDiv.style.display = 'block';
    } else {
        conversationDiv.style.display = 'none';
    }
}