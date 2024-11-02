import { schedules } from './constants.js';

const container = document.getElementById('form');

schedules.forEach((item) => {
  const key = Object.keys(item)[0];
  const schedule = item[key];

  const scheduleHTML = `
        <div class="mb-5" id="${schedule.container}">
            <div class="flex items-center justify-between gap-3">
                <div class="flex items-center min-w-[4rem]">
                    <input
                        id="${schedule.id}"
                        name="${schedule.name}"
                        type="${schedule.type}"
                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
                    <label
                        for="${schedule.id}"
                        class="ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                        >${schedule.name}</label
                    >
                </div>

                <ul data-lists="radio" class="items-center w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg sm:flex dark:bg-gray-700 dark:border-gray-600 dark:text-white opacity-[0.5]">
                    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
                        <div class="flex items-center ps-3">
                            <input disabled id="${schedule.id}_opener" type="radio" value="Opener" name="${schedule.id}" class="schedule-radio w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                            <label for="${schedule.id}_opener" class="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Opener</label>
                        </div>
                    </li>
                    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
                        <div class="flex items-center ps-3">
                            <input disabled id="${schedule.id}_regular" type="radio" value="Regular" name="${schedule.id}" class="schedule-radio w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                            <label for="${schedule.id}_regular" class="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Regular</label>
                        </div>
                    </li>
                    <li class="w-full border-b border-gray-200 sm:border-b-0 sm:border-r dark:border-gray-600">
                        <div class="flex items-center ps-3">
                            <input disabled id="${schedule.id}_closer" type="radio" value="Closer" name="${schedule.id}" class="schedule-radio w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                            <label for="${schedule.id}_closer" class="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300">Closer</label>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    `;

  // Insert HTML into container
  container.innerHTML += scheduleHTML;
});
