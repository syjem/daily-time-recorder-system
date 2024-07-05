const fileInput = document.getElementById('fileInput');
const image = document.getElementById('profile-image');

fileInput.addEventListener('change', async (event) => {
  const fileInput = event.target;
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/api/upload/user/profile', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      console.error('File upload failed:', response.statusText);
    }

    const result = await response.json();
    image.src = result.image;
  } catch (error) {
    console.error('Error uploading file:', error);
  }
});

const btn = document.getElementById('edit-profile');
const viewProfile = document.querySelector('div[data-profile-view]');
const editProfile = document.querySelector('form[data-profile-edit]');
const nameInput = document.getElementById('name');
const currentUserName = document.getElementById('currentUserName').innerText;
const nameVale = (document.getElementById('name').value = currentUserName);

btn.addEventListener('click', () => {
  viewProfile.style.display = 'none';
  editProfile.style.display = 'block';
  nameInput.focus();
  btn.style.display = 'none';
});
