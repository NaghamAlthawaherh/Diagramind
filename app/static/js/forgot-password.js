/**
 * Password Reset Module - Secure Password Reset Flow
 * @module ForgotPassword
 * @description Handles the complete password reset process including validation,
 * CAPTCHA verification, rate limiting, and success state management.
 */

class PasswordReset {
    // Configuration constants
    static CONFIG = {
      RESEND_DELAY: 30000, // 30 seconds cooldown
      MAX_ATTEMPTS: 5,
      ATTEMPT_EXPIRE_TIME: 3600000, // 1 hour
      CAPTCHA_ACTION: 'forgot_password',
      STORAGE_KEYS: {
        DARK_MODE: 'estiuse-dark-mode',
        ATTEMPTS: 'resetAttempts'
      }
    };
  
    constructor() {
      this.form = document.getElementById('resetPasswordForm');
      this.emailInput = document.getElementById('email');
      this.resetBtn = document.getElementById('resetBtn');
      this.spinner = document.getElementById('spinner');
      this.toastEl = document.getElementById('toast');
      this.toastMessage = document.getElementById('toastMessage');
      
      this.init();
    }
  
    /**
     * Initialize the password reset module
     */
    init() {
      this.setupDarkMode();
      this.setupFormValidation();
      this.setupEventListeners();
      
      // Load any saved attempts from localStorage
      this.attempts = JSON.parse(
        localStorage.getItem(PasswordReset.CONFIG.STORAGE_KEYS.ATTEMPTS) || []
      );
    }
  
    /**
     * Setup dark mode toggle functionality
     */
    setupDarkMode() {
      const toggleBtn = document.getElementById('toggleDark');
      const savedMode = localStorage.getItem(
        PasswordReset.CONFIG.STORAGE_KEYS.DARK_MODE
      );
  
      // Apply saved mode
      if (savedMode === 'enabled') {
        document.body.classList.add('dark-mode');
        this.updateDarkModeButton(toggleBtn, true);
      }
  
      // Toggle handler
      toggleBtn.addEventListener('click', () => {
        const isDark = document.body.classList.toggle('dark-mode');
        localStorage.setItem(
          PasswordReset.CONFIG.STORAGE_KEYS.DARK_MODE,
          isDark ? 'enabled' : 'disabled'
        );
        this.updateDarkModeButton(toggleBtn, isDark);
      });
    }
  
    /**
     * Update dark mode button state
     * @param {HTMLElement} button - The toggle button
     * @param {boolean} isDark - Current dark mode state
     */
    updateDarkModeButton(button, isDark) {
      button.innerHTML = isDark
        ? '<i class="fas fa-sun me-1"></i> Light Mode'
        : '<i class="fas fa-moon me-1"></i> Dark Mode';
      button.setAttribute('aria-pressed', isDark);
    }
  
    /**
     * Setup real-time form validation
     */
    setupFormValidation() {
      this.emailInput.addEventListener('input', () => {
        const isValid = this.validateEmail(this.emailInput.value.trim());
        this.emailInput.classList.toggle('is-invalid', !isValid);
        this.emailInput.classList.toggle('is-valid', isValid);
      });
    }
  
    /**
     * Setup event listeners
     */
    setupEventListeners() {
      this.form.addEventListener('submit', this.handleSubmit.bind(this));
    }
  
    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean} Validation result
     */
    validateEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
      return re.test(email);
    }
  
    /**
     * Execute reCAPTCHA verification
     * @returns {Promise<string>} CAPTCHA token
     */
    async executeCaptcha() {
      try {
        return await new Promise((resolve, reject) => {
          if (!window.grecaptcha) {
            reject(new Error('CAPTCHA service unavailable'));
            return;
          }
  
          grecaptcha.ready(() => {
            grecaptcha
              .execute('YOUR_RECAPTCHA_SITE_KEY', {
                action: PasswordReset.CONFIG.CAPTCHA_ACTION
              })
              .then(resolve)
              .catch(reject);
          });
        });
      } catch (error) {
        console.error('CAPTCHA Error:', error);
        throw new Error('Failed to verify you are human. Please try again.');
      }
    }
  
    /**
     * Show toast notification
     * @param {string} message - Message to display
     * @param {string} type - Toast type (success, danger, warning, info)
     */
    showToast(message, type = 'info') {
      const icons = {
        success: '<i class="fas fa-check-circle me-2"></i>',
        danger: '<i class="fas fa-exclamation-circle me-2"></i>',
        warning: '<i class="fas fa-exclamation-triangle me-2"></i>',
        info: '<i class="fas fa-info-circle me-2"></i>'
      };
  
      this.toastMessage.innerHTML = `${icons[type] || ''} ${message}`;
      this.toastEl.className = `toast align-items-center text-bg-${type} border-0 show`;
  
      const toast = new bootstrap.Toast(this.toastEl, {
        autohide: true,
        delay: 5000
      });
      toast.show();
    }
  
    /**
     * Handle form submission
     * @param {Event} e - Form submit event
     */
    async handleSubmit(e) {
      e.preventDefault();
      
      const email = this.emailInput.value.trim();
  
      // Validate email
      if (!this.validateEmail(email)) {
        this.showToast('Please enter a valid email address', 'danger');
        return;
      }
  
      // Check rate limits
      if (this.isRateLimited(email)) {
        this.showToast(
          'Too many attempts. Please try again later.',
          'warning'
        );
        return;
      }
  
      // Update UI state
      this.setLoadingState(true);
  
      try {
        // Verify CAPTCHA
        const captchaToken = await this.executeCaptcha();
  
        // Simulate API call - Replace with actual fetch
        await this.sendResetRequest(email, captchaToken);
  
        // Log attempt
        this.logAttempt(email);
  
        // Show success state
        this.showSuccessState(email);
      } catch (error) {
        console.error('Reset Error:', error);
        this.showToast(error.message, 'danger');
      } finally {
        this.setLoadingState(false);
      }
    }
  
    /**
     * Check if user is rate limited
     * @param {string} email - User email
     * @returns {boolean} Rate limited status
     */
    isRateLimited(email) {
      const now = Date.now();
      const recentAttempts = this.attempts.filter(
        attempt => now - attempt.time < PasswordReset.CONFIG.ATTEMPT_EXPIRE_TIME
      );
      
      return recentAttempts.length >= PasswordReset.CONFIG.MAX_ATTEMPTS;
    }
  
    /**
     * Log reset attempt
     * @param {string} email - User email
     */
    logAttempt(email) {
      this.attempts.push({
        email,
        time: Date.now()
      });
      
      localStorage.setItem(
        PasswordReset.CONFIG.STORAGE_KEYS.ATTEMPTS,
        JSON.stringify(this.attempts)
      );
    }
  
    /**
     * Set loading state
     * @param {boolean} isLoading - Loading state
     */
    setLoadingState(isLoading) {
      this.resetBtn.disabled = isLoading;
      this.spinner.classList.toggle('d-none', !isLoading);
      this.emailInput.readOnly = isLoading;
    }
  
    /**
     * Simulate reset request (Replace with actual API call)
     * @param {string} email - User email
     * @param {string} captchaToken - CAPTCHA token
     */
    async sendResetRequest(email, captchaToken) {
      // This is a simulation - Replace with actual fetch
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          // Simulate 10% failure rate for demo
          if (Math.random() < 0.1) {
            reject(new Error('Network error occurred. Please try again.'));
          } else {
            resolve();
          }
        }, 1500);
      });
    }
  
    /**
     * Show success state
     * @param {string} email - User email
     */
    showSuccessState(email) {
      this.form.innerHTML = `
        <div class="reset-success text-center animate__animated animate__fadeIn">
          <div class="mb-4">
            <svg width="64" height="64" viewBox="0 0 24 24" class="text-success">
              <path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10s10-4.5 10-10S17.5 2 12 2m-2 15l-5-5l1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9Z"/>
            </svg>
          </div>
          <h3 class="mb-3">Reset Link Sent!</h3>
          <p class="text-muted mb-4">
            We've sent password reset instructions to<br>
            <strong class="text-primary">${email}</strong>
          </p>
          
          <div id="resendContainer" class="mb-4">
            <p class="small text-muted mb-2">Didn't receive the email?</p>
            <button id="resendBtn" class="btn btn-outline-primary btn-sm" disabled>
              Resend Link (<span id="countdown">30</span>s)
            </button>
          </div>
          
          <div class="d-grid gap-2">
            <a href="login.html" class="btn btn-primary">
              <i class="fas fa-arrow-left me-2"></i> Back to Login
            </a>
          </div>
        </div>
      `;
  
      this.startResendCountdown();
    }
  
    /**
     * Start resend countdown timer
     */
    startResendCountdown() {
      const resendBtn = document.getElementById('resendBtn');
      const countdownEl = document.getElementById('countdown');
      let seconds = PasswordReset.CONFIG.RESEND_DELAY / 1000;
  
      const timer = setInterval(() => {
        seconds--;
        countdownEl.textContent = seconds;
  
        if (seconds <= 0) {
          clearInterval(timer);
          resendBtn.disabled = false;
          resendBtn.innerHTML = 'Resend Link';
        }
      }, 1000);
  
      resendBtn.addEventListener('click', () => {
        clearInterval(timer);
        window.location.reload();
      });
    }
  }
  
  // Initialize when DOM is fully loaded
  document.addEventListener('DOMContentLoaded', () => {
    // Feature detection
    if (!window.Promise || !window.fetch) {
      document.getElementById('resetPasswordForm').innerHTML = `
        <div class="alert alert-danger">
          <i class="fas fa-exclamation-triangle me-2"></i>
          Your browser is not supported. Please update to the latest version.
        </div>
      `;
      return;
    }
  
    // Initialize password reset flow
    new PasswordReset();
  });