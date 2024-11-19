import { loaderIcon, avatarUploadIcon } from '../constants.js';
import { renderToast } from '../toast.js';

document.addEventListener('DOMContentLoaded', () => {
  const csrfToken = document.querySelector("meta[name='csrf-token']").content;
  const fileInput = document.getElementById('fileInput');
  const uploadButton = document.getElementById('upload-button');
  const errorEl = document.getElementById('upload-error');
  const userAvatarEl = document.getElementById('user-avatar');
  const removeAvatarButton = document.getElementById('remove-avatar');

  fileInput.addEventListener('change', submitHandler);

  async function submitHandler(event) {
    const file = event.target.files[0];

    if (!file) {
      errorEl.innerText = 'Please select a file to upload.';
      return;
    }

    setLoadingState(uploadButton, 'Uploading');
    errorEl.innerText = '';

    const location = window.location.href;
    const parts = location.split('/');
    const userId = parts[parts.length - 1];

    const url = `/api/admin/user/avatar/${userId}`;

    try {
      const formData = new FormData();
      formData.append('avatar', file);

      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRF-Token': csrfToken,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        errorEl.innerText = data.error || 'An unexpected error occurred.';
        return;
      }

      if (data.avatar) {
        userAvatarEl.src = data.avatar;
        renderToast(data.message);
        removeAvatarButton.removeAttribute('disabled');
      }
    } catch (error) {
      errorEl.innerText =
        'An error occurred while uploading the file. Please try again.';
    } finally {
      resetButtonState(uploadButton, 'Upload avatar');
    }
  }
});

function setLoadingState(button, loadingText) {
  button.innerHTML = loaderIcon + loadingText;
  button.setAttribute('disabled', true);
}

function resetButtonState(button, defaultText) {
  button.innerHTML = avatarUploadIcon + defaultText;
  button.removeAttribute('disabled');
}
