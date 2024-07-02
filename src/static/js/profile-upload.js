const fileInput = document.getElementById('fileInput');
const image = document.getElementById('profile-image');

fileInput.addEventListener('change', async (event) => {
  const fileInput = event.target;
  const file = fileInput.files[0];

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('/user/upload/profile', {
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
