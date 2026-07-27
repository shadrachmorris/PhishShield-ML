function switchTab(tab) {
    const urlForm = document.getElementById('urlForm');
    const imgForm = document.getElementById('imgForm');
    const urlBtn = document.getElementById('urlTabBtn');
    const imgBtn = document.getElementById('imgTabBtn');
    const results = document.getElementById('results');

    results.classList.add('hidden');

    if (tab === 'url') {
        urlForm.classList.remove('hidden');
        imgForm.classList.add('hidden');
        urlBtn.className = "px-4 py-2 text-sm font-semibold rounded-lg bg-cyber-accent text-cyber-900 transition";
        imgBtn.className = "px-4 py-2 text-sm font-semibold rounded-lg text-gray-400 hover:text-white transition";
    } else {
        imgForm.classList.remove('hidden');
        urlForm.classList.add('hidden');
        imgBtn.className = "px-4 py-2 text-sm font-semibold rounded-lg bg-cyber-accent text-cyber-900 transition";
        urlBtn.className = "px-4 py-2 text-sm font-semibold rounded-lg text-gray-400 hover:text-white transition";
    }
}

function updateFileName(input) {
    if (input.files.length > 0) {
        document.getElementById('fileName').innerText = `Selected File: ${input.files[0].name}`;
    }
}

async function handleUrlSubmit(e) {
    e.preventDefault();
    const url = document.getElementById('urlInput').value;
    const formData = new FormData();
    formData.append('url', url);

    showLoading(true);
    try {
        const res = await fetch('/api/v1/scan-url', { method: 'POST', body: formData });
        const data = await res.json();
        displayResult(data);
    } catch (err) {
        alert('Server Error: Failed to complete URL scan.');
    } finally {
        showLoading(false);
    }
}

async function handleImgSubmit(e) {
    e.preventDefault();
    const fileInput = document.getElementById('imgInput');
    if (!fileInput.files.length) return alert('Please attach a screenshot file first.');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    showLoading(true);
    try {
        const res = await fetch('/api/v1/scan-image', { method: 'POST', body: formData });
        const data = await res.json();
        if (res.status !== 200) {
            alert(data.error || 'Failed to extract valid URL from image.');
        } else {
            displayResult(data);
        }
    } catch (err) {
        alert('Server Error: Failed to process image.');
    } finally {
        showLoading(false);
    }
}

function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    if (isLoading) {
        loading.classList.remove('hidden');
        results.classList.add('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

function displayResult(data) {
    const container = document.getElementById('results');
    container.classList.remove('hidden');

    const confPercentage = data.confidence ? (data.confidence * 100).toFixed(1) + '%' : 'N/A';

    if (data.is_phishing) {
        container.className = "mt-8 p-6 rounded-xl border border-red-500/50 bg-red-950/30 text-red-200";
        container.innerHTML = `
            <div class="flex items-start justify-between">
                <div>
                    <span class="inline-block px-3 py-1 bg-red-500/20 text-red-400 border border-red-500/30 font-bold text-xs uppercase tracking-wider rounded-full mb-2">High Risk Phishing</span>
                    <h3 class="font-bold text-xl text-red-400 mb-1">${data.status}</h3>
                    <p class="text-sm opacity-80 break-all font-mono bg-black/40 px-3 py-1.5 rounded-lg border border-red-900/50 mt-2">${data.scanned_url}</p>
                </div>
                <div class="text-right">
                    <span class="block text-xs uppercase text-gray-400">Confidence</span>
                    <span class="text-2xl font-extrabold text-red-400">${confPercentage}</span>
                </div>
            </div>
        `;
    } else {
        container.className = "mt-8 p-6 rounded-xl border border-emerald-500/50 bg-emerald-950/30 text-emerald-200";
        container.innerHTML = `
            <div class="flex items-start justify-between">
                <div>
                    <span class="inline-block px-3 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold text-xs uppercase tracking-wider rounded-full mb-2">Safe Resource</span>
                    <h3 class="font-bold text-xl text-emerald-400 mb-1">${data.status}</h3>
                    <p class="text-sm opacity-80 break-all font-mono bg-black/40 px-3 py-1.5 rounded-lg border border-emerald-900/50 mt-2">${data.scanned_url}</p>
                </div>
                <div class="text-right">
                    <span class="block text-xs uppercase text-gray-400">Confidence</span>
                    <span class="text-2xl font-extrabold text-emerald-400">${confPercentage}</span>
                </div>
            </div>
        `;
    }
}