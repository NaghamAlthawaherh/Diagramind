/**
 * 📁 Esti-Use Signup Script (Final Version)
 * Description: Secure signup with validation and email verification
 */

// 🚀 Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", initSignupPage);

function initSignupPage() {
  initDarkMode();           // Setup dark mode toggle
  initLanguageSwitcher();   // Setup language switching
  initFormValidation();     // Setup form validation on submit
  initPasswordToggle();     // Setup password show/hide toggles and strength meter
  initSocialLogin();        // Setup social signup buttons
  trackPageView();          // Track page view event for analytics
}

// 🌙 Dark Mode Handler (Same as login.js)
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

// 🌐 Translation System
const translations = {
  en: {
    createAccount: "Create your account",
    firstName: "First Name",
    lastName: "Last Name",
    email: "Email",
    password: "Password",
    confirmPassword: "Confirm Password",
    company: "Company (Optional)",
    typeLabel: "User Type",
    acceptTerms: "I agree to the",
    terms: "Terms of Service",
    and: "and",
    privacy: "Privacy Policy",
    subscribeNewsletter: "Subscribe to our newsletter",
    haveAccount: "Already have an account?",
    login: "Log In",
    toggleDark: "Dark Mode",
    backHome: "Back to Home",
    verifyEmail: "Verify Your Email",
    verificationMessage: "We've sent a verification link to your email address. Please click the link to verify your account.",
    checkSpam: "Didn't receive the email? Check your spam folder.",
    close: "Close",
    resend: "Resend Email",
    passwordRequirements: "Use 8+ characters with a mix of letters, numbers & symbols",
    invalidEmail: "Please enter a valid email address.",
    emptyPassword: "Password is required.",
    shortPassword: "Password must be at least 8 characters.",
    weakPassword: "Password is too weak. Include numbers and special characters.",
    passwordMismatch: "Passwords do not match.",
    termsRequired: "You must agree to the terms and conditions.",
    signupSuccess: "Account created successfully! Please verify your email.",
    userTypeRequired: "Please select a user type."
  },
  ar: {
    createAccount: "إنشاء حساب جديد",
    firstName: "الاسم الأول",
    lastName: "الاسم الأخير",
    email: "البريد الإلكتروني",
    password: "كلمة المرور",
    confirmPassword: "تأكيد كلمة المرور",
    company: "الشركة (اختياري)",
    typeLabel: "نوع المستخدم",
    acceptTerms: "أوافق على",
    terms: "شروط الخدمة",
    and: "و",
    privacy: "سياسة الخصوصية",
    subscribeNewsletter: "الاشتراك في النشرة الإخبارية",
    haveAccount: "لديك حساب بالفعل؟",
    login: "تسجيل الدخول",
    toggleDark: "الوضع المظلم",
    backHome: "العودة للرئيسية",
    verifyEmail: "تحقق من بريدك الإلكتروني",
    verificationMessage: "لقد أرسلنا رابط تحقق إلى عنوان بريدك الإلكتروني. يرجى النقر على الرابط للتحقق من حسابك.",
    checkSpam: "لم تستلم البريد؟ تحقق من مجلد البريد العشوائي.",
    close: "إغلاق",
    resend: "إعادة إرسال البريد",
    passwordRequirements: "استخدم 8 أحرف على الأقل مع مزيج من الحروف والأرقام والرموز",
    invalidEmail: "الرجاء إدخال بريد إلكتروني صحيح.",
    emptyPassword: "كلمة المرور مطلوبة.",
    shortPassword: "يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل.",
    weakPassword: "كلمة المرور ضعيفة. أضف أرقامًا ورموزًا خاصة.",
    passwordMismatch: "كلمات المرور غير متطابقة.",
    termsRequired: "يجب الموافقة على الشروط والأحكام.",
    signupSuccess: "تم إنشاء الحساب بنجاح! يرجى التحقق من بريدك الإلكتروني.",
    userTypeRequired: "يرجى اختيار نوع المستخدم."
  }
};

// Initialize language switcher UI and behavior
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

// Setup form validation on submit
function initFormValidation() {
  const signupForm = document.getElementById("signupForm");
  if (!signupForm) return;

  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const firstName = document.getElementById("firstName");
    const lastName = document.getElementById("lastName");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const termsCheck = document.getElementById("termsCheck");
    const userType = document.getElementById("userType");
    const lang = localStorage.getItem("estiuse-login-lang") || "en";
    const t = translations[lang];

    // Reset previous validation states
    firstName.classList.remove("is-invalid");
    lastName.classList.remove("is-invalid");
    email.classList.remove("is-invalid");
    password.classList.remove("is-invalid");
    confirmPassword.classList.remove("is-invalid");
    termsCheck.classList.remove("is-invalid");
    userType.classList.remove("is-invalid");

    // Validate form inputs
    const errors = validateInputs(
      firstName.value,
      lastName.value,
      email.value,
      password.value,
      confirmPassword.value,
      termsCheck.checked,
      userType.value,
      t
    );

    if (errors.length > 0) {
      showFirstError(errors);
      return;
    }

    if (checkRateLimit()) return;

    await processSignup();

    trackEvent('signup_attempt');
  });
}

function validateInputs(firstName, lastName, email, password, confirmPassword, termsAccepted, userType, t) {
  const errors = [];
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

  if (!firstName.trim()) {
    errors.push({ element: "firstName", message: "Please enter your first name." });
  }

  if (!lastName.trim()) {
    errors.push({ element: "lastName", message: "Please enter your last name." });
  }

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

  if (password !== confirmPassword) {
    errors.push({ element: "confirmPassword", message: t.passwordMismatch });
  }

  if (!termsAccepted) {
    errors.push({ element: "termsCheck", message: t.termsRequired });
  }

  if (!userType) {
    errors.push({ element: "userType", message: t.userTypeRequired });
  }

  return errors;
}

function showFirstError(errors) {
  const firstError = errors[0];
  const element = document.getElementById(firstError.element);
  element.classList.add("is-invalid");
  element.focus();
  showToast(firstError.message, "danger");
}

// Password show/hide toggles and strength meter
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

  const confirmPasswordInput = document.getElementById("confirmPassword");
  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener("input", checkPasswordMatch);
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

function checkPasswordMatch() {
  const password = document.getElementById("password").value;
  const confirmPassword = this.value;
  const confirmPasswordError = document.getElementById("confirmPasswordError");

  if (confirmPassword && password !== confirmPassword) {
    this.classList.add("is-invalid");
    confirmPasswordError.textContent = translations[localStorage.getItem("estiuse-login-lang") || "en"].passwordMismatch;
  } else {
    this.classList.remove("is-invalid");
  }
}

// Toast notification
function showToast(message, type = "info", duration = 5000) {
  const toastEl = document.getElementById("signupToast");
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


async function processSignup() {
  const signupBtn = document.getElementById("signupBtn");
  const signupText = document.getElementById("signupText");
  const spinner = document.getElementById("signupSpinner");

  try {
    signupBtn.disabled = true;
    spinner.classList.remove("d-none");
    signupText.textContent = "Creating account...";

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const company = document.getElementById("company").value;
    const userType = document.getElementById("userType").value;
    const termsCheck = document.getElementById("termsCheck").checked;

    const payload = {
      firstName,
      lastName,
      email,
      password,
      confirmPassword,
      company,
      userType,
      termsCheck
    };

    const response = await axios.post("/signup", payload);

    // افترض أن السيرفر يرجع JSON مع status
    if (response.status === 200) {
      // نجاح التسجيل - عرض رسالة النجاح كما في الكود الحالي
      // أو يمكنك إعادة توجيه المستخدم إلى صفحة أخرى
      location.href = "/login"; // مثلاً
    } else {
      // خطأ ما في التسجيل - عرض رسالة خطأ
      showToast("Signup failed: " + response.data.message, "danger");
    }
  } catch (error) {
    showToast("Signup failed: " + (error.response?.data?.message || error.message), "danger");
  } finally {
    signupBtn.disabled = false;
    spinner.classList.add("d-none");
    signupText.textContent = "Sign Up";
  }
}




// Signup process (simulate with delay)
// async function processSignup() {
//   const signupBtn = document.getElementById("signupBtn");
//   const signupText = document.getElementById("signupText");
//   const spinner = document.getElementById("signupSpinner");

//   try {
//     signupBtn.disabled = true;
//     spinner.classList.remove("d-none");
//     signupText.textContent = "Creating account...";

//     // TODO: Replace with actual API call
//     await new Promise(resolve => setTimeout(resolve, 2000));

//     const lang = localStorage.getItem("estiuse-login-lang") || "en";
//     const t = translations[lang];

//     document.getElementById("signupForm").innerHTML = `
//       <div class="success-message animate__animated animate__fadeIn">
//         <div class="success-icon mb-3">
//           <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
//             <circle cx="12" cy="12" r="10" stroke="#28a745" stroke-width="2"/>
//             <path d="M8 12L11 15L16 9" stroke="#28a745" stroke-width="2" stroke-linecap="round"/>
//           </svg>
//         </div>
//         <h3 class="mb-3 fw-bold">${t.signupSuccess}</h3>
//         <p class="mb-4">${t.verificationMessage}</p>
//         <div class="d-flex gap-2 justify-content-center">
//           <a href="{{ url_for('main.login') }}"class="btn btn-primary px-4">
//             <i class="fas fa-sign-in-alt me-2"></i> ${t.login}
//           </a>
//           <a href="{{ url_for('main.index1') }}"class="btn btn-outline-secondary px-4">
//             <i class="fas fa-home me-2"></i> ${t.backHome}
//           </a>
//         </div>
//         <p class="text-muted mt-3 small">
//           <i class="fas fa-info-circle me-1"></i> ${t.checkSpam}
//         </p>
//       </div>
//     `;

//     trackEvent('signup_success');
//   } catch (error) {
//     showToast("⚠️ Signup failed. Please try again.", "danger");
//   } finally {
//     signupBtn.disabled = false;
//     spinner.classList.add("d-none");
//     signupText.textContent = "Sign Up";
//   }
// }

// Social login/signup buttons initialization
function initSocialLogin() {
  document.querySelectorAll('.social-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const provider = btn.getAttribute('data-provider');
      trackEvent('social_signup_attempt', { provider });
      showToast(`Redirecting to ${provider}...`, "info");
      window.open(`/auth/${provider}`, '_blank', 'width=500,height=600');
    });
  });
}

// Analytics tracking helpers
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

// Rate limiting (temporarily disabled)
function checkRateLimit() {
  return false;
}
