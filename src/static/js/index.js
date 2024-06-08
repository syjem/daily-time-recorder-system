document.addEventListener('readystatechange', () => {
  const progressBar = document.getElementById('progress-bar');

  if (document.readyState === 'interactive') {
    progressBar.style.width = '50%';
  } else if (document.readyState === 'complete') {
    progressBar.style.width = '100%';

    // Hide the progress bar after some time
    setTimeout(() => {
      progressBar.style.opacity = '0';
    }, 500);

    // Remove the progress bar from the DOM after it fades out
    setTimeout(() => {
      progressBar.style.display = 'none';
    }, 1000);
  }
});
