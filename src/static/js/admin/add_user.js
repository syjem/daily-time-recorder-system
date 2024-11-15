import { renderError, clearError, redirect } from '../helpers.js';
import { renderToast } from '../toast.js';
import { togglePassword } from '../utils/togglePasswordIcon.js';
import { loaderIcon, plusIcon } from '../constants.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('add-user-form');
  const submitButton = form.querySelector("button[type='submit']");
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  form.addEventListener('submit', submitHandler);
  form.addEventListener('input', clearError);

  async function submitHandler(event) {
    event.preventDefault();

    submitButton.innerHTML = loaderIcon + 'Adding';
    submitButton.setAttribute('disabled', true);

    const formData = new FormData(form);

    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get('page') || 1;

    const url = `/api/admin/user/add?page=${currentPage}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRF-Token': csrfToken,
        },
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
      renderToast('An error occurred while adding the user.', true);
    } finally {
      submitButton.innerHTML = plusIcon + 'Add user';
      submitButton.removeAttribute('disabled');
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
