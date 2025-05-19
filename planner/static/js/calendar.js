// static/js/calendar.js

(function () {
  const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // DOM refs
  const titleEl = document.getElementById("title");
  const dayNamesEl = document.getElementById("day-names");
  const datesEl = document.getElementById("dates");
  const prevBtn = document.getElementById("prev");
  const nextBtn = document.getElementById("next");
  const btnMonth = document.getElementById("btn-month");
  const btnWeek = document.getElementById("btn-week");
  const btnToday = document.getElementById("btn-today");


  // state
  let today = new Date();
  let current = new Date(today.getFullYear(), today.getMonth(), 1);
  let view = "month"; // or "week"

  // helpers
  function formatMonthYear(date) {
    return date.toLocaleString("default", {
      month: "long",
      year: "numeric",
    });
  }

  function clear(el) {
    while (el.firstChild) el.removeChild(el.firstChild);
  }

  // render day names once
  function renderDayNames() {
    clear(dayNamesEl);
    DAYS.forEach((d) => {
      const div = document.createElement("div");
      div.textContent = d;
      div.className = "day-name";
      dayNamesEl.appendChild(div);
    });
  }

  // render month grid
  function renderMonth(date) {
    clear(datesEl);
    titleEl.textContent = formatMonthYear(date);

    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
    const daysInMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    // leading blanks
    for (let i = 0; i < firstDay; i++) {
      datesEl.appendChild(document.createElement("div"));
    }

    for (let d = 1; d <= daysInMonth; d++) {
      const div = document.createElement("div");
      div.textContent = d;
      div.className = "day";
      // today highlight
      if (
        d === today.getDate() &&
        date.getMonth() === today.getMonth() &&
        date.getFullYear() === today.getFullYear()
      ) {
        div.classList.add("today");
      }
      datesEl.appendChild(div);
    }
  }

  // render week view (shows current week of current state date)
  function renderWeek(date) {
    clear(datesEl);
    // find Sunday of the week
    const start = new Date(date);
    start.setDate(date.getDate() - date.getDay());
    titleEl.textContent = `${start.toLocaleDateString()} – ${new Date(
      start.getFullYear(),
      start.getMonth(),
      start.getDate() + 6
    ).toLocaleDateString()}`;

    for (let i = 0; i < 7; i++) {
      const curr = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
      const div = document.createElement("div");
      div.textContent = curr.getDate();
      div.className = "day";
      if (
        curr.toDateString() === today.toDateString()
      ) {
        div.classList.add("today");
      }
      datesEl.appendChild(div);
    }
  }

  function render() {
    renderDayNames();
    if (view === "month") {
      renderMonth(current);
    } else {
      renderWeek(current);
    }
  }

  // event listeners
  prevBtn.addEventListener("click", () => {
    if (view === "month") {
      current.setMonth(current.getMonth() - 1);
    } else {
      current.setDate(current.getDate() - 7);
    }
    render();
  });

  nextBtn.addEventListener("click", () => {
    if (view === "month") {
      current.setMonth(current.getMonth() + 1);
    } else {
      current.setDate(current.getDate() + 7);
    }
    render();
  });

  btnMonth.addEventListener("click", () => {
    view = "month";
    btnMonth.classList.add("active");
    btnWeek.classList.remove("active");
    render();
  });

  btnWeek.addEventListener("click", () => {
    view = "week";
    btnWeek.classList.add("active");
    btnMonth.classList.remove("active");
    render();
  });

  btnToday.addEventListener("click", () => {
  // refresh the "today" reference
  today = new Date();

  // jump to the first day of the current month
  current = new Date(today.getFullYear(), today.getMonth(), 1);

  view = "month";
  btnMonth.classList.remove("active");
  btnWeek.classList.remove("active");

  render();
  });

  // initial render
  render();
})();
