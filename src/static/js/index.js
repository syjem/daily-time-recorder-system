document.addEventListener('readystatechange', () => {
  const progressBar = document.getElementById('progress-bar');

  if (document.readyState === 'interactive') {
    progressBar.style.width = '50%';
  } else if (document.readyState === 'complete') {
    progressBar.style.width = '100%';

    setTimeout(() => {
      progressBar.style.opacity = '0';
    }, 500);

    setTimeout(() => {
      progressBar.style.display = 'none';
    }, 1000);
  }
});
