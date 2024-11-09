import { renderError, clearError, redirect } from '../helpers.js';
import { renderToast } from '../toast.js';
import { togglePassword } from '../utils/togglePasswordIcon.js';

const toastMessage = localStorage.getItem('toastMessage');
if (toastMessage) {
  renderToast(toastMessage);
  localStorage.removeItem('toastMessage');
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('add-user-form');

  form.addEventListener('submit', submitHandler);
  form.addEventListener('input', clearError);

  async function submitHandler(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const url = '/api/admin/user/add';

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.errors) {
          data.errors.forEach((error) => {
            renderError(form, error.field, error.message);
          });
        } else {
          renderError(form, 'email', data.error);
        }
      } else {
        if (data.success) {
          localStorage.setItem('toastMessage', data.success);
          window.location.href = data.redirect;
        }
      }
    } catch (error) {
      console.error('Failed request: ', error);
    }
  }

  function clearError(event) {
    const fieldName = event.target.name;

    const container = form.querySelector(`#${fieldName}_container`);
    if (container) {
      const errorElement = container.querySelector('p');
      if (errorElement) {
        container.removeChild(errorElement);
      }
    }
  }

  togglePassword();
});
