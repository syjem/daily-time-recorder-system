import { loaderIcon } from '../constants.js';
import { renderError, redirect } from '../helpers.js';
import { renderToast } from '../toast.js';

document.addEventListener('DOMContentLoaded', () => {
  const csrfToken = document.querySelector("meta[name='csrf-token']").content;
  const form = document.getElementById('employment-info-form');
  const submitButton = form.querySelector("button[type='submit']");

  form.addEventListener('submit', submitHandler);

  async function submitHandler(event) {
    event.preventDefault();

    submitButton.innerHTML = loaderIcon + 'Saving';
    submitButton.setAttribute('disabled', true);

    const formData = new FormData(form);
    const fields = {};

    formData.forEach((value, key) => {
      fields[key] = value;
    });

    const location = window.location.href;
    const parts = location.split('/');
    const userId = parts[parts.length - 1];

    const url = `/api/admin/user/${userId}/update`;

    try {
      const response = await fetch(url, {
        method: 'PUT',
        body: JSON.stringify(fields),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': csrfToken,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.errors) {
          data.errors.forEach((error) => {
            renderError(form, error.field, error.message);
          });
        }
      } else {
        if (data.success) {
          localStorage.setItem('toastMessage', data.success);
          redirect(data.redirect);
        }
      }
    } catch (error) {
      renderToast('An error occurred while adding the user.', true);
    } finally {
      submitButton.innerHTML = 'Save';
      submitButton.removeAttribute('disabled');
    }
  }
});
