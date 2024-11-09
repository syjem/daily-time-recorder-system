export const renderError = (form, field, message) => {
  const first_name = form.querySelector('#first_name_container');
  const last_name = form.querySelector('#last_name_container');
  const email = form.querySelector('#email_container');
  const birthday = form.querySelector('#birthday_container');
  const position = form.querySelector('#position_container');
  const password = form.querySelector('#password_container');

  const removeExistingError = (container) => {
    const existingError = container.querySelector('p');
    if (existingError) {
      container.removeChild(existingError);
    }
  };

  const errorElement = document.createElement('p');
  errorElement.className = 'text-sm text-red-500 mt-2';
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
  if (field === 'position') {
    removeExistingError(position);
    position.appendChild(errorElement);
  }
  if (field === 'password') {
    removeExistingError(password);
    password.appendChild(errorElement);
  }
};

// Remove error messages for a specific field
export const clearError = (event) => {
  const fieldName = event.target.name;

  const container = form.querySelector(`#${fieldName}_container`);
  if (container) {
    const errorElement = container.querySelector('p');
    if (errorElement) {
      container.removeChild(errorElement);
    }
  }
};

export const successToast = (message) => {
  const toaster = `
      <div class="border dark:border-green-800 p-4 flex items-center rounded-lg">
          <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200">
              <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
              </svg>
              <span class="sr-only">Check icon</span>
          </div>
          <p class="ms-2 text-sm text-green-800 dark:text-green-200">${message}</p>
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
      <div class="border dark:border-red-700/85 p-4 flex items-center rounded-lg">
          <div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200">
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
          </svg>
          <span class="sr-only">Error icon</span>
          </div>
          <p class="ms-2 text-sm text-red-800 dark:text-red-100">${message}</p>
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

export const renderEmploymentError = (form, field, message) => {
  const company = form.querySelector('#company_container');
  const employee_id = form.querySelector('#employee_id_container');
  const position = form.querySelector('#position_container');
  const hired_date = form.querySelector('#hired_date_container');

  const removeExistingError = (container) => {
    const existingError = container.querySelector('p');
    if (existingError) {
      container.removeChild(existingError);
    }
  };

  const errorElement = document.createElement('p');
  errorElement.className = 'text-sm text-red-500';
  errorElement.innerText = message;

  if (field === 'company') {
    removeExistingError(company);
    company.appendChild(errorElement);
  }
  if (field === 'employee_id') {
    removeExistingError(employee_id);
    employee_id.appendChild(errorElement);
  }
  if (field === 'position') {
    removeExistingError(position);
    position.appendChild(errorElement);
  }

  if (field === 'hired_date') {
    removeExistingError(hired_date);
    position.appendChild(errorElement);
  }
};

export const redirect = (url) => {
  window.location.href = url;
};
