import { renderToast } from '../toast.js';
import { loaderIcon } from '../constants.js';

document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button[data-user-id]');
  const form = document.getElementById('delete-user-form');
  const submitButton = form.querySelector("button[type='submit']");
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  let user_id = '';

  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const userId = button.getAttribute('data-user-id');
      if (userId) {
        user_id = userId;
      }
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    submitButton.innerHTML = loaderIcon + 'Deleting';
    submitButton.setAttribute('disabled', true);

    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get('page') || 1;

    const url = `/api/admin/user/${user_id}/delete?page=${currentPage}`;

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRF-Token': csrfToken,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.error) renderToast(data.error, true);
        if (data.message) renderToast(data.message, true);
      }

      if (data.success) {
        localStorage.setItem('toastMessage', data.success);
        window.location.href = data.redirect;
      }
    } catch (error) {
      renderToast('An error occurred while deleting the user.', true);
    } finally {
      submitButton.innerHTML = "Yes, I'm sure";
      submitButton.removeAttribute('disabled');
    }
  });
});
