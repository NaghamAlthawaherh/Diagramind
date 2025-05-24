
// ------------------------------
// 📌 DOM Elements
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
const elementsGrid = document.getElementById('elementsGrid');
const calculateUFPBtn = document.getElementById('calculateUFP');
const resetFormBtn = document.getElementById('resetForm');
const adjustmentQuestionsList = document.getElementById('adjustmentQuestions');
const calculateFinalEstimationBtn = document.getElementById('calculateFinalEstimation');

// 🔵 New Elements for Enhanced Features
const themeToggle = document.getElementById('themeToggle');
const languageToggle = document.getElementById('languageToggle');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const closeModalBtn = document.querySelector('.close-btn');
const userProfile = document.getElementById('userProfile');
const usernameDisplay = document.getElementById('usernameDisplay');
const userRoleDisplay = document.getElementById('userRoleDisplay');
const roleSelect = document.getElementById('roleSelect');

// 📂 Placeholder Detected Elements
const detectedElements = [
  { img: 'crop1.jpg' },
  { img: 'crop2.jpg' },
  { img: 'crop3.jpg' }
];

// 📈 Function Points Weights
const weights = {
  Input: { Simple: 2, Average: 4, Complex: 6 },
  Output: { Simple: 3, Average: 5, Complex: 7 },
  File: { Simple: 5, Average: 10, Complex: 15 },
  Inquiry: { Simple: 2, Average: 4, Complex: 6 },
  Interface: { Simple: 4, Average: 7, Complex: 10 }
};

// 🧩 GSC Questions
const gscQuestions = [
  "Will the application use data communications?",
  "Are data or functions distributed?",
  "Are there specific performance objectives?",
  "Will the application run on heavily used configurations?",
  "Will the transaction rate be high?",
  "Will there be online data entry?",
  "Will the application be designed for end-user efficiency?",
  "Will there be online updates?",
  "Is complex processing logic involved?",
  "Is there an intent to provide usability for other applications?",
  "How important is installation ease and conversion?",
  "How important is operational ease?",
  "Will the application be accessed from multiple sites?",
  "Is there an intent with the design to facilitate change?"
];

// 🌍 Internationalization (i18n)
const translations = {
  en: {
    dashboard: "Dashboard",
    wizard_mode: "Wizard Mode",
    upload_diagram: "Upload Diagram",
    requirements: "Requirements",
    effort_estimation: "Effort Estimation",
    budget_prediction: "Budget Prediction",
    timeline: "Timeline",
    reports: "Reports",
    documentation: "Documentation",
    support: "Support",
    use_case_analyzer: "Use Case Diagram Analyzer",
    analyzer_description: "Automatically extract functional requirements and estimate project effort from Use Case Diagrams.",
    upload_file: "Upload a file",
    or: "or",
    drag_drop: "drag and drop",
    file_types: "PNG, JPG, GIF up to 10MB",
    remove: "Remove",
    last_modified: "Last modified",
    today: "Today",
    start_analysis: "Start Analysis",
    processing_diagram: "Processing Diagram",
    processing_description: "Your diagram is being analyzed",
    upload: "Upload",
    image_processing: "Image Preprocessing",
    object_detection: "Object Detection",
    classification: "Element Classification",
    estimation: "Effort Estimation",
    extracted_requirements: "Extracted Requirements",
    calculate_ufp: "Calculate UFP",
    reset: "Reset",
    adjustment_questions: "Adjustment Questions",
    project_assumptions: "Project Assumptions",
    productivity: "Average Productivity (FP/Month)",
    average_salary: "Average Salary ($/Month)",
    calculate_estimation: "Calculate Final Estimation",
    function_points: "Function Points",
    adjusted_fp: "Adjusted FP",
    estimated_hours: "Estimated Hours",
    team_size: "Team Size",
    budget_prediction: "Budget Prediction",
    minimum_budget: "Minimum Budget",
    maximum_budget: "Maximum Budget",
    project_timeline: "Project Timeline",
    estimated_duration: "Estimated Duration",
    results: "Results",
    estimates: "Estimates",
    select_type: "Select Type",
    select_complexity: "Select Complexity",
    agile_breakdown: "Agile Breakdown",
    scrum_sprints: "Scrum Sprints",
    xp_iterations: "XP Iterations",
    completion_percentage: "Completion %",
    effort: "Effort",
    login: "Login",
    logout: "Logout",
    select_role: "Select your role",
    developer: "Developer",
    student: "Student",
    project_manager: "Project Manager",
    other: "Other",
    welcome: "Welcome"
  },
  ar: {
    dashboard: "لوحة التحكم",
    wizard_mode: "وضع المعالج",
    upload_diagram: "رفع المخطط",
    requirements: "المتطلبات",
    effort_estimation: "تقدير الجهد",
    budget_prediction: "توقع الميزانية",
    timeline: "الجدول الزمني",
    reports: "التقارير",
    documentation: "التوثيق",
    support: "الدعم",
    use_case_analyzer: "محلل مخطط حالات الاستخدام",
    analyzer_description: "استخراج المتطلبات الوظيفية وتقدير جهد المشروع تلقائياً من مخططات حالات الاستخدام.",
    upload_file: "رفع ملف",
    or: "أو",
    drag_drop: "سحب وإفلات",
    file_types: "PNG, JPG, GIF حتى 10MB",
    remove: "إزالة",
    last_modified: "آخر تعديل",
    today: "اليوم",
    start_analysis: "بدء التحليل",
    processing_diagram: "معالجة المخطط",
    processing_description: "جاري تحليل المخطط الخاص بك",
    upload: "رفع",
    image_processing: "معالجة الصورة",
    object_detection: "كشف العناصر",
    classification: "تصنيف العناصر",
    estimation: "تقدير الجهد",
    extracted_requirements: "المتطلبات المستخرجة",
    calculate_ufp: "حساب UFP",
    reset: "إعادة تعيين",
    adjustment_questions: "أسئلة التعديل",
    project_assumptions: "افتراضات المشروع",
    productivity: "متوسط الإنتاجية (FP/شهر)",
    average_salary: "متوسط الراتب ($/شهر)",
    calculate_estimation: "حساب التقدير النهائي",
    function_points: "نقاط الوظيفة",
    adjusted_fp: "نقاط الوظيفة المعدلة",
    estimated_hours: "الساعات المقدرة",
    team_size: "حجم الفريق",
    budget_prediction: "توقع الميزانية",
    minimum_budget: "الحد الأدنى للميزانية",
    maximum_budget: "الحد الأقصى للميزانية",
    project_timeline: "الجدول الزمني للمشروع",
    estimated_duration: "المدة المقدرة",
    results: "النتائج",
    estimates: "التقديرات",
    select_type: "اختر النوع",
    select_complexity: "اختر التعقيد",
    agile_breakdown: "تفصيل أجايل",
    scrum_sprints: "سباقات سكروم",
    xp_iterations: "تكرارات XP",
    completion_percentage: "نسبة الإكمال %",
    effort: "الجهد",
    login: "تسجيل الدخول",
    logout: "تسجيل خروج",
    select_role: "اختر دورك",
    developer: "مطور",
    student: "طالب",
    project_manager: "مدير مشروع",
    other: "أخرى",
    welcome: "مرحباً"
  }
};

// Initialize i18next
function initI18n() {
  i18next.init({
    lng: localStorage.getItem('language') || 'en',
    resources: translations,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  }, function(err, t) {
    if (err) {
      console.error('Error initializing i18n:', err);
      return;
    }
    updateContent();
  });
}

function updateContent() {
  document.querySelectorAll('[data-i18n]').forEach(element => {
    const key = element.getAttribute('data-i18n');
    element.textContent = i18next.t(key);
  });
}

// ------------------------------
// 🎨 Theme Management
function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  // Update icon
  themeToggle.innerHTML = newTheme === 'dark' ? 
    '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

function initTheme() {
  const savedTheme = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', savedTheme);
  themeToggle.innerHTML = savedTheme === 'dark' ? 
    '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

// ------------------------------
// 🌐 Language Management
function toggleLanguage() {
  const currentLang = document.documentElement.getAttribute('data-lang');
  const newLang = currentLang === 'en' ? 'ar' : 'en';
  
  document.documentElement.setAttribute('data-lang', newLang);
  document.documentElement.setAttribute('dir', newLang === 'ar' ? 'rtl' : 'ltr');
  localStorage.setItem('language', newLang);
  
  i18next.changeLanguage(newLang, () => {
    updateContent();
    setupCharts(); // Update charts with new language
  });
}

function initLanguage() {
  const savedLang = localStorage.getItem('language') || 'en';
  document.documentElement.setAttribute('data-lang', savedLang);
  document.documentElement.setAttribute('dir', savedLang === 'ar' ? 'rtl' : 'ltr');
}

// ------------------------------
// 👤 User Authentication with Role Management
function handleLogin(e) {
  e.preventDefault();
  const username = loginForm.querySelector('input[type="text"]').value;
  const role = roleSelect.value;
  
  if (!username || !role) {
    showToast('Error', 'Please enter both username and select a role.', 'error');
    return;
  }

  // Simulate login with role
  localStorage.setItem('isLoggedIn', 'true');
  localStorage.setItem('username', username);
  localStorage.setItem('userRole', role);
  
  loginModal.style.display = 'none';
  updateUserProfile();
  applyRoleBasedUI(role);
  showToast('Success', `Welcome ${username} (${role})!`, 'success');
}

function handleLogout() {
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('username');
  localStorage.removeItem('userRole');
  updateUserProfile();
  resetRoleBasedUI();
  showToast('Success', 'You have been logged out.', 'success');
}

function updateUserProfile() {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
  const username = localStorage.getItem('username');
  const role = localStorage.getItem('userRole');
  
  if (isLoggedIn && username && role) {
    loginBtn.style.display = 'none';
    logoutBtn.style.display = 'block';
    userProfile.style.display = 'flex';
    usernameDisplay.textContent = username;
    userRoleDisplay.textContent = role;
    userRoleDisplay.className = `role-badge role-${role.toLowerCase().replace(' ', '-')}`;
  } else {
    loginBtn.style.display = 'block';
    logoutBtn.style.display = 'none';
    userProfile.style.display = 'none';
  }
}

function applyRoleBasedUI(role) {
  // Remove any existing role classes
  document.body.classList.remove(
    'role-developer',
    'role-student',
    'role-project-manager',
    'role-other'
  );
  
  // Add the current role class
  document.body.classList.add(`role-${role.toLowerCase().replace(' ', '-')}`);
  
  // Apply role-specific UI changes
  switch(role.toLowerCase()) {
    case 'developer':
      // Developer-specific UI changes
      break;
    case 'project manager':
      // PM-specific UI changes
      break;
    case 'student':
      // Student-specific UI changes
      break;
    default:
      // Default UI for other roles
  }
}

function resetRoleBasedUI() {
  // Remove all role-specific classes
  document.body.classList.remove(
    'role-developer',
    'role-student',
    'role-project-manager',
    'role-other'
  );
}

// ------------------------------
// 📁 File Upload
function handleFileSelection() {
  if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    if (!file.type.startsWith('image/')) return showToast('Error', 'Only image files allowed.', 'error');

    const reader = new FileReader();
    reader.onload = function (e) {
      const base64Image = e.target.result;
      previewImage.src = base64Image;
      filePreview.style.display = 'block';
      dropzone.style.display = 'none';
      fileName.textContent = file.name;
      fileMeta.textContent = `${(file.size / 1024).toFixed(1)} KB`;
      localStorage.setItem('uploadedDiagram', base64Image);
    };
    reader.readAsDataURL(file);
  }
}

function handleRemoveFile() {
  fileInput.value = '';
  previewImage.src = '';
  filePreview.style.display = 'none';
  dropzone.style.display = 'flex';
}

// ▶️ Start Analysis
function handleStartAnalysis() {
  if (!fileInput.files.length) return showToast('Error', 'Please upload a file first.', 'error');

  uploadSection.style.display = 'none';
  processingSection.style.display = 'block';

  let progress = 0;
  const steps = ['upload', 'image_processing', 'object_detection', 'classification', 'estimation'];

  const interval = setInterval(() => {
    progress += 20;
    progressBar.style.width = `${progress}%`;
    progressPercent.textContent = `${progress}%`;

    const stepIndex = Math.floor(progress / 20) - 1;
    if (stepIndex >= 0 && steps[stepIndex]) {
      currentStep.textContent = i18next.t(steps[stepIndex]);

      document.querySelectorAll('.step').forEach((step, index) => {
        if (index < stepIndex) step.classList.add('completed'), step.classList.remove('active');
        else if (index === stepIndex) step.classList.add('active'), step.classList.remove('completed');
        else step.classList.remove('active', 'completed');
      });
    }

    if (progress >= 100) {
      clearInterval(interval);
      setTimeout(() => {
        processingSection.style.display = 'none';
        resultsSection.style.display = 'block';
        populateDetectedElements();
        populateAdjustmentQuestions();
        setupCharts();
        showToast('Success', 'Analysis Complete.', 'success');
      }, 500);
    }
  }, 500);
}

// 🔵 Populate Detected Elements
function populateDetectedElements() {
  elementsGrid.innerHTML = '';
  detectedElements.forEach((el, index) => {
    const card = document.createElement('div');
    card.className = 'element-card';
    card.innerHTML = `
      <img src="${el.img}" alt="Detected ${index + 1}">
      <select class="type-select">
        <option value="">${i18next.t('select_type')}</option>
        <option value="Input">Input</option>
        <option value="Output">Output</option>
        <option value="File">File</option>
        <option value="Inquiry">Inquiry</option>
        <option value="Interface">Interface</option>
      </select>
      <select class="complexity-select">
        <option value="">${i18next.t('select_complexity')}</option>
        <option value="Simple">Simple</option>
        <option value="Average">Average</option>
        <option value="Complex">Complex</option>
      </select>
    `;
    elementsGrid.appendChild(card);
  });
}

// // 🧩 Populate Adjustment Questions with Sliders
// function populateAdjustmentQuestions() {
//   adjustmentQuestionsList.innerHTML = '';
//   gscQuestions.forEach((q, index) => {
//     const li = document.createElement('li');
//     li.className = 'gsc-question-item';
//     li.innerHTML = `
//       <div class="question-text">${index + 1}. ${q}</div>
//       <div class="slider-container">
//         <input type="range" class="gsc-slider" min="0" max="5" value="0" step="1">
//         <div class="slider-labels">
//           <span>0</span>
//           <span>1</span>
//           <span>2</span>
//           <span>3</span>
//           <span>4</span>
//           <span>5</span>
//         </div>
//       </div>
//       <div class="slider-value-display">0</div>
//     `;
//     adjustmentQuestionsList.appendChild(li);
    
//     // Add event listener for slider changes
//     const slider = li.querySelector('.gsc-slider');
//     const valueDisplay = li.querySelector('.slider-value-display');
    
//     slider.addEventListener('input', function() {
//       valueDisplay.textContent = this.value;
//       valueDisplay.style.transform = 'scale(1.2)';
//       setTimeout(() => valueDisplay.style.transform = 'scale(1)', 200);
//     });
    
//     // Add click handlers for number labels
//     const labels = li.querySelectorAll('.slider-labels span');
//     labels.forEach((label, idx) => {
//       label.addEventListener('click', function() {
//         slider.value = idx;
//         slider.dispatchEvent(new Event('input'));
//       });
//     });
//   });
// }

function populateAdjustmentQuestions() {
  adjustmentQuestionsList.innerHTML = '';
  gscQuestions.forEach((q, index) => {
    const li = document.createElement('li');
    li.className = 'gsc-question-item';
    li.innerHTML = `
      <div class="question-text">${index + 1}. ${q}</div>
      <div class="slider-container">
        <input type="range" class="gsc-slider" min="0" max="5" value="0" step="1">
        <div class="slider-labels">
          <span>0</span>
          <span>1</span>
          <span>2</span>
          <span>3</span>
          <span>4</span>
          <span>5</span>
        </div>
      </div>
      <div class="slider-value-display">0</div>
    `;
    adjustmentQuestionsList.appendChild(li);
    
    // Add event listener for slider changes
    const slider = li.querySelector('.gsc-slider');
    const valueDisplay = li.querySelector('.slider-value-display');
    
    slider.addEventListener('input', function() {
      const value = this.value;
      const max = this.max || 5;
      const percentage = (value / max) * 100;

      // Set dynamic background gradient for the slider track
      this.style.background = `linear-gradient(to right, var(--primary-color) 0%, var(--primary-color) ${percentage}%, var(--slider-track-bg) ${percentage}%, var(--slider-track-bg) 100%)`;

      valueDisplay.textContent = value;
      valueDisplay.style.transform = 'scale(1.2)';
      setTimeout(() => valueDisplay.style.transform = 'scale(1)', 200);
    });
    
    // Add click handlers for number labels
    const labels = li.querySelectorAll('.slider-labels span');
    labels.forEach((label, idx) => {
      label.addEventListener('click', function() {
        slider.value = idx;
        slider.dispatchEvent(new Event('input'));
      });
    });

    // Initialize background on load for initial value (0)
    slider.dispatchEvent(new Event('input'));
  });
}

// 🧮 Calculate UFP
function calculateUFPHandler() {
  const typeSelects = document.querySelectorAll('.type-select');
  const complexitySelects = document.querySelectorAll('.complexity-select');
  let ufp = 0;
  for (let i = 0; i < typeSelects.length; i++) {
    const type = typeSelects[i].value;
    const complexity = complexitySelects[i].value;
    if (type && complexity) ufp += weights[type][complexity];
  }
  document.getElementById('ufpValue').textContent = ufp;
  showToast('Success', `UFP calculated: ${ufp}`, 'success');
}

// 🔄 Reset
function resetFormHandler() {
  document.querySelectorAll('.type-select, .complexity-select').forEach(select => select.value = '');
  document.querySelectorAll('.gsc-slider').forEach(slider => {
    slider.value = 0;
    slider.dispatchEvent(new Event('input'));
  });
}

// 📈 Calculate Final Estimation
function calculateFinalEstimationHandler() {
  const adjustmentSliders = document.querySelectorAll('.gsc-slider');
  let totalGSC = 0;
  adjustmentSliders.forEach(slider => totalGSC += parseInt(slider.value, 10));

  const af = 0.65 + (totalGSC * 0.01);
  const ufp = parseInt(document.getElementById('ufpValue').textContent, 10) || 0;
  const afp = ufp * af;

  const productivityInput = document.getElementById('productivityInput');
  const salaryInput = document.getElementById('salaryInput');
  const productivity = parseFloat(productivityInput.value) || 18;
  const salary = parseFloat(salaryInput.value) || 5200;

  // Effort Calculation
  const effortManMonths = afp / productivity;
  const estimatedHours = effortManMonths * 160;
  const teamSize = Math.ceil(estimatedHours / 160);

  // Cost Estimation
  const minBudget = effortManMonths * salary;
  const maxBudget = effortManMonths * salary * 1.1;

  // Timeline
  const durationWeeks = Math.ceil(effortManMonths * 4.345);

  // Agile Breakdown
  const scrumSprintWeeks = 4;
  const xpIterationWeeks = 2;
  const scrumSprints = Math.ceil(durationWeeks / scrumSprintWeeks);
  const xpIterations = Math.ceil(durationWeeks / xpIterationWeeks);

  // Update Effort Estimation Tab
  document.getElementById('afpValue').textContent = afp.toFixed(2);
  document.getElementById('effortHours').textContent = Math.round(estimatedHours);
  document.getElementById('teamSize').textContent = teamSize;
  document.getElementById('budgetMin').textContent = `$${Math.round(minBudget).toLocaleString()}`;
  document.getElementById('budgetMax').textContent = `$${Math.round(maxBudget).toLocaleString()}`;
  document.getElementById('timeline').textContent = `${durationWeeks} weeks`;

  // Update Timeline Agile Details
  const timelineContainer = document.querySelector('.timeline-container');
  timelineContainer.innerHTML = `
    <div class="timeline-header">
      <div class="timeline-duration">
        <h3>${i18next.t('estimated_duration')}</h3>
        <div class="duration-value">${durationWeeks} weeks</div>
      </div>
      <div class="timeline-agile" style="margin-top:1rem;">
        <h4>${i18next.t('agile_breakdown')}</h4>
        <p><strong>${i18next.t('scrum_sprints')}:</strong> ${scrumSprints} Sprints (4 weeks each)</p>
        <p><strong>${i18next.t('xp_iterations')}:</strong> ${xpIterations} Iterations (2 weeks each)</p>
      </div>
    </div>
    <div class="timeline-chart">
      <canvas id="timelineChart"></canvas>
    </div>
  `;

  setupCharts();
  showToast('Success', 'Final estimation calculated.', 'success');
}

// 🔄 Tab Switching
function switchTab(tabId) {
  tabButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.tab === tabId));
  tabPanes.forEach(pane => pane.classList.toggle('active', pane.id.startsWith(tabId)));
}

// 🔔 Toasts
function showToast(title, message, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close">&times;</button>
  `;
  toastContainer.appendChild(toast);
  toast.querySelector('.toast-close').addEventListener('click', () => toast.remove());
  setTimeout(() => toast.remove(), 4000);
}

// 📈 Setup Charts
function setupCharts() {
  // تدمير الرسوم البيانية القديمة إذا كانت موجودة
  if (window.effortChart) window.effortChart.destroy();
  if (window.budgetChart) window.budgetChart.destroy();
  if (window.timelineChart) window.timelineChart.destroy();

  // الحصول على القيم الحالية
  const ufp = parseInt(document.getElementById('ufpValue').textContent) || 0;
  const afp = parseFloat(document.getElementById('afpValue').textContent) || 0;
  const minBudget = parseInt(document.getElementById('budgetMin').textContent.replace(/[^0-9]/g, '')) || 0;
  const maxBudget = parseInt(document.getElementById('budgetMax').textContent.replace(/[^0-9]/g, '')) || 0;
  const timelineWeeks = parseInt(document.getElementById('timeline').textContent) || 8;

  // إنشاء بيانات ديناميكية للجدول الزمني
  const timelineLabels = [];
  const timelineData = [];
  for (let i = 1; i <= timelineWeeks; i++) {
    timelineLabels.push(`${i18next.t('week')} ${i}`);
    timelineData.push(Math.min(100, Math.round((i / timelineWeeks) * 100)));
  }

  // Effort Chart
  window.effortChart = new Chart(document.getElementById('effortChart'), {
    type: 'bar',
    data: {
      labels: [i18next.t('function_points'), i18next.t('adjusted_fp')],
      datasets: [{
        label: i18next.t('effort'),
        data: [ufp, afp],
        backgroundColor: ['#4f46e5', '#38bdf8']
      }]
    },
    options: getChartOptions(i18next.t('function_points_comparison'))
  });

  // Budget Chart
  window.budgetChart = new Chart(document.getElementById('budgetChart'), {
    type: 'doughnut',
    data: {
      labels: [i18next.t('minimum_budget'), i18next.t('maximum_budget')],
      datasets: [{
        data: [minBudget, maxBudget],
        backgroundColor: ['#38bdf8', '#4f46e5']
      }]
    },
    options: getChartOptions(i18next.t('budget_distribution'), 'bottom')
  });

  // Timeline Chart
  window.timelineChart = new Chart(document.getElementById('timelineChart'), {
    type: 'line',
    data: {
      labels: timelineLabels,
      datasets: [{
        label: i18next.t('progress'),
        data: timelineData,
        backgroundColor: 'rgba(79,70,229,0.2)',
        borderColor: '#4f46e5',
        fill: true,
        tension: 0.4
      }]
    },
    options: getChartOptions(i18next.t('project_timeline'), 'top', {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: i18next.t('completion_percentage')
        }
      }
    })
  });
}

// دالة مساعدة لإنشاء خيارات الرسم البياني
function getChartOptions(title, legendPosition = 'top', scales = {}) {
  return {
    responsive: true,
    plugins: {
      legend: {
        position: legendPosition,
      },
      title: {
        display: true,
        text: title
      }
    },
    scales: scales
  };
}

// Setup Sidebar Navigation
function setupSidebarNavigation() {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      const tabId = link.getAttribute('data-tab');
      if (tabId) {
        switchTab(tabId);
      } else if (link.getAttribute('href') === '#uploadSection') {
        uploadSection.style.display = 'block';
        processingSection.style.display = 'none';
        resultsSection.style.display = 'none';
      }
    });
  });
}

// 🔥 Init
function init() {
  // Initialize i18n
  initI18n();
  
  // Initialize theme
  initTheme();
  
  // Initialize language
  initLanguage();
  
  // Initialize user profile
  updateUserProfile();
  
  // Apply role-based UI if logged in
  const role = localStorage.getItem('userRole');
  if (role) {
    applyRoleBasedUI(role);
  }

  // Setup sidebar navigation
  setupSidebarNavigation();

  // File upload handlers
  dropzone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', handleFileSelection);
  removeFileBtn.addEventListener('click', handleRemoveFile);
  startAnalysisBtn.addEventListener('click', handleStartAnalysis);

  // Tab switching
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabId = button.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Calculation handlers
  if (calculateUFPBtn) calculateUFPBtn.addEventListener('click', calculateUFPHandler);
  if (resetFormBtn) resetFormBtn.addEventListener('click', resetFormHandler);
  if (calculateFinalEstimationBtn) calculateFinalEstimationBtn.addEventListener('click', calculateFinalEstimationHandler);

  // New feature handlers
  themeToggle.addEventListener('click', toggleTheme);
  languageToggle.addEventListener('click', toggleLanguage);
  loginBtn.addEventListener('click', () => loginModal.style.display = 'flex');
  closeModalBtn.addEventListener('click', () => loginModal.style.display = 'none');
  logoutBtn.addEventListener('click', handleLogout);
  loginForm.addEventListener('submit', handleLogin);
  
  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
      loginModal.style.display = 'none';
    }
  });
}
