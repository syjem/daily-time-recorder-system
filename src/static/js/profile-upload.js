const fileInput = document.getElementById('fileInput');

fileInput.addEventListener('onChange', (event) => {
  async (event) => {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/profile/upload/pic', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        console.error('File upload failed:', response.statusText);
      }

      const result = await response.json();
      console.log('File uploaded successfully:', result);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };
});
