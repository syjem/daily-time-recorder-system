import { deleteUserHandler } from '../fetch/delete_user_handler.js';

document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('button[data-user-id]');
  const form = document.getElementById('delete-user-form');

  let user_id;

  deleteButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const userId = button.getAttribute('data-user-id');
      if (userId) {
        user_id = userId;
      }
    });
  });

  form.addEventListener('submit', (event) => deleteUserHandler(event, user_id));
});
