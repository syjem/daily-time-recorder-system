import { renderToast } from './toast.js';
import { avatarUploadIcon, loaderIcon } from './constants.js';
import { renderError, clearError } from './helpers.js';

const fileInput = document.getElementById('fileInput');
const image = document.getElementById('profile-image');
const headerProfile = document.getElementById('header-profile');
const button = document.getElementById('upload-button');
const deleteProfileButton = document.getElementById('delete-profile');
const errorEl = document.getElementById('file-error');

let action = 'Uploading picture';

const uploadAvatar = async (event) => {
  const fileInput = event.target;
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append('file', file);

  button.innerHTML = loaderIcon + action;
  button.setAttribute('disabled', true);
  deleteProfileButton.setAttribute('disabled', true);

  try {
    const response = await fetch('/api/user/avatar', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      errorEl.innerHTML = data.error;

      if (data.image_file) {
        button.innerHTML = avatarUploadIcon + 'Update picture';
      } else {
        button.innerHTML = avatarUploadIcon + 'Upload picture';
      }
    }

    if (data.image) {
      errorEl.innerHTML = '';
      image.src = data.image;
      headerProfile.src = data.image;
      await new Promise((resolve) => setTimeout(resolve, 200));
      renderToast(data.message);
      action = 'Updating picture';
      button.innerHTML = avatarUploadIcon + 'Update picture';
      button.removeAttribute('disabled');
      deleteProfileButton.removeAttribute('disabled');
    }
  } catch (error) {
    console.error('Error uploading file:', error);
    errorEl.innerHTML =
      'An error occurred while uploading the file. Please try again.';
  } finally {
    button.removeAttribute('disabled');
  }
};

const deleteAvatar = async () => {
  deleteProfileButton.setAttribute('disabled', true);
  deleteProfileButton.innerHTML = loaderIcon + 'Removing';

  try {
    const response = await fetch('/api/user/avatar', {
      method: 'DELETE',
    });

    if (!response.ok) throw new Error(response.statusText);

    const data = await response.json();

    if (data.src) {
      image.src = data.src;
      headerProfile.src = data.src;
      errorEl.innerHTML = '';
      await new Promise((resolve) => setTimeout(resolve, 200));
      renderToast(data.message, true);
    }
  } catch (error) {
    console.error('Error deleting profile picture:', error);
    errorEl.innerHTML =
      'An error occurred while deleting the profile picture. Please try again.';
  } finally {
    action = 'Uploading picture';
    button.innerHTML = avatarUploadIcon + 'Upload picture';
    deleteProfileButton.innerHTML = 'Remove';
    deleteProfileButton.removeAttribute('disabled');
  }
};

fileInput.addEventListener('change', uploadAvatar);
deleteProfileButton.addEventListener('click', deleteAvatar);

// ------- ------- ------- ------- --------- //
// ------- Personal Information Form ------- //
// ------- ------- ------- ------- --------- //

const form = document.getElementById('personal-information-form');
const submitButton = form.querySelector('button');

const submitPersonalInfo = async (event) => {
  event.preventDefault();

  submitButton.innerHTML = loaderIcon + 'Saving';
  submitButton.setAttribute('disabled', true);

  const formData = new FormData(form);

  try {
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
  } catch (error) {
    console.error('Failed request: ', error);
  } finally {
    submitButton.removeAttribute('disabled');
    submitButton.innerHTML = 'Save all';
  }
};

form.addEventListener('submit', submitPersonalInfo);
form.addEventListener('input', clearError);
