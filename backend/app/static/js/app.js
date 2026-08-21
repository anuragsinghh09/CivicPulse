document.addEventListener('DOMContentLoaded', function () {
  const previewInputs = document.querySelectorAll('[data-image-preview]');
  previewInputs.forEach((input) => {
    input.addEventListener('change', function () {
      const previewContainer = document.getElementById(input.dataset.imagePreview);
      if (!previewContainer) return;

      previewContainer.innerHTML = '';
      const files = Array.from(input.files || []).slice(0, 3);

      files.forEach((file) => {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = function (event) {
          const img = document.createElement('img');
          img.src = event.target.result;
          img.alt = 'Uploaded preview';
          img.className = 'img-fluid rounded';

          const box = document.createElement('div');
          box.className = 'preview-box';
          box.appendChild(img);
          previewContainer.appendChild(box);
        };
        reader.readAsDataURL(file);
      });
    });
  });

  const dismissButtons = document.querySelectorAll('[data-bs-dismiss="alert"]');
  dismissButtons.forEach((button) => {
    button.addEventListener('click', function () {
      const alert = button.closest('.alert');
      if (alert) {
        alert.remove();
      }
    });
  });

  const forms = document.querySelectorAll('form[data-validate]');
  forms.forEach((form) => {
    form.addEventListener('submit', function (event) {
      const requiredFields = form.querySelectorAll('[required]');
      let valid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          valid = false;
          field.classList.add('is-invalid');
        } else {
          field.classList.remove('is-invalid');
        }
      });

      if (!valid) {
        event.preventDefault();
        const alert = document.createElement('div');
        alert.className = 'alert alert-warning mt-3';
        alert.textContent = 'Please complete all required fields before submitting the form.';
        const existing = form.querySelector('.form-validation-message');
        if (existing) {
          existing.remove();
        }
        const wrapper = document.createElement('div');
        wrapper.className = 'form-validation-message';
        wrapper.appendChild(alert);
        form.appendChild(wrapper);
      }
    });
  });
});
