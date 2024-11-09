// ADMIN USERS TABLE: Populate the form input value with the User ID when on delete button click.

document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button[data-user-id]');
  const deleteUserForm = document.getElementById('delete-user-form');
  const userIdInput = deleteUserForm.querySelector('#user-id-input');

  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const userId = button.getAttribute('data-user-id');
      deleteUserForm.action = `/api/admin/user/${userId}/delete`;
      userIdInput.value = userId;
    });
  });
});
