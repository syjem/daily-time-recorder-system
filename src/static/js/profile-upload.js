import { renderToast } from './toast.js';
import { avatarUploadIcon, loaderIcon } from './constants.js';
import { renderError, renderEmploymentError, clearError } from './helpers.js';

const fileInput = document.getElementById('fileInput');
const image = document.getElementById('profile-image');
const headerProfile = document.getElementById('header-profile');
const button = document.getElementById('upload-button');
const deleteProfileButton = document.getElementById('delete-profile');
const errorEl = document.getElementById('file-error');
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

const uploadAvatar = async (event) => {
  const fileInput = event.target;
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append('file', file);

  button.innerHTML = loaderIcon + 'Uploading picture';
  button.setAttribute('disabled', true);
  deleteProfileButton.setAttribute('disabled', true);

  try {
    const response = await fetch('/api/user/avatar', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRF-Token': csrfToken,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      errorEl.innerHTML = data.error;
    }

    if (data.image) {
      errorEl.innerHTML = '';
      image.src = data.image;
      headerProfile.src = data.image;
      renderToast(data.message);
      deleteProfileButton.removeAttribute('disabled');
    } else {
      deleteProfileButton.setAttribute('disabled', true);
    }
  } catch (error) {
    console.error('Error uploading file:', error);
    errorEl.innerHTML =
      'An error occurred while uploading the file. Please try again.';
  } finally {
    button.innerHTML = avatarUploadIcon + 'Upload picture';
    button.removeAttribute('disabled');
  }
};

const deleteAvatar = async () => {
  button.setAttribute('disabled', true);
  deleteProfileButton.setAttribute('disabled', true);
  deleteProfileButton.innerHTML = loaderIcon + 'Removing';

  try {
    const response = await fetch('/api/user/avatar', {
      headers: {
        'X-CSRF-Token': csrfToken,
      },
      method: 'DELETE',
    });

    if (!response.ok) throw new Error(response.statusText);

    const data = await response.json();

    if (data.src) {
      image.src = data.src;
      headerProfile.src = data.src;
      errorEl.innerHTML = '';
      renderToast(data.message, true);
    }
  } catch (error) {
    errorEl.innerHTML =
      'An error occurred while deleting the profile picture. Please try again.';
  } finally {
    button.removeAttribute('disabled');
    deleteProfileButton.innerHTML = 'Remove';
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

// ------- ------- ------- ------- --------- //
// ------ Employment Information Form ------ //
// ------- ------- ------- ------- --------- //

const employmentForm = document.getElementById('employment-information-form');
const submit_btn = employmentForm.querySelector('button');

const submitEmploymentForm = async (event) => {
  event.preventDefault();

  submit_btn.innerHTML = loaderIcon + 'Saving';
  submit_btn.setAttribute('disabled', true);

  const formData = new FormData(employmentForm);

  try {
    const response = await fetch('/api/user/employment_information', {
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
          renderEmploymentError(employmentForm, error.field, error.message);
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
    submit_btn.removeAttribute('disabled');
    submit_btn.innerHTML = 'Save all';
  }
};

employmentForm.addEventListener('submit', submitEmploymentForm);
// employmentForm.addEventListener('input', clearError);
