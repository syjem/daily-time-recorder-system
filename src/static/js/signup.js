const removeErrorOnChange = () => {
  const email = document.getElementById('email');
  const error = document.getElementById('error');

  email.addEventListener('input', () => {
    error.textContent = '';
    error.style.display = 'none';
  });
};

removeErrorOnChange();
