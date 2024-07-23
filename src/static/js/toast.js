import { successToast, deletedToast } from './constants.js';

export const renderToast = (message, isDeleted = false) => {
  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.className =
    'fixed top-5 right-5 z-[100] flex flex-col gap-2 opacity-0 w-full max-w-sm text-gray-500 bg-white rounded-lg shadow-md dark:text-gray-400 dark:bg-gray-800 -translate-y-10 transform';
  toast.role = 'alert';
  toast.innerHTML = isDeleted ? deletedToast(message) : successToast(message);

  document.body.appendChild(toast);

  // Fade-in effect for the toast
  setTimeout(() => {
    toast.classList.remove('opacity-0', '-translate-y-10');
    toast.classList.add(
      'opacity-100',
      'translate-y-0',
      'transition-transform',
      'ease-in-out'
    );
  }, 100);

  // Automatically hide the toast after 3 seconds
  setTimeout(() => {
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
  }, 3000);

  // Hide the toast when the close button is clicked
  toast.querySelector('button').addEventListener('click', () => {
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
  });
};
