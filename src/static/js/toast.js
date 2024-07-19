export const renderToast = (message) => {
  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.className =
    'fixed top-5 right-5 z-[100] flex flex-col gap-2 opacity-0 w-full max-w-sm text-gray-500 bg-white rounded-lg shadow-md dark:text-gray-400 dark:bg-gray-800 -translate-y-10 transform';
  toast.role = 'alert';
  toast.innerHTML = `
      <div class="border border-sky-700 p-4 flex items-center rounded-lg">
        <p class="text-sm text-sky-800 dark:text-sky-300">${message}</p>
        <div class="flex items-center ms-auto space-x-2 rtl:space-x-reverse">
          <button
            type="button"
            class="ms-auto -mx-1.5 -my-1.5 text-inherit bg-white rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700"
            aria-label="Close">
            <span class="sr-only">Close</span>
            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
            </svg>
          </button>
        </div>
      </div>
    `;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('opacity-0', '-translate-y-10');
    toast.classList.add(
      'opacity-100',
      'translate-y-0',
      'transition-transform',
      'ease-in-out'
    );
  }, 100);

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
