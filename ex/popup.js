document.addEventListener('DOMContentLoaded', async () => {
  const urlBox = document.getElementById('currentUrl');
  const scanBtn = document.getElementById('scanBtn');
  const resultDiv = document.getElementById('result');
  const statusText = document.getElementById('statusText');
  const confText = document.getElementById('confText');

  // Currently open tab ka URL uthana
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const currentUrl = tab ? tab.url : "";
  urlBox.innerText = currentUrl || "No URL detected";

  scanBtn.addEventListener('click', async () => {
    if (!currentUrl || currentUrl.startsWith('chrome://')) {
      alert('Is page ko scan nahi kiya ja sakta!');
      return;
    }

    scanBtn.innerText = "Scanning...";
    scanBtn.disabled = true;

    try {
      // Local FastAPI server ko call karna
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: currentUrl })
      });

      const data = await response.json();

      resultDiv.style.display = 'block';
      if (data.is_phishing) {
        resultDiv.className = 'phishing';
        statusText.innerText = '⚠️ WARNING: Phishing Detected!';
      } else {
        resultDiv.className = 'safe';
        statusText.innerText = '✅ SAFE: Legit Website';
      }
      confText.innerText = `Confidence: ${data.confidence}%`;

    } catch (err) {
      alert('Error: Backend server run nahi ho raha!');
      console.error(err);
    } finally {
      scanBtn.innerText = "Scan This Website";
      scanBtn.disabled = false;
    }
  });
});