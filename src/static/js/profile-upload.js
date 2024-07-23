import { renderToast } from './toast.js';
import { avatarUploadIcon, loaderIcon, renderError } from './constants.js';

const fileInput = document.getElementById('fileInput');
const image = document.getElementById('profile-image');
const headerProfile = document.getElementById('header-profile');
const button = document.getElementById('upload-button');
const buttonSVG = document.getElementById('button-svg');
const deleteProfileButton = document.getElementById('delete-profile');
const errorEl = document.getElementById('file-error');

const uploadAvatar = async (event) => {
  const fileInput = event.target;
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append('file', file);

  buttonSVG.innerHTML = loaderIcon;
  button.setAttribute('disabled', true);

  try {
    const response = await fetch('/api/user/avatar', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      console.error('File upload failed:', response.statusText);
    }

    const data = await response.json();

    if (data.image) {
      image.src = data.image;
      headerProfile.src = data.image;
      errorEl.innerHTML = '';
      await new Promise((resolve) => setTimeout(resolve, 200));
      renderToast(data.message);
    } else {
      errorEl.innerHTML = data.error;
    }

    buttonSVG.innerHTML = avatarUploadIcon;
    button.removeAttribute('disabled');
    deleteProfileButton.removeAttribute('disabled');
  } catch (error) {
    console.error('Error uploading file:', error);
  }
};

const deleteAvatar = async () => {
  deleteProfileButton.setAttribute('disabled', true);
  deleteProfileButton.innerHTML = loaderIcon + 'Removing';
  try {
    const response = await fetch('/api/user/avatar', {
      method: 'DELETE',
    });

    if (!response.ok)
      throw new Error(`File delete failed: ${response.statusText}`);

    const data = await response.json();

    if (data.image) {
      image.src = data.image;
      headerProfile.src = data.image;
      errorEl.innerHTML = '';
      await new Promise((resolve) => setTimeout(resolve, 200));
      renderToast(data.message, true);
    } else {
      errorEl.innerHTML = data.error;
      deleteProfileButton.removeAttribute('disabled');
    }

    deleteProfileButton.innerHTML = 'Remove';
  } catch (error) {
    console.error('Error deleting profile picture:', error);
  }
};

fileInput.addEventListener('change', uploadAvatar);
deleteProfileButton.addEventListener('click', deleteAvatar);

// ------- ------- ------- ------- --------- //
// ------- ------- ------- ------- --------- //
// ------- Personal Information Form ------- //
// ------- ------- ------- ------- --------- //
// ------- ------- ------- ------- --------- //

const form = document.getElementById('personal-information-form');
const submitButton = form.querySelector('button');

const submitPersonalInfo = async (event) => {
  event.preventDefault();

  submitButton.innerHTML = loaderIcon + 'Saving';
  submitButton.setAttribute('disabled', true);

  const formData = new FormData(form);

  const response = await fetch('/api/user/personal_info', {
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
      console.error('Unknown error occurred');
    }
  } else {
    if (data.success) {
      renderToast(data.success);
    }
  }

  submitButton.removeAttribute('disabled');
  submitButton.innerHTML = 'Save all';
};

// Remove error messages for a specific field
const clearError = (event) => {
  const fieldName = event.target.name;

  const container = form.querySelector(`#${fieldName}_container`);
  if (container) {
    const errorElement = container.querySelector('p');
    if (errorElement) {
      container.removeChild(errorElement);
    }
  }
};

form.addEventListener('submit', submitPersonalInfo);
form.addEventListener('input', clearError);
