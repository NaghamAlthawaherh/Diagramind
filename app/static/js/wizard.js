document.addEventListener('DOMContentLoaded', function () {
    const steps = document.querySelectorAll(".wizard-step");
    const contents = document.querySelectorAll(".wizard-content");
    const nextBtn = document.getElementById("nextBtn");
    const backBtn = document.getElementById("backBtn");
    const finishBtn = document.getElementById("finishBtn");
  
    let currentStep = 0;
  
    function updateWizard() {
      steps.forEach((step, index) => {
        step.classList.toggle("active", index === currentStep);
      });
  
      contents.forEach((content, index) => {
        content.classList.toggle("active", index === currentStep);
      });
  
      backBtn.disabled = currentStep === 0;
      nextBtn.style.display = currentStep === steps.length - 1 ? "none" : "inline-block";
      finishBtn.style.display = currentStep === steps.length - 1 ? "inline-block" : "none";
    }
  
    nextBtn.addEventListener("click", () => {
      if (currentStep < steps.length - 1) {
        currentStep++;
        updateWizard();
      }
    });
  
    backBtn.addEventListener("click", () => {
      if (currentStep > 0) {
        currentStep--;
        updateWizard();
      }
    });
  
    finishBtn.addEventListener("click", () => {
      showToast("Completed", "You have successfully completed the wizard!", "success");
    });
  
    updateWizard();
  });
  
  function showToast(title, message, type = 'success') {
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
      toastContainer = document.createElement('div'); // ✅ صححنا الاسم هون
      toastContainer.id = 'toastContainer';
      toastContainer.className = 'toast-container';
      document.body.appendChild(toastContainer);
    }
  
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
  