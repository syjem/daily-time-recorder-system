export default function updateTable(users) {
  const tableBody = document.getElementById('table-body');
  tableBody.innerHTML = '';

  users.forEach((user) => {
    const tableRow = document.createElement('tr');
    tableRow.className = 'hover:bg-gray-100 dark:hover:bg-gray-700';

    tableRow.innerHTML = `
        <td class="flex items-center p-4 mr-12 space-x-6 whitespace-nowrap">
        ${
          user.avatar
            ? `<img
              class="w-10 h-10 rounded-full"
              src="/static/assets/users/${user.avatar}"
              alt="${user.first_name} ${user.last_name} avatar"
            />`
            : `<div class="relative w-10 h-10 overflow-hidden bg-gray-300 rounded-full dark:bg-gray-600">
              <svg
                class="absolute w-12 h-12 text-gray-400 -left-1"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg">
                <path
                  fill-rule="evenodd"
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                  clip-rule="evenodd"></path>
              </svg>
            </div>`
        }
        <div class="text-sm font-normal text-gray-500 dark:text-gray-400">
          <div
            class="text-base font-semibold text-gray-900 dark:text-white capitalize">
            ${user.first_name} ${user.last_name}
          </div>
          <div class="text-sm font-normal text-gray-500 dark:text-gray-400">
            ${user.email}
          </div>
        </div>
      </td>
      <td
        class="p-4 text-base font-normal text-gray-900 text-ellipsis whitespace-nowrap dark:text-white capitalize">
        ${
          user.employment_data
            ? user.employment_data.map((employment) => employment.company)
            : ''
        }
      </td>
      <td
        class="p-4 text-base font-medium text-gray-900 whitespace-nowrap dark:text-white capitalize">
        ${
          user.employment_data
            ? user.employment_data.map((employment) => employment.position)
            : ''
        }
      </td>

      <td class="p-4 space-x-2 whitespace-nowrap">
        <a
          href="/admin/user/${user.id}"
          type="button"
          class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
          <svg class="w-[18px] h-[18px] mr-2" 
          aria-hidden="true" 
          xmlns="http://www.w3.org/2000/svg" 
          fill="currentColor" 
          viewBox="0 0 24 24">
            <path fill-rule="evenodd" 
            d="M5 8a4 4 0 1 1 7.796 1.263l-2.533 2.534A4 4 0 0 1 5 8Zm4.06 5H7a4 4 0 0 0-4 4v1a2 2 0 0 0 2 2h2.172a2.999 2.999 0 0 1-.114-1.588l.674-3.372a3 3 0 0 1 .82-1.533L9.06 13Zm9.032-5a2.907 2.907 0 0 0-2.056.852L9.967 14.92a1 1 0 0 0-.273.51l-.675 3.373a1 1 0 0 0 1.177 1.177l3.372-.675a1 1 0 0 0 .511-.273l6.07-6.07a2.91 2.91 0 0 0-.944-4.742A2.907 2.907 0 0 0 18.092 8Z" 
            clip-rule="evenodd"/>
          </svg>
          Edit
        </a>
        <button
          data-user-id="${user.id}"
          type="button"
          data-modal-target="delete-user-modal"
          data-modal-toggle="delete-user-modal"
          class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-red-600 rounded-lg hover:bg-red-800 focus:ring-4 focus:ring-red-300 dark:focus:ring-red-900">
          <svg
            class="w-4 h-4 mr-2"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg">
            <path
              fill-rule="evenodd"
              d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
              clip-rule="evenodd"></path>
          </svg>
          Delete
        </button>
      </td>
        `;

    tableBody.appendChild(tableRow);
  });
}
