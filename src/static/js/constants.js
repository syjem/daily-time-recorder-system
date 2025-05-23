export const loaderIcon = `
    <svg aria-hidden="true" role="status" class="w-4 h-4 text-white animate-spin mr-2 -ml-1" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
      <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
    </svg>
    `;

export const plusIcon = `
    <svg
      class="mr-1 -ml-1 w-6 h-6"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg">
      <path
        fill-rule="evenodd"
        d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
        clip-rule="evenodd"></path>
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

export const schedules = [
  {
    sunday: {
      id: 'sunday',
      name: 'Sun',
      type: 'checkbox',
      container: 'container-sunday',
    },
  },
  {
    monday: {
      id: 'monday',
      name: 'Mon',
      type: 'checkbox',
      container: 'container-monday',
    },
  },
  {
    tuesday: {
      id: 'tuesday',
      name: 'Tue',
      type: 'checkbox',
      container: 'container-tuesday',
    },
  },
  {
    wednesday: {
      id: 'wednesday',
      name: 'Wed',
      type: 'checkbox',
      container: 'container-wednesday',
    },
  },
  {
    thursday: {
      id: 'thursday',
      name: 'Thu',
      type: 'checkbox',
      container: 'container-thursday',
    },
  },
  {
    friday: {
      id: 'friday',
      name: 'Fri',
      type: 'checkbox',
      container: 'container-friday',
    },
  },
  {
    saturday: {
      id: 'saturday',
      name: 'Sat',
      type: 'checkbox',
      container: 'container-saturday',
    },
  },
];

export const shiftType = ['Opener', 'Regular', 'Closer'];
