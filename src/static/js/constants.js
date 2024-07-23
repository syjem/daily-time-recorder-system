export const loaderIcon = `
    <svg aria-hidden="true" role="status" class="w-4 h-4 text-white animate-spin mr-2 -ml-1" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
      <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
    </svg>
    `;

export const avatarUploadIcon = `
    <svg
      class="w-4 h-4 mr-2 -ml-1"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg">
      <path
        d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z"></path>
      <path d="M9 13h2v5a1 1 0 11-2 0v-5z"></path>
    </svg>
    `;

export const successToast = (message) => {
  const toaster = `
    <div class="border dark:border-green-700 p-4 flex items-center rounded-lg">
        <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-400 bg-green-100 rounded-lg dark:bg-green-700 dark:text-green-500">
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
            </svg>
            <span class="sr-only">Check icon</span>
        </div>
        <p class="ms-2 text-sm text-green-800 dark:text-green-500">${message}</p>
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

  return toaster;
};

export const deletedToast = (message) => {
  const toaster = `
    <div class="border dark:border-gray-600 p-4 flex items-center rounded-lg">
        <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-400 bg-red-100 rounded-lg dark:bg-red-700 dark:text-red-200">
          <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
        </svg>
        <span class="sr-only">Error icon</span>
        </div>
        <p class="ms-2 text-sm text-red-800 dark:text-red-300">${message}</p>
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

  return toaster;
};

export const renderError = (form, field, message) => {
  const first_name = form.querySelector('#first_name_container');
  const last_name = form.querySelector('#last_name_container');
  const email = form.querySelector('#email_container');
  const birthday = form.querySelector('#birthday_container');

  const removeExistingError = (container) => {
    const existingError = container.querySelector('p');
    if (existingError) {
      container.removeChild(existingError);
    }
  };

  const errorElement = document.createElement('p');
  errorElement.className = 'text-sm text-red-500';
  errorElement.innerText = message;

  if (field === 'first_name') {
    removeExistingError(first_name);
    first_name.appendChild(errorElement);
  }
  if (field === 'last_name') {
    removeExistingError(last_name);
    last_name.appendChild(errorElement);
  }
  if (field === 'email') {
    removeExistingError(email);
    email.appendChild(errorElement);
  }
  if (field === 'birthday') {
    removeExistingError(birthday);
    birthday.appendChild(errorElement);
  }
};
