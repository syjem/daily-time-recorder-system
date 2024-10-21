import { schedules } from './constants.js';

const container = document.getElementById('form');

schedules.forEach((item) => {
  const key = Object.keys(item)[0];
  const schedule = item[key];

  const scheduleHTML = `
        <div class="mb-5" id="${schedule.container}">
            <div class="flex items-center justify-between gap-3 sm:gap-5">
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

                <div class="w-full max-w-[7.5rem]">
                    <label for="start-time-${schedule.id}" class="sr-only">Start time:</label>
                    <div class="relative">
                        <input
                            type="time"
                            id="start-time-${schedule.id}"
                            name="start-time-${schedule.id}"
                            class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            value="00:00"
                            required />
                    </div>
                </div>
                <div class="w-full max-w-[7.5rem]">
                    <label for="end-time-${schedule.id}" class="sr-only">End time:</label>
                    <div class="relative">
                        <input
                            type="time"
                            id="end-time-${schedule.id}"
                            name="end-time-${schedule.id}"
                            class="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            value="00:00"
                            required />
                    </div>
                </div>
            </div>
        </div>
    `;

  // Insert HTML into container
  container.innerHTML += scheduleHTML;
});
