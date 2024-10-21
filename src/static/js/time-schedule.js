import { schedules } from './constants.js';

const setBusinessDays = () => {
  const checkbox = document.getElementById('business-days');
  const monday = document.getElementById('monday');
  const tuesday = document.getElementById('tuesday');
  const wednesday = document.getElementById('wednesday');
  const thursday = document.getElementById('thursday');
  const friday = document.getElementById('friday');
  const saturday = document.getElementById('saturday');
  const sunday = document.getElementById('sunday');
  const startTimeSaturday = document.getElementById('start-time-saturday');
  const endTimeSaturday = document.getElementById('end-time-saturday');
  const startTimeSunday = document.getElementById('start-time-sunday');
  const endTimeSunday = document.getElementById('end-time-sunday');

  const containerSaturday = document.getElementById('container-saturday');
  const containerSunday = document.getElementById('container-sunday');

  const weekdays = [monday, tuesday, wednesday, thursday, friday];
  const toggleDisableElements = [
    saturday,
    startTimeSaturday,
    endTimeSaturday,
    sunday,
    startTimeSunday,
    endTimeSunday,
  ];

  checkbox.addEventListener('change', () => {
    if (checkbox.checked) {
      saturday.checked = false;
      sunday.checked = false;

      checkElements(weekdays);
      disableElements(toggleDisableElements);

      containerSaturday.style.opacity = '0.4';
      containerSunday.style.opacity = '0.4';
    } else {
      uncheckElements(weekdays);
      enableElements(toggleDisableElements);

      containerSaturday.style.opacity = '1';
      containerSunday.style.opacity = '1';
    }
  });

  const checkElements = (elements) => {
    elements.forEach((element) => {
      element.checked = true;
    });
  };

  const uncheckElements = (elements) => {
    elements.forEach((element) => {
      element.checked = false;
    });
  };

  const disableElements = (elements) => {
    elements.forEach((element) => {
      element.setAttribute('disabled', true);
    });
  };

  const enableElements = (elements) => {
    elements.forEach((element) => {
      element.removeAttribute('disabled', true);
    });
  };
};

setBusinessDays();

const submitForm = () => {
  const form = document.getElementById('form');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = [];

    schedules.forEach((item) => {
      const key = Object.keys(item)[0];
      const schedule = item[key];

      const checkbox = document.getElementById(schedule.id);
      const startTime = document.getElementById(
        `start-time-${schedule.id}`
      ).value;
      const endTime = document.getElementById(`end-time-${schedule.id}`).value;

      if (checkbox.checked) {
        formData.push({
          day: schedule.name,
          day_off: false,
          start_time: startTime,
          end_time: endTime,
        });
      } else {
        formData.push({
          day: schedule.name,
          day_off: true,
          start_time: null,
          end_time: null,
        });
      }
    });

    const response = await fetch('/sample', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    console.log(data);

    // console.log(JSON.parse(JSON.stringify(formData)));
  });
};

submitForm();
