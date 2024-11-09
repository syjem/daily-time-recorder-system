import { successToast, deletedToast } from './helpers.js';

export const renderToast = (message, isDeleted = false) => {
  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.className =
    'fixed top-5 right-5 z-[100] flex flex-col gap-2 opacity-0 w-full max-w-sm text-gray-500 bg-white rounded-lg shadow-md dark:text-gray-400 dark:bg-gray-800 -translate-y-10 transform';
  toast.role = 'alert';
  toast.innerHTML = isDeleted ? deletedToast(message) : successToast(message);

  document.body.appendChild(toast);

  let closeTimeout;

  // Show toast with animation
  const showToast = () => {
    toast.classList.remove('opacity-0', '-translate-y-10');
    toast.classList.add(
      'opacity-100',
      'translate-y-0',
      'transition-transform',
      'ease-in-out'
    );
  };

  // Hide toast with animation
  const hideToast = () => {
    toast.classList.remove('opacity-100', 'translate-y-0');
    toast.classList.add(
      'opacity-0',
      '-translate-y-10',
      'transition-opacity',
      'duration-300'
    );
    setTimeout(() => {
      toast.remove();
    }, 500);
  };

  // Set a timeout to close the toast
  const startCloseTimeout = () => {
    closeTimeout = setTimeout(hideToast, 4000);
  };

  // Show the toast initially
  setTimeout(showToast, 300);

  // Pause close timeout on hover
  toast.addEventListener('mouseenter', () => clearTimeout(closeTimeout));

  // Resume close timeout on mouse leave
  toast.addEventListener('mouseleave', startCloseTimeout);

  // Start the close timeout initially
  startCloseTimeout();

  // Hide the toast when the close button is clicked
  toast.querySelector('button').addEventListener('click', hideToast);
};
