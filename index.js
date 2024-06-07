function uploadCSV() {
    const fileInput = document.getElementById('csvFileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const csvData = e.target.result;
            sendCSVToServer(csvData);
        };
        reader.readAsText(file);
    } else {
        alert('Please upload a CSV file.');
    }
}

function sendCSVToServer(csvData) {
    fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/csv',
        },
        body: csvData,
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        displayResults(data);
    })
}



function displayResults(data) {
    const resultsDiv = document.createElement('div');
    resultsDiv.innerHTML = '<h2>Prediction Results</h2>';

    const table = document.createElement('table');
    table.border = '1';
    
    const headerRow = document.createElement('tr');
    const headers = ['Actual', 'Predicted'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.appendChild(document.createTextNode(headerText));
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);
    
    data.forEach(row => {
        const dataRow = document.createElement('tr');
        Object.values(row).forEach(text => {
            const cell = document.createElement('td');
            cell.appendChild(document.createTextNode(text));
            dataRow.appendChild(cell);
        });
        table.appendChild(dataRow);
    });

    resultsDiv.appendChild(table);
    document.body.appendChild(resultsDiv);
}
