document.addEventListener('DOMContentLoaded', async () => {
  const urlBox = document.getElementById('currentUrl');
  const scanBtn = document.getElementById('scanBtn');
  const resultDiv = document.getElementById('result');
  const statusText = document.getElementById('statusText');
  const confText = document.getElementById('confText');
  const reasonsList = document.getElementById('reasonsList');

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
    reasonsList.innerHTML = "";

    try {
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

        // Reasons display karna
        if (data.reasons && data.reasons.length > 0) {
          data.reasons.forEach(r => {
            const li = document.createElement('li');
            li.innerText = r;
            reasonsList.appendChild(li);
          });
        }
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