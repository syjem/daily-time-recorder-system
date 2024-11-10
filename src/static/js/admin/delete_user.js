// Populate the form input value with the User ID when on delete button click.
// Send the data to the server for deletions.
import { renderToast } from '../toast.js';

document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button[data-user-id]');
  const form = document.getElementById('delete-user-form');
  const userIdInput = form.querySelector('#user-id-input');

  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const userId = button.getAttribute('data-user-id');
      userIdInput.value = userId;
    });
  });

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const url = `/api/admin/user/${userIdInput.value}/delete`;
    const formData = new FormData(form);

    try {
      const response = await fetch(url, {
        method: 'DELETE',
        body: formData,
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
    }
  });
});
