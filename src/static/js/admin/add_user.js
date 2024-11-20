import { renderToast } from '../toast.js';
import { renderError, redirect } from '../helpers.js';
import { loaderIcon, plusIcon } from '../constants.js';
import { togglePassword } from '../utils/togglePasswordIcon.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('add-user-form');
  const submitButton = form.querySelector("button[type='submit']");
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  form.addEventListener('submit', submitHandler);
  form.addEventListener('input', clearError);

  async function submitHandler(event) {
    event.preventDefault();

    setLoadingState(submitButton, 'Adding');

    const formData = new FormData(form);

    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get('page');

    let url = '';

    currentPage
      ? (url = `/api/admin/user/add?page=${currentPage}`)
      : (url = '/api/admin/user/add');

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
        } else if (data.email_error) {
          renderError(form, 'email', data.email_error);
        } else {
          renderToast(data.error, true);
        }
      }

      if (data.success) {
        localStorage.setItem('toastMessage', data.success);
        redirect(data.redirect);
      }
    } catch (error) {
      renderToast('An error occurred while adding the user.', true);
    } finally {
      resetButtonState(submitButton, 'Add user');
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

  function setLoadingState(button, loadingText) {
    button.innerHTML = loaderIcon + loadingText;
    button.setAttribute('disabled', true);
  }

  function resetButtonState(button, defaultText) {
    button.innerHTML = plusIcon + defaultText;
    button.removeAttribute('disabled');
  }

  togglePassword();
});
