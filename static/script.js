function analyze() {
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");

    if (!url) {
        resultDiv.innerHTML = "Please enter a YouTube URL";
        return;
    }

    resultDiv.innerHTML = "Analyzing comments...";

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = data.error;
        } else {
            resultDiv.innerHTML = `
                Total Comments: ${data.total_comments}<br>
                Positive: ${data.positive}<br>
                Negative: ${data.negative}<br>
                Neutral: ${data.neutral}
            `;
        }
    })
    .catch(error => {
        resultDiv.innerHTML = "Something went wrong";
    });
}
