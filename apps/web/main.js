const API_BASE_URL = window.NEUROLIFT_API_URL || "http://localhost:8000";

const healthOutput = document.getElementById("health-output");
const demoOutput = document.getElementById("demo-output");

async function callApi(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

document.getElementById("health-btn").addEventListener("click", async () => {
  healthOutput.textContent = "Loading...";
  try {
    const payload = await callApi("/health");
    healthOutput.textContent = JSON.stringify(payload, null, 2);
  } catch (error) {
    healthOutput.textContent = `Failed: ${error.message}`;
  }
});

document.getElementById("demo-btn").addEventListener("click", async () => {
  demoOutput.textContent = "Running demo...";
  try {
    const payload = await callApi("/sessions/demo-run");
    demoOutput.textContent = JSON.stringify(payload, null, 2);
  } catch (error) {
    demoOutput.textContent = `Failed: ${error.message}`;
  }
});
