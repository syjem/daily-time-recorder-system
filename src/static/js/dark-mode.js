const themeToggleBtn = document.getElementById('theme-toggle');
const darkModeSwitch = document.getElementById('dark-mode');

if (
  localStorage.getItem('color-theme') === 'dark' ||
  (!('color-theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  document.documentElement.classList.add('dark');
  darkModeSwitch.checked = true;
} else {
  document.documentElement.classList.remove('dark');
  darkModeSwitch.checked = false;
}

let event = new Event('dark-mode');

themeToggleBtn.addEventListener('click', function () {
  // if set via local storage previously
  if (localStorage.getItem('color-theme')) {
    if (localStorage.getItem('color-theme') === 'light') {
      darkModeSwitch.checked = true;
      document.documentElement.classList.add('dark');
      localStorage.setItem('color-theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('color-theme', 'light');
      darkModeSwitch.checked = false;
    }

    // if NOT set via local storage previously
  } else {
    if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('color-theme', 'light');
    } else {
      document.documentElement.classList.add('dark');
      localStorage.setItem('color-theme', 'dark');
    }
  }

  document.dispatchEvent(event);
});
