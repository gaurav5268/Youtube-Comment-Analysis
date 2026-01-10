let svmChart = null;
let vaderChart = null;

function analyze() {
    const url = document.getElementById("url").value;

    if (!url) {
        alert("Please enter a YouTube URL");
        return;
    }

    document.getElementById("loader").classList.remove("hidden");
    document.getElementById("chartsSection").classList.add("hidden");

    fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("loader").classList.add("hidden");

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById("total").innerText =
            `Total Comments: ${data.total_comments}`;

        // ===== SVM =====
        const svm = data.svm;

        document.getElementById("svm_positive").innerText =
            `Positive: ${svm.Positive}`;
        document.getElementById("svm_neutral").innerText =
            `Neutral: ${svm.Neutral}`;
        document.getElementById("svm_negative").innerText =
            `Negative: ${svm.Negative}`;

        if (svmChart) svmChart.destroy();
        svmChart = new Chart(document.getElementById("svmChart"), {
            type: "pie",
            data: {
                labels: ["Positive", "Neutral", "Negative"],
                datasets: [{
                    data: [svm.Positive, svm.Neutral, svm.Negative],
                    backgroundColor: ["#4CAF50", "#FFC107", "#F44336"]
                }]
            }
        });

        // ===== VADER =====
        const vader = data.vader;

        document.getElementById("vader_positive").innerText =
            `Positive: ${vader.Positive}`;
        document.getElementById("vader_neutral").innerText =
            `Neutral: ${vader.Neutral}`;
        document.getElementById("vader_negative").innerText =
            `Negative: ${vader.Negative}`;

        if (vaderChart) vaderChart.destroy();
        vaderChart = new Chart(document.getElementById("vaderChart"), {
            type: "pie",
            data: {
                labels: ["Positive", "Neutral", "Negative"],
                datasets: [{
                    data: [vader.Positive, vader.Neutral, vader.Negative],
                    backgroundColor: ["#2196F3", "#9E9E9E", "#E91E63"]
                }]
            }
        });

        document.getElementById("chartsSection").classList.remove("hidden");
    })
    .catch(err => {
        document.getElementById("loader").classList.add("hidden");
        console.error(err);
        alert("Something went wrong");
    });
}
