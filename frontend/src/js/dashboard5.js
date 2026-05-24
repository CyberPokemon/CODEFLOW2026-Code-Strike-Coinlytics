const BASE_URL =
  "https://coindeployment-357779294190.asia-south1.run.app";

const TOKEN = sessionStorage.getItem("coinlytics_token");

let pieChartInstance = null;
let barChartInstance = null;

// Logout
function logoutUser() {
  sessionStorage.removeItem("coinlytics_token");
  window.location.href = "index.html";
}

// Load uploaded files initially
window.onload = function () {
  fetchFiles();
};

// Upload File
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a CSV file");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("uploadStatus").innerText =
    "Uploading...";

  try {
    await fetch(`${BASE_URL}/api/files/upload?=null`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${TOKEN}`,
      },
      body: formData,
    });

    document.getElementById("uploadStatus").innerText =
      "Upload Successful";

    fetchFiles();
  } catch (error) {
    console.error(error);

    document.getElementById("uploadStatus").innerText =
      "Upload Failed";
  }
}

// Fetch Uploaded Files
async function fetchFiles() {
  try {
    const response = await fetch(
      `${BASE_URL}/api/files/getfiles`,
      {
        headers: {
          Authorization: `Bearer ${TOKEN}`,
        },
      }
    );

    const files = await response.json();

    const tableBody =
      document.getElementById("filesTableBody");

    tableBody.innerHTML = "";

    files.forEach((file) => {
      const uploadedTime = new Date(
        file.uploadedAt
      ).toLocaleString();
      
      const expiryTime = new Date(
        file.encryptedExpiryAt
      ).toLocaleString();
      
      const row = `
        <tr>
          <td>${file.fileNo}</td>
      
          <td>${file.originalFilename}</td>
      
          <td>${uploadedTime}</td>
      
          <td>${expiryTime}</td>
      
          <td>
            <button onclick="analyzeFile(${file.fileNo})">
              Analyze
            </button>
          </td>
        </tr>
      `;

      tableBody.innerHTML += row;
    });
  } catch (error) {
    console.error(error);
  }
}

// Analyze File
async function analyzeFile(fileNo) {
  try {
    const response = await fetch(
      `${BASE_URL}/api/ai/analyze/${fileNo}`,
      {
        headers: {
          Authorization: `Bearer ${TOKEN}`,
        },
      }
    );

    const data = await response.json();

    displayAnalysis(data);
  } catch (error) {
    console.error(error);
  }
}

// Display Analysis
function displayAnalysis(data) {
  document.getElementById(
    "analysisSection"
  ).style.display = "block";

  // Health Score
  document.getElementById(
    "healthScore"
  ).innerText =
    data.type_5_health_score.score + "/100";

  const insightsContainer =
    document.getElementById("healthInsights");

  insightsContainer.innerHTML = "";

  data.type_5_health_score.insights.forEach(
    (insight) => {
      insightsContainer.innerHTML += `
        <p>• ${insight}</p>
      `;
    }
  );

  // Category Data
  const categories =
    data.type_2_category_statistics.category_statistics;

  const labels = categories.map((c) => c.category);

  const debitData = categories.map(
    (c) => c.total_debit
  );

  // Pie Chart
  createPieChart(labels, debitData);

  // Bar Chart
  createBarChart(categories);

  // Statistics Table
  const statsBody =
    document.getElementById("statsTableBody");

  statsBody.innerHTML = "";

  categories.forEach((item) => {
    statsBody.innerHTML += `
      <tr>
        <td>${item.category}</td>
        <td>₹${item.total_credit.toLocaleString()}</td>
        <td>₹${item.total_debit.toLocaleString()}</td>
        <td>₹${item.net_amount.toLocaleString()}</td>
        <td>${item.transaction_count}</td>
      </tr>
    `;
  });

  // Anomalies
  const anomaliesContainer =
    document.getElementById("anomaliesContainer");

  anomaliesContainer.innerHTML = "";

  data.type_3_anomalies.forEach((anomaly) => {
    anomaliesContainer.innerHTML += `
      <div class="anomaly-card">
        <h3>${anomaly.transaction_statement}</h3>

        <p>
          <strong>Category:</strong>
          ${anomaly.predicted_category}
        </p>

        <p>
          <strong>Reason:</strong>
          ${anomaly.anomaly_reason}
        </p>

        <p>
          <strong>Confidence:</strong>
          ${(anomaly.confidence * 100).toFixed(1)}%
        </p>
      </div>
    `;
  });
}

// Pie Chart
function createPieChart(labels, data) {
  const ctx =
    document.getElementById("pieChart").getContext("2d");

  if (pieChartInstance) {
    pieChartInstance.destroy();
  }

  pieChartInstance = new Chart(ctx, {
    type: "pie",

    data: {
      labels: labels,

      datasets: [
        {
          data: data,
          backgroundColor: [
            "#3b82f6",
            "#10b981",
            "#f59e0b",
            "#ef4444",
          ],
        },
      ],
    },
  });
}

// Bar Chart
function createBarChart(categories) {
  const ctx =
    document.getElementById("barChart").getContext("2d");

  if (barChartInstance) {
    barChartInstance.destroy();
  }

  barChartInstance = new Chart(ctx, {
    type: "bar",

    data: {
      labels: categories.map((c) => c.category),

      datasets: [
        {
          label: "Credit",
          data: categories.map((c) => c.total_credit),
          backgroundColor: "#3b82f6",
        },
        {
          label: "Debit",
          data: categories.map((c) => c.total_debit),
          backgroundColor: "#ef4444",
        },
      ],
    },

    options: {
      responsive: true,

      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}