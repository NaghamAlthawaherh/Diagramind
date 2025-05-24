
// -------------------------------------------------
// 📁 Esti-Use - Enhanced Homepage Script
// Features: Dark mode, i18n translations, toast, RTL support
// Optimized for performance and maintainability
// -------------------------------------------------

// 🚀 Initialize on DOM Ready (with error handling)
document.addEventListener('DOMContentLoaded', () => {
    try {
      initDarkMode();
      initTranslations();
      showWelcomeToast();
    } catch (error) {
      console.error('Esti-Use initialization error:', error);
    }
  });
  
  // 🌙 Dark Mode Handler (Optimized)
  function initDarkMode() {
    const toggleDarkBtn = document.getElementById('toggleDark');
    if (!toggleDarkBtn) return;
  
    // Check saved preference or system preference
    const savedMode = localStorage.getItem('estiuse-dark');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'on' || (!savedMode && systemPrefersDark)) {
      document.body.classList.add('dark-mode');
      toggleDarkBtn.innerHTML = `<i class="fas fa-sun"></i> <span data-i18n="toggleLight">Light Mode</span>`;
    }
  
    // Toggle handler
    toggleDarkBtn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-mode');
      localStorage.setItem('estiuse-dark', isDark ? 'on' : 'off');
      
      // Update button icon/text
      toggleDarkBtn.innerHTML = isDark 
        ? `<i class="fas fa-sun"></i> <span data-i18n="toggleLight">Light Mode</span>`
        : `<i class="fas fa-moon"></i> <span data-i18n="toggleDark">Dark Mode</span>`;
      
      // Re-apply translations for the updated text
      const currentLang = document.documentElement.lang || 'en';
      applyTranslations(currentLang);
    });
  }
  
  // 🌐 Translation System (Modular Approach)
  const translations = {
    en: {
      subtitle: "Smart Estimation. Powered by AI & Use Case Diagrams.",
      lead: "Upload your UML diagram and get instant project estimates with 90%+ accuracy",
      step1text: "Upload Use Case Diagram",
      step2text: "Extract Requirements",
      step3text: "Estimate Effort & Cost",
      step4text: "Export Report",
      feature1: "Extract Actors and Use Cases automatically",
      feature2: "Generate functional requirements in seconds",
      feature3: "AI-powered effort & cost estimations",
      feature4: "Export professional PDF/Excel reports",
      feature5: "Dark mode & multilingual support",
      welcome: "👋 Welcome to Esti-Use! Upload your first diagram and get instant estimates.",
      login: "Log In",
      signup: "Sign Up",
      getStarted: "Get Started - It's Free",
      toggleDark: "Dark Mode",
      toggleLight: "Light Mode",
      watchDemo: "Watch 2-Minute Demo",
      help: "Help Center",
      settings: "Settings",
      contact: "Contact Us",
      howItWorks: "How It Works"
    },
    ar: {
      subtitle: "تقدير ذكي مدعوم بالذكاء الاصطناعي ومخططات الحالات",
      lead: "قم برفع مخطط UML الخاص بك واحصل على تقديرات فورية بدقة تزيد عن 90٪",
      step1text: "رفع مخطط الحالات",
      step2text: "استخراج المتطلبات",
      step3text: "تقدير الجهد والتكلفة",
      step4text: "تصدير التقرير",
      feature1: "استخراج تلقائي للجهات الفاعلة وحالات الاستخدام",
      feature2: "إنشاء المتطلبات الوظيفية في ثوانٍ",
      feature3: "تقديرات الجهد والتكلفة بالذكاء الاصطناعي",
      feature4: "تصدير تقارير PDF/Excel احترافية",
      feature5: "الوضع المظلم ودعم متعدد اللغات",
      welcome: "👋 مرحبًا بكم في Esti-Use! ارفع مخططك الأول واحصل على تقديرات فورية.",
      login: "تسجيل الدخول",
      signup: "إنشاء حساب",
      getStarted: "ابدأ الآن - مجانًا",
      toggleDark: "الوضع المظلم",
      toggleLight: "الوضع الفاتح",
      watchDemo: "مشاهدة عرض دقيقتين",
      help: "مركز المساعدة",
      settings: "الإعدادات",
      contact: "اتصل بنا",
      howItWorks: "كيف يعمل"
    }
  };
  
  function initTranslations() {
    const languageSwitcher = document.getElementById('langSwitcher');
    if (!languageSwitcher) return;
  
    // Set initial language
    const savedLang = localStorage.getItem('estiuse-lang') || 'en';
    setLanguage(savedLang, false);
  
    // Handle language change
    languageSwitcher.addEventListener('change', (e) => {
      setLanguage(e.target.value, true);
    });
  }
  
  function setLanguage(lang, save = true) {
    if (!translations[lang]) return;
  
    // Update UI
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Apply RTL-specific styles
    if (lang === 'ar') {
      document.body.classList.add('rtl');
    } else {
      document.body.classList.remove('rtl');
    }
  
    // Save preference
    if (save) {
      localStorage.setItem('estiuse-lang', lang);
    }
  
    // Apply translations
    applyTranslations(lang);
  }
  
  function applyTranslations(lang) {
    const t = translations[lang];
    if (!t) return;
  
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) {
        // Handle different element types
        if (el.tagName === 'INPUT' && el.placeholder !== undefined) {
          el.placeholder = t[key];
        } else {
          el.textContent = t[key];
        }
  
        // Update accessibility attributes
        if (el.hasAttribute('aria-label')) {
          el.setAttribute('aria-label', t[key]);
        }
        if (el.hasAttribute('title')) {
          el.setAttribute('title', t[key]);
        }
      }
    });
  }
  
  // 🎉 Welcome Toast (Optimized)
  function showWelcomeToast() {
    if (sessionStorage.getItem('estiuse-visited')) return;
    
    const toastEl = document.getElementById('welcomeToast');
    if (!toastEl) return;
  
    // Show toast with delay
    setTimeout(() => {
      const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 5000
      });
      toast.show();
      sessionStorage.setItem('estiuse-visited', 'true');
    }, 1000);
  }
  
  // 🖥️ System Preference Listeners
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('estiuse-dark')) {
      document.body.classList.toggle('dark-mode', e.matches);
    }

// -------------------------------------------------
// 📁 Esti-Use - Enhanced Homepage Script
// Features: Dark mode, i18n translations, toast, RTL support
// Optimized for performance and maintainability
// -------------------------------------------------

// 🚀 Initialize on DOM Ready (with error handling)
document.addEventListener('DOMContentLoaded', () => {
    try {
      initDarkMode();
      initTranslations();
      showWelcomeToast();
    } catch (error) {
      console.error('Esti-Use initialization error:', error);
    }
  });
  
  // 🌙 Dark Mode Handler (Optimized)
  function initDarkMode() {
    const toggleDarkBtn = document.getElementById('toggleDark');
    if (!toggleDarkBtn) return;
  
    // Check saved preference or system preference
    const savedMode = localStorage.getItem('estiuse-dark');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'on' || (!savedMode && systemPrefersDark)) {
      document.body.classList.add('dark-mode');
      toggleDarkBtn.innerHTML = `<i class="fas fa-sun"></i> <span data-i18n="toggleLight">Light Mode</span>`;
    }
  
    // Toggle handler
    toggleDarkBtn.addEventListener('click', () => {
      const isDark = document.body.classList.toggle('dark-mode');
      localStorage.setItem('estiuse-dark', isDark ? 'on' : 'off');
      
      // Update button icon/text
      toggleDarkBtn.innerHTML = isDark 
        ? `<i class="fas fa-sun"></i> <span data-i18n="toggleLight">Light Mode</span>`
        : `<i class="fas fa-moon"></i> <span data-i18n="toggleDark">Dark Mode</span>`;
      
      // Re-apply translations for the updated text
      const currentLang = document.documentElement.lang || 'en';
      applyTranslations(currentLang);
    });
  }
  
  // 🌐 Translation System (Modular Approach)
  const translations = {
    en: {
      subtitle: "Smart Estimation. Powered by AI & Use Case Diagrams.",
      lead: "Upload your UML diagram and get instant project estimates with 90%+ accuracy",
      step1text: "Upload Use Case Diagram",
      step2text: "Extract Requirements",
      step3text: "Estimate Effort & Cost",
      step4text: "Export Report",
      feature1: "Extract Actors and Use Cases automatically",
      feature2: "Generate functional requirements in seconds",
      feature3: "AI-powered effort & cost estimations",
      feature4: "Export professional PDF/Excel reports",
      feature5: "Dark mode & multilingual support",
      welcome: "👋 Welcome to Esti-Use! Upload your first diagram and get instant estimates.",
      login: "Log In",
      signup: "Sign Up",
      getStarted: "Get Started - It's Free",
      toggleDark: "Dark Mode",
      toggleLight: "Light Mode",
      watchDemo: "Watch 2-Minute Demo",
      help: "Help Center",
      settings: "Settings",
      contact: "Contact Us",
      howItWorks: "How It Works"
    },
    ar: {
      subtitle: "تقدير ذكي مدعوم بالذكاء الاصطناعي ومخططات الحالات",
      lead: "قم برفع مخطط UML الخاص بك واحصل على تقديرات فورية بدقة تزيد عن 90٪",
      step1text: "رفع مخطط الحالات",
      step2text: "استخراج المتطلبات",
      step3text: "تقدير الجهد والتكلفة",
      step4text: "تصدير التقرير",
      feature1: "استخراج تلقائي للجهات الفاعلة وحالات الاستخدام",
      feature2: "إنشاء المتطلبات الوظيفية في ثوانٍ",
      feature3: "تقديرات الجهد والتكلفة بالذكاء الاصطناعي",
      feature4: "تصدير تقارير PDF/Excel احترافية",
      feature5: "الوضع المظلم ودعم متعدد اللغات",
      welcome: "👋 مرحبًا بكم في Esti-Use! ارفع مخططك الأول واحصل على تقديرات فورية.",
      login: "تسجيل الدخول",
      signup: "إنشاء حساب",
      getStarted: "ابدأ الآن - مجانًا",
      toggleDark: "الوضع المظلم",
      toggleLight: "الوضع الفاتح",
      watchDemo: "مشاهدة عرض دقيقتين",
      help: "مركز المساعدة",
      settings: "الإعدادات",
      contact: "اتصل بنا",
      howItWorks: "كيف يعمل"
    }
  };
  
  function initTranslations() {
    const languageSwitcher = document.getElementById('langSwitcher');
    if (!languageSwitcher) return;
  
    // Set initial language
    const savedLang = localStorage.getItem('estiuse-lang') || 'en';
    setLanguage(savedLang, false);
  
    // Handle language change
    languageSwitcher.addEventListener('change', (e) => {
      setLanguage(e.target.value, true);
    });
  }
  
  function setLanguage(lang, save = true) {
    if (!translations[lang]) return;
  
    // Update UI
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // Apply RTL-specific styles
    if (lang === 'ar') {
      document.body.classList.add('rtl');
    } else {
      document.body.classList.remove('rtl');
    }
  
    // Save preference
    if (save) {
      localStorage.setItem('estiuse-lang', lang);
    }
  
    // Apply translations
    applyTranslations(lang);
  }
  
  function applyTranslations(lang) {
    const t = translations[lang];
    if (!t) return;
  
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) {
        // Handle different element types
        if (el.tagName === 'INPUT' && el.placeholder !== undefined) {
          el.placeholder = t[key];
        } else {
          el.textContent = t[key];
        }
  
        // Update accessibility attributes
        if (el.hasAttribute('aria-label')) {
          el.setAttribute('aria-label', t[key]);
        }
        if (el.hasAttribute('title')) {
          el.setAttribute('title', t[key]);
        }
      }
    });
  }
  
  // 🎉 Welcome Toast (Optimized)
  function showWelcomeToast() {
    if (sessionStorage.getItem('estiuse-visited')) return;
    
    const toastEl = document.getElementById('welcomeToast');
    if (!toastEl) return;
  
    // Show toast with delay
    setTimeout(() => {
      const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 5000
      });
      toast.show();
      sessionStorage.setItem('estiuse-visited', 'true');
    }, 1000);
  }
  
  // 🖥️ System Preference Listeners
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('estiuse-dark')) {
      document.body.classList.toggle('dark-mode', e.matches);
    }

  });})