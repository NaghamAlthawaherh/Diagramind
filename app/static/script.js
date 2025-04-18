// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.getElementById('filePreview');
const previewImage = document.getElementById('previewImage');
const fileName = document.getElementById('fileName');
const fileMeta = document.getElementById('fileMeta');
const removeFileBtn = document.getElementById('removeFile');
const startAnalysisBtn = document.getElementById('startAnalysis');
const uploadSection = document.getElementById('uploadSection');
const processingSection = document.getElementById('processingSection');
const resultsSection = document.getElementById('resultsSection');
const progressBar = document.getElementById('progressBar');
const progressPercent = document.getElementById('progressPercent');
const currentStep = document.getElementById('currentStep');
const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const toastContainer = document.getElementById('toastContainer');

// Current state
// let uploadedFile = null;
// let mockSession = null;
// let mockRequirements = [
//     {
//         id: 'REQ-001',
//         title: 'User Login',
//         description: 'The system shall allow users to authenticate using username and password.',
//         category: 'Authentication',
//         actors: ['User'],
//         complexity: 'Low',
//         complexityValue: 20
//     },
//     {
//         id: 'REQ-002',
//         title: 'Search Products',
//         description: 'The system shall allow users to search for products using keywords.',
//         category: 'Core Functionality',
//         actors: ['User', 'Guest'],
//         complexity: 'Medium',
//         complexityValue: 50
//     },
//     {
//         id: 'REQ-003',
//         title: 'Process Payment',
//         description: 'The system shall securely process payment transactions using various payment methods.',
//         category: 'Payment',
//         actors: ['User', 'Payment Gateway'],
//         complexity: 'High',
//         complexityValue: 85
//     }
// ];
function toggleDarkMode() {
    document.body.classList.toggle("dark");
    localStorage.setItem("darkMode", document.body.classList.contains("dark"));
  }
  window.onload = () => {
    const dark = localStorage.getItem("darkMode") === "true";
    if (dark) document.body.classList.add("dark");
  };
// Initialize the application
function init() {
    dropzone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelection);
    removeFileBtn.addEventListener('click', handleRemoveFile);
    startAnalysisBtn.addEventListener('click', handleStartAnalysis);

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('border-primary', 'bg-blue-50');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('border-primary', 'bg-blue-50');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('border-primary', 'bg-blue-50');
        if (e.dataTransfer.files.length > 0) {
            handleFiles(e.dataTransfer.files);
        }
    });

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // Theme toggle
    setupThemeToggle();

    // Initialize charts if results already shown
    if (resultsSection.style.display !== 'none') {
        setupCharts();
    }
}

// Handle file selection
function handleFileSelection(e) {
    if (fileInput.files.length > 0) {
        handleFiles(fileInput.files);
    }
}

// Process selected files
function handleFiles(files) {
    const file = files[0];
    if (!file.type.startsWith('image/')) {
        showToast('Error', 'Please upload an image file (JPEG, PNG, GIF).', 'error');
        return;
    }
    if (file.size > 10 * 1024 * 1024) {
        showToast('Error', 'File size exceeds 10MB limit.', 'error');
        return;
    }
    uploadedFile = file;
    dropzone.style.display = 'none';
    filePreview.style.display = 'block';

    const objectUrl = URL.createObjectURL(file);
    previewImage.src = objectUrl;
    fileName.textContent = file.name;
    fileMeta.textContent = `${formatFileSize(file.size)} · Last modified: ${formatDate(new Date(file.lastModified))}`;
}

function formatFileSize(size) {
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    }).format(date);
}

function handleRemoveFile() {
    if (previewImage.src) URL.revokeObjectURL(previewImage.src);
    uploadedFile = null;
    previewImage.src = '';
    dropzone.style.display = 'flex';
    filePreview.style.display = 'none';
    fileInput.value = '';
}

function handleStartAnalysis() {
    if (!uploadedFile) {
        showToast('Error', 'Please upload a file first.', 'error');
        return;
    }

    uploadSection.style.display = 'none';
    processingSection.style.display = 'block';

    mockSession = {
        id: Math.floor(Math.random() * 1000),
        steps: ['upload', 'image_processing', 'ocr', 'nlp_analysis', 'estimation', 'complete'],
        currentStepIndex: 0,
        progress: 0
    };

    updateProcessingStatus();
    simulateProcessing();
}

function updateProcessingStatus() {
    if (!mockSession) return;

    const currentStepName = mockSession.steps[mockSession.currentStepIndex];
    const progress = mockSession.progress;

    progressBar.style.width = `${progress}%`;
    progressPercent.textContent = `${Math.round(progress)}%`;

    const stepDisplayNames = {
        'upload': 'File Upload',
        'image_processing': 'Image Processing',
        'ocr': 'Text Recognition',
        'nlp_analysis': 'NLP Analysis',
        'estimation': 'Estimation',
        'complete': 'Complete'
    };

    currentStep.textContent = stepDisplayNames[currentStepName] || currentStepName;

    document.querySelectorAll('.step').forEach(stepEl => {
        const stepName = stepEl.getAttribute('data-step');
        const stepIndex = mockSession.steps.indexOf(stepName);
        stepEl.classList.remove('active', 'completed');
        if (stepIndex === mockSession.currentStepIndex) stepEl.classList.add('active');
        else if (stepIndex < mockSession.currentStepIndex) stepEl.classList.add('completed');
    });
}

function simulateProcessing() {
    const intervalId = setInterval(() => {
        mockSession.progress += 2;
        if (mockSession.progress >= 100 && mockSession.currentStepIndex < mockSession.steps.length - 2) {
            mockSession.currentStepIndex++;
            mockSession.progress = 0;
        }
        updateProcessingStatus();
        if (mockSession.progress >= 100 && mockSession.currentStepIndex === mockSession.steps.length - 2) {
            clearInterval(intervalId);
            mockSession.currentStepIndex++;
            processComplete();
        }
    }, 200);
}

function processComplete() {
    processingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    populateRequirements();
    setupCharts();
    showToast('Analysis Complete', 'Your Use Case Diagram has been successfully analyzed.', 'success');
}

function populateRequirements() {
    const requirementsList = document.querySelector('.requirements-list');
    requirementsList.innerHTML = '';
    mockRequirements.forEach(req => {
        const reqElement = document.createElement('div');
        reqElement.className = 'requirement-card';
        let complexityClass = '';
        if (req.complexity === 'Low') complexityClass = 'complexity-low';
        else if (req.complexity === 'Medium') complexityClass = 'complexity-medium';
        else if (req.complexity === 'High') complexityClass = 'complexity-high';
        reqElement.innerHTML = `
            <div class="requirement-header">
                <div class="requirement-id">${req.id}</div>
                <div class="requirement-tag ${complexityClass}">${req.complexity} Complexity</div>
            </div>
            <div class="requirement-title">${req.title}</div>
            <div class="requirement-description">${req.description}</div>
            <div class="requirement-meta">
                <div class="requirement-tag">${req.category}</div>
                ${req.actors.map(actor => `<div class="requirement-tag">Actor: ${actor}</div>`).join('')}
            </div>
        `;
        requirementsList.appendChild(reqElement);
    });
}

function switchTab(tabId) {
    tabButtons.forEach(btn => {
        if (btn.getAttribute('data-tab') === tabId) btn.classList.add('active');
        else btn.classList.remove('active');
    });
    tabPanes.forEach(pane => {
        const paneId = pane.id.split('-')[0];
        if (paneId === tabId) pane.classList.add('active');
        else pane.classList.remove('active');
    });
}

function setupCharts() {
    setupEffortChart();
    setupBudgetChart();
    setupTimelineChart();
}

// setupEffortChart, setupBudgetChart, setupTimelineChart, showToast ... موجودين بالفعل وما تغيروا

// ✅ Dark Mode Toggle Logic
function setupThemeToggle() {
    const themeToggleBtn = document.getElementById('themeToggle');
    if (!themeToggleBtn) return;

    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('dark');
        themeToggleBtn.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeToggleBtn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        themeToggleBtn.innerHTML = isDark
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
}

// Run the app
document.addEventListener('DOMContentLoaded', init);