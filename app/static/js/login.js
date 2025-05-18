document.addEventListener("DOMContentLoaded", initLoginPage);

function initLoginPage() {
  initDarkMode();
  initLanguageSwitcher();
  initFormValidation();
  initPasswordToggle();
  initSocialLogin();
  initWebAuthn();
  loadSavedCredentials();
  requestNotificationPermission();
  trackPageView();
  init2FAResendTimer();
}

// Dark Mode
function initDarkMode() {
  const toggleDarkBtn = document.getElementById("toggleDark");
  if (!toggleDarkBtn) return;

  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedMode = localStorage.getItem("estiuse-login-dark");

  if (savedMode === "on" || (savedMode === null && systemPrefersDark)) {
    document.body.classList.add("dark-mode");
    toggleDarkBtn.setAttribute("aria-pressed", "true");
    toggleDarkBtn.innerHTML = '<i class="fas fa-sun me-1"></i> Light Mode';
  }

  toggleDarkBtn.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-mode");
    localStorage.setItem("estiuse-login-dark", isDark ? "on" : "off");
    toggleDarkBtn.setAttribute("aria-pressed", isDark);
    toggleDarkBtn.innerHTML = isDark
      ? '<i class="fas fa-sun me-1"></i> Light Mode'
      : '<i class="fas fa-moon me-1"></i> Dark Mode';
    trackEvent('dark_mode_toggle', { mode: isDark ? 'dark' : 'light' });
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener("change", e => {
    if (localStorage.getItem("estiuse-login-dark") === null) {
      document.body.classList.toggle("dark-mode", e.matches);
    }
  });
}

// Translations
const translations = {
  en: {
    email: "Email",
    password: "Password",
    remember: "Remember me",
    forgot: "Forgot Password?",
    login: "Log In",
    signup: "Sign Up",
    noaccount: "Don't have an account?",
    toggleDark: "Dark Mode",
    backHome: "Back to Home",
    or: "or",
    useBiometric: "Use Biometric Login",
    twoFATitle: "Two-Factor Authentication",
    twoFAMessage: "Please enter the 6-digit code sent to your email",
    cancel: "Cancel",
    verify: "Verify",
    invalidEmail: "Please enter a valid email address.",
    emptyPassword: "Password is required.",
    shortPassword: "Password must be at least 8 characters.",
    weakPassword: "Password is too weak. Include numbers and special characters.",
    biometricSuccess: "Biometric authentication successful!",
    biometricError: "Biometric authentication failed",
    invalid2FACode: "Please enter a valid 6-digit code."
  },
  ar: {
    email: "البريد الإلكتروني",
    password: "كلمة المرور",
    remember: "تذكرني",
    forgot: "نسيت كلمة المرور؟",
    login: "تسجيل الدخول",
    signup: "إنشاء حساب",
    noaccount: "ليس لديك حساب؟",
    toggleDark: "الوضع المظلم",
    backHome: "العودة للرئيسية",
    or: "أو",
    useBiometric: "استخدام البصمة أو التعرف على الوجه",
    twoFATitle: "المصادقة الثنائية",
    twoFAMessage: "الرجاء إدخال الرمز المكون من 6 أرقام المرسل إلى بريدك",
    cancel: "إلغاء",
    verify: "تحقق",
    invalidEmail: "الرجاء إدخال بريد إلكتروني صحيح.",
    emptyPassword: "كلمة المرور مطلوبة.",
    shortPassword: "يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل.",
    weakPassword: "كلمة المرور ضعيفة. أضف أرقامًا ورموزًا خاصة.",
    biometricSuccess: "تم التسجيل بنجاح باستخدام البصمة!",
    biometricError: "فشلت المصادقة البيومترية",
    invalid2FACode: "الرجاء إدخال رمز صحيح مكون من 6 أرقام."
  }
};

function initLanguageSwitcher() {
  const langSwitcher = document.getElementById("langSwitcher");
  if (!langSwitcher) return;

  const savedLang = localStorage.getItem("estiuse-login-lang") || "en";
  applyTranslations(savedLang);
  langSwitcher.value = savedLang;

  langSwitcher.addEventListener("change", (e) => {
    const newLang = e.target.value;
    localStorage.setItem("estiuse-login-lang", newLang);
    applyTranslations(newLang);
    document.documentElement.lang = newLang;
    document.documentElement.dir = newLang === "ar" ? "rtl" : "ltr";
    trackEvent('language_change', { language: newLang });
  });
}

function applyTranslations(lang) {
  const t = translations[lang];
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (t[key]) {
      if (el.tagName === "INPUT") {
        el.placeholder = t[key];
      } else {
        el.textContent = t[key];
      }
    }
  });
}

// Form Validation
function initFormValidation() {
  const loginForm = document.getElementById("loginForm");
  if (!loginForm) return;

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const remember = document.getElementById("rememberMe").checked;
    const lang = localStorage.getItem("estiuse-login-lang") || "en";
    const t = translations[lang];

    email.classList.remove("is-invalid");
    email.setAttribute("aria-invalid", "false");
    password.classList.remove("is-invalid");
    password.setAttribute("aria-invalid", "false");

    const errors = validateInputs(email.value, password.value, t);
    if (errors.length > 0) {
      showFirstError(errors);
      return;
    }

    // Rate limiting check (adjust maxAttempts as needed)
    if (checkRateLimit()) return;

    handleRememberMe(email.value, remember);

    const is2FARequired = await initiate2FA(email.value);
    if (is2FARequired) {
      show2FAModal();
      startResendTimer();
    } else {
      await processLogin();
    }

    trackEvent('login_attempt', { method: 'email' });
  });
}

function validateInputs(email, password, t) {
  const errors = [];
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

  if (!emailRegex.test(email.trim())) {
    errors.push({ element: "email", message: t.invalidEmail });
  }

  if (!password.trim()) {
    errors.push({ element: "password", message: t.emptyPassword });
  } else if (password.length < 8) {
    errors.push({ element: "password", message: t.shortPassword });
  } else if (!passwordRegex.test(password)) {
    errors.push({ element: "password", message: t.weakPassword });
  }

  return errors;
}

function showFirstError(errors) {
  const firstError = errors[0];
  const element = document.getElementById(firstError.element);
  element.classList.add("is-invalid");
  element.setAttribute("aria-invalid", "true");
  element.focus();
  showToast(firstError.message, "danger");
}

// Password toggle & strength
function initPasswordToggle() {
  document.querySelectorAll(".toggle-password").forEach(icon => {
    icon.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = icon.getAttribute("data-target");
      const input = document.getElementById(targetId);
      if (!input) return;

      const isPassword = input.type === "password";
      input.type = isPassword ? "text" : "password";

      const iconElement = icon.querySelector("i");
      iconElement.classList.toggle("fa-eye", !isPassword);
      iconElement.classList.toggle("fa-eye-slash", isPassword);
      icon.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
      input.focus();
    });
  });

  const passwordInput = document.getElementById("password");
  if (passwordInput) {
    passwordInput.addEventListener("input", updatePasswordStrength);
  }
}

function updatePasswordStrength() {
  const password = this.value;
  const strengthMeter = document.querySelector(".password-strength progress");
  if (!strengthMeter) return;

  let strength = 0;
  if (password.length > 0) strength += 25;
  if (password.length >= 8) strength += 25;
  if (/[A-Z]/.test(password)) strength += 20;
  if (/\d/.test(password)) strength += 15;
  if (/[^A-Za-z0-9]/.test(password)) strength += 15;

  strengthMeter.value = Math.min(strength, 100);
}

// Toast Notifications
function showToast(message, type = "info", duration = 5000) {
  const toastEl = document.getElementById("loginToast");
  const toastMessage = document.getElementById("toastMessage");
  if (!toastEl || !toastMessage) return;

  toastMessage.textContent = message;
  toastEl.className = `toast align-items-center text-bg-${type} border-0`;

  const isRTL = /[\u0591-\u07FF]/.test(message);
  toastEl.setAttribute("dir", isRTL ? "rtl" : "ltr");

  const toast = new bootstrap.Toast(toastEl, {
    animation: true,
    autohide: true,
    delay: duration
  });
  toast.show();

  return toast;
}

// Credentials Management
function loadSavedCredentials() {
  const emailInput = document.getElementById("email");
  const rememberCheckbox = document.getElementById("rememberMe");
  if (!emailInput || !rememberCheckbox) return;

  const savedEmail = localStorage.getItem("estiuse-saved-email");
  if (savedEmail) {
    emailInput.value = savedEmail;
    rememberCheckbox.checked = true;
  }
}

function handleRememberMe(email, shouldRemember) {
  if (shouldRemember) {
    localStorage.setItem("estiuse-saved-email", email.trim());
  } else {
    localStorage.removeItem("estiuse-saved-email");
  }
}

// Login Process with skeleton loading
async function processLogin() {
  const loginBtn = document.getElementById("loginBtn");
  const loginText = document.getElementById("loginText");
  const spinner = document.getElementById("loginSpinner");

  try {
    loginBtn.disabled = true;
    loginBtn.setAttribute("aria-busy", "true");
    loginBtn.setAttribute("aria-disabled", "true");
    spinner.classList.remove("d-none");
    loginText.textContent = "Logging in...";

    showToast("جاري التحميل...", "info");
    document.body.innerHTML = `
      <div class="skeleton-loading">
        <div class="skeleton-header"></div>
        <div class="skeleton-content"></div>
      </div>
    `;

    await new Promise(resolve => setTimeout(resolve, 1500));

    window.location.href = "index1.html";
  } catch (error) {
    showToast("⚠️ Login failed. Please try again.", "danger");
    loginBtn.disabled = false;
    loginBtn.setAttribute("aria-busy", "false");
    loginBtn.setAttribute("aria-disabled", "false");
    spinner.classList.add("d-none");
    loginText.textContent = "Log In";
  }
}

// 2FA System
async function initiate2FA(email) {
  const requires2FA = Math.random() > 0.5;
  if (requires2FA) {
    console.log(`2FA code sent to ${email}`);
    return true;
  }
  return false;
}

function show2FAModal() {
  const modalEl = document.getElementById('twoFAModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();

  const inputs = modalEl.querySelectorAll('.verification-input');
  const verifyBtn = document.getElementById('verify2FABtn');
  const errorMsg = document.getElementById('twoFAError');

  function updateVerifyButtonState() {
    const code = Array.from(inputs).map(input => input.value.trim()).join('');
    if (code.length === 6 && /^[0-9]{6}$/.test(code)) {
      verifyBtn.disabled = false;
      errorMsg.classList.add('visually-hidden');
      clearInvalidInputs();
    } else {
      verifyBtn.disabled = true;
      if (code.length > 0) {
        errorMsg.classList.remove('visually-hidden');
        markInvalidInputs();
      } else {
        errorMsg.classList.add('visually-hidden');
        clearInvalidInputs();
      }
    }
  }

  function markInvalidInputs() {
    inputs.forEach(input => {
      if (!/^[0-9]$/.test(input.value)) {
        input.classList.add('is-invalid');
      } else {
        input.classList.remove('is-invalid');
      }
    });
  }

  function clearInvalidInputs() {
    inputs.forEach(input => input.classList.remove('is-invalid'));
  }

  // Clear inputs on modal show
  inputs.forEach((input, index) => {
    input.value = '';
    input.classList.remove('is-invalid');

    input.addEventListener('input', (e) => {
      // Allow only digits
      input.value = input.value.replace(/[^0-9]/g, '');
      if (input.value.length === 1 && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
      updateVerifyButtonState();
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && input.value.length === 0 && index > 0) {
        inputs[index - 1].focus();
      }
    });

    // Support paste event for full 6-digit code
    input.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasteData = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '');
      if (pasteData.length === 6) {
        inputs.forEach((inputEl, i) => {
          inputEl.value = pasteData.charAt(i);
        });
        inputs[inputs.length - 1].focus();
        updateVerifyButtonState();
      }
    });
  });

  verifyBtn.disabled = true;
  errorMsg.classList.add('visually-hidden');

  verifyBtn.onclick = async () => {
    const code = Array.from(inputs).map(input => input.value).join('');
    const lang = localStorage.getItem("estiuse-login-lang") || "en";
    const t = translations[lang];
    if (code.length === 6 && /^[0-9]{6}$/.test(code)) {
      await processLogin();
      modal.hide();
    } else {
      showToast(t.invalid2FACode, "warning");
      errorMsg.classList.remove('visually-hidden');
      markInvalidInputs();
    }
  };
}

// 2FA resend timer
let resendTimerInterval;
function startResendTimer(seconds = 30) {
  const resendBtn = document.getElementById('resend2FABtn');
  const timerEl = document.getElementById('resendTimer');
  if (!resendBtn || !timerEl) return;

  let remaining = seconds;
  resendBtn.disabled = true;
  timerEl.textContent = `إعادة إرسال الرمز (${remaining})`;

  clearInterval(resendTimerInterval);
  resendTimerInterval = setInterval(() => {
    remaining--;
    timerEl.textContent = `إعادة إرسال الرمز (${remaining})`;
    if (remaining <= 0) {
      clearInterval(resendTimerInterval);
      resendBtn.disabled = false;
      timerEl.textContent = "إعادة إرسال الرمز";
    }
  }, 1000);

  resendBtn.onclick = () => {
    // هنا تضيف منطق إعادة إرسال الرمز (مثلاً طلب API)
    showToast("تم إعادة إرسال الرمز.", "success");
    startResendTimer(seconds);
  };
}

function init2FAResendTimer() {
  const resendBtn = document.getElementById('resend2FABtn');
  if (resendBtn) {
    resendBtn.disabled = true;
  }
}

// Social Login
function initSocialLogin() {
  document.querySelectorAll('.social-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const provider = btn.getAttribute('data-provider');
      trackEvent('social_login_attempt', { provider });
      showToast(`جاري التحويل إلى ${provider}...`, "info");
      window.open(`/auth/${provider}`, '_blank', 'width=500,height=600');
    });
  });
}

// Analytics
function trackPageView() {
  if (typeof analytics !== 'undefined') {
    analytics.track('page_view', {
      page: window.location.pathname,
      referrer: document.referrer,
      userAgent: navigator.userAgent
    });
  }
}

function trackEvent(eventName, metadata = {}) {
  if (typeof analytics !== 'undefined') {
    analytics.track(eventName, {
      ...metadata,
      timestamp: new Date().toISOString()
    });
  }
  console.log(`Event: ${eventName}`, metadata);
}

// Notification Permission
function requestNotificationPermission() {
  if ('Notification' in window && Notification.permission !== 'denied') {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        trackEvent('notification_permission_granted');
      }
    });
  }
}

// Rate Limiting
const loginAttemptsKey = 'loginAttempts';

function getLoginAttempts() {
  const data = localStorage.getItem(loginAttemptsKey);
  return data ? JSON.parse(data) : { count: 0, lastAttempt: 0 };
}

function setLoginAttempts(attempts) {
  localStorage.setItem(loginAttemptsKey, JSON.stringify(attempts));
}

function checkRateLimit() {
  const now = Date.now();
  const oneHour = 3600000;
  let loginAttempts = getLoginAttempts();

  if (now - loginAttempts.lastAttempt > oneHour) {
    loginAttempts = { count: 0, lastAttempt: 0 };
  }

  const maxAttempts = 100;

  if (loginAttempts.count >= maxAttempts && (now - loginAttempts.lastAttempt) < oneHour) {
    showToast("⏳ Too many attempts. Please try again later.", "warning");
    return true;
  }

  loginAttempts.count++;
  loginAttempts.lastAttempt = now;
  setLoginAttempts(loginAttempts);
  return false;
}
