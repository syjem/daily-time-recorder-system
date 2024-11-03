import { schedules } from './constants.js';
import { redirect } from './helpers.js';
import { renderToast } from './toast.js';

const submitForm = () => {
  const form = document.getElementById('form');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = [];

      schedules.forEach((item) => {
        const key = Object.keys(item)[0];
        const schedule = item[key];

        const checkbox = document.getElementById(schedule.id);
        const selectedRadio = document.querySelector(
          `input[name=${schedule.id}]:checked`
        );
        const shiftType = selectedRadio ? selectedRadio.value : null;

        if (checkbox.checked) {
          formData.push({
            day: schedule.name,
            day_off: false,
            shift_type: shiftType,
          });
        } else {
          formData.push({
            day: schedule.name,
            day_off: true,
            shift_type: null,
          });
        }
      });

      try {
        const response = await fetch('/api/sample', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        const data = await response.json();
        redirect(data.redirect);
      } catch (error) {
        renderToast(error.message, true);
      }
    });
  }
};

const enableCheckboxOnCheck = () => {
  schedules.forEach((item) => {
    const key = Object.keys(item)[0];
    const schedule = item[key];

    const checkbox = document.getElementById(schedule.id);
    const ul = document.querySelector(
      `#${schedule.container} ul[data-lists="radio"]`
    );
    const radioInputs = document.querySelectorAll(
      `#${schedule.container} .schedule-radio`
    );

    if (checkbox) {
      checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
          ul.classList.remove('opacity-[0.5]');
          radioInputs.forEach((radio) => {
            radio.disabled = false;
          });
        } else {
          ul.classList.add('opacity-[0.5]');
          radioInputs.forEach((radio) => {
            radio.disabled = true;
          });
        }
      });
    }
  });
};

submitForm();
enableCheckboxOnCheck();
