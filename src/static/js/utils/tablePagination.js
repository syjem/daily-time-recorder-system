export const updateTablePages = (page, pages) => {
  const tablePage = document.getElementById('table-page');

  if (pages === 0) {
    tablePage.innerHTML = '';
    return;
  }

  tablePage.innerHTML = `
    <span class="font-semibold text-gray-900 dark:text-white">
       Page ${page} of ${pages}
    </span>
  `;
};

export const tablePaginate = (start, end, total) => {
  const tablePaginationDetails = document.getElementById(
    'table-users-paginate'
  );

  if (total === 0) {
    tablePaginationDetails.innerHTML = '';
    return;
  }

  tablePaginationDetails.innerHTML = `
    <span class="font-semibold text-gray-900 dark:text-white">
        Showing ${end === 0 ? 0 : start} - ${end}
    </span>
    <span class="font-semibold text-gray-900 dark:text-white">
        of ${total} users
    </span>
  `;
};

export const setPrevNextButton = (has_prev, has_next, prev_num, next_num) => {
  const prevButton = document.getElementById('prev-button');
  const nextButton = document.getElementById('next-button');
  const url = '/admin/users';

  // Enable/disable the Previous button based on has_prev
  if (has_prev) {
    prevButton.removeAttribute('disabled'); // Enable button if previous exists
    if (prev_num) {
      prevButton.setAttribute(
        'onclick',
        `window.location.href='${url}?page=${prev_num}'` // Correct URL with quotes
      );
    }
  } else {
    prevButton.setAttribute('disabled', true); // Disable button if no previous
    prevButton.removeAttribute('onclick'); // Ensure no invalid onclick is left
  }

  // Enable/disable the Next button based on has_next
  if (has_next) {
    nextButton.removeAttribute('disabled'); // Enable button if next exists
    if (next_num) {
      nextButton.setAttribute(
        'onclick',
        `window.location.href='${url}?page=${next_num}'` // Correct URL with quotes
      );
    }
  } else {
    nextButton.setAttribute('disabled', true); // Disable button if no next
    nextButton.removeAttribute('onclick'); // Ensure no invalid onclick is left
  }
};
