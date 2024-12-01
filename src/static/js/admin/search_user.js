import updateTable from '../utils/updateTable.js';
import {
  updateTablePages,
  tablePaginate,
  setPrevNextButton,
} from '../utils/tablePagination.js';

document.addEventListener('DOMContentLoaded', () => {
  let searchTimeout;
  const searchInput = document.getElementById('users-search');

  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    const query = e.target.value;

    if (!query) {
      const currentUrl = window.location.pathname;
      history.pushState({}, '', currentUrl);
      window.location.reload(currentUrl);
    } else {
      const newUrl = `/admin/users?name=${encodeURIComponent(query)}`;
      history.pushState({ query }, '', newUrl);
    }

    // Debounce the search
    searchTimeout = setTimeout(async () => {
      const APIUrl = `/api/admin/users/search?name=${encodeURIComponent(
        query
      )}`;

      try {
        const response = await fetch(APIUrl, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (!response.ok) {
          console.error(data.error);
          return;
        }
        updateTable(data.users);
        updateTablePages(data.pagination.page, data.pagination.pages);
        tablePaginate(data.start_index, data.end_index, data.pagination.total);
        setPrevNextButton(
          data.pagination.has_prev,
          data.pagination.has_next,
          data.pagination.prev_num,
          data.pagination.next_num
        );
      } catch (error) {
        console.error(error);
      }
    }, 1500);
  });
});
