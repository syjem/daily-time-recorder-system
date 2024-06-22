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
