/* -------------------------------------------------------------
   Cute‑Planner : calendar.js
   -------------------------------------------------------------
   • expects `EVENTS` injected in <script> as
     [{start:"yyyy-mm-dd", title:"...", desc:"...", priority:"mid"}, ...]
   • requires #dates, #title, #prev, #next… elements already present
   ------------------------------------------------------------- */

/* ---------- helper constants & dom refs ---------- */
const DAYS      = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const titleEl   = document.getElementById("title");
const dayNames  = document.getElementById("day-names");
const datesBox  = document.getElementById("dates");
const prevBtn   = document.getElementById("prev");
const nextBtn   = document.getElementById("next");
const btnMonth  = document.getElementById("btn-month");
const btnWeek   = document.getElementById("btn-week");
const btnToday  = document.getElementById("btn-today");

/* modal refs */
const mWrap  = document.getElementById("eventsModal");
const mBack  = document.getElementById("eventsBD");
const mBox   = document.getElementById("eventsBox");
const mTitle = document.getElementById("eventsTitle");
const mBody  = document.getElementById("eventsBody");
const mClose = document.getElementById("eventsClose");

/* ---------- state ---------- */
let today   = new Date();                                    // live “today”
let current = new Date(today.getFullYear(), today.getMonth(), 1); // view month
let view    = "month";                                       // "month"|"week"

/* ---------- utility ---------- */
const iso = d => {
  const local = new Date(d.getTime() - d.getTimezoneOffset()*60_000);
  return local.toISOString().slice(0,10);
};

function clear(el){ while (el.firstChild) el.removeChild(el.firstChild); }
const fmtMY = d => d.toLocaleString("default",{month:"long",year:"numeric"});

/* ---------- build a single day cell ---------- */
function dayCell(jsDate, isBlank=false){
  const div = document.createElement("div");
  if (isBlank) return div;                                   // empty spacer

  div.textContent   = jsDate.getDate();
  div.className     = "day";
  div.dataset.date  = iso(jsDate);                           // store date
  if (iso(jsDate) === iso(today)) div.classList.add("today");
  return div;
}

/* ---------- dots indicating priority ---------- */
function addPriorityDots(){
  if (!Array.isArray(EVENTS)) return;

  const map = Object.fromEntries(EVENTS.map(e => [e.start, e.priority]));

  document.querySelectorAll("#dates .day").forEach(cell=>{
    const pr = map[cell.dataset.date];
    if(!pr) return;

    const dot = document.createElement("span");
    dot.className = `date-dot dot-${pr}`;                    // dot‑urgent …
    cell.style.position = "relative";
    cell.appendChild(dot);
  });
}

/* ---------- render ---------- */
function renderDayNames(){
  clear(dayNames);
  DAYS.forEach(d=>{
    const div = document.createElement("div");
    div.textContent = d;
    div.className = "day-name";
    dayNames.appendChild(div);
  });
}

function renderMonth(date){
  clear(datesBox);
  titleEl.textContent = fmtMY(date);

  const firstWeekday   = new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  const daysInMonth    = new Date(date.getFullYear(), date.getMonth()+1, 0).getDate();

  /* blanks from previous month */
  for(let i=0;i<firstWeekday;i++){
    const prev = new Date(date.getFullYear(),date.getMonth(),1-(firstWeekday-i));
    datesBox.appendChild(dayCell(prev,true));
  }
  /* actual month days */
  for(let d=1;d<=daysInMonth;d++){
    const real = new Date(date.getFullYear(),date.getMonth(),d);
    datesBox.appendChild(dayCell(real));
  }
  addPriorityDots();
}

function renderWeek(date){
  clear(datesBox);
  const start = new Date(date.getFullYear(),date.getMonth(),date.getDate()-date.getDay()); // Sun
  const end   = new Date(start.getFullYear(),start.getMonth(),start.getDate()+6);
  titleEl.textContent = `${start.toLocaleDateString()} – ${end.toLocaleDateString()}`;

  for(let i=0;i<7;i++){
    const d = new Date(start.getFullYear(),start.getMonth(),start.getDate()+i);
    datesBox.appendChild(dayCell(d));
  }
  addPriorityDots();
}

function render(){
  renderDayNames();
  view==="month" ? renderMonth(current) : renderWeek(current);
}

/* ---------- modal helpers ---------- */
function openEventsModal(){
  mWrap.classList.remove("hidden");
  mBack.classList.remove("modal-hide-bd");
  mBox.classList.remove("modal-hide");
  mBack.classList.add("modal-show-bd");
  mBox.classList.add("modal-show");
}
function closeEventsModal(){
  mBack.classList.remove("modal-show-bd");
  mBox.classList.remove("modal-show");
  mBack.classList.add("modal-hide-bd");
  mBox.classList.add("modal-hide");
  setTimeout(()=>mWrap.classList.add("hidden"),200);
}
mClose.addEventListener("click",closeEventsModal);
mBack .addEventListener("click",closeEventsModal);

/* ---------- nav buttons ---------- */
prevBtn.addEventListener("click",()=>{
  view==="month" ? current.setMonth(current.getMonth()-1)
                 : current.setDate(current.getDate()-7);
  render();
});
nextBtn.addEventListener("click",()=>{
  view==="month" ? current.setMonth(current.getMonth()+1)
                 : current.setDate(current.getDate()+7);
  render();
});
btnMonth.addEventListener("click",()=>{
  view="month"; btnMonth.classList.add("active"); btnWeek.classList.remove("active"); render();
});
btnWeek.addEventListener("click",()=>{
  view="week";  btnWeek.classList.add("active");  btnMonth.classList.remove("active"); render();
});
btnToday.addEventListener("click",()=>{
  today   = new Date();
  current = new Date(today.getFullYear(),today.getMonth(),1);
  view="month";
  btnMonth.classList.remove("active");
  btnWeek .classList.remove("active");
  render();
});

/* ---------- click on a day ---------- */
datesBox.addEventListener("click",e=>{
  const cell = e.target.closest(".day");
  if(!cell) return;

  const key   = cell.dataset.date;
  const matches = Array.isArray(EVENTS) ? EVENTS.filter(ev=>ev.start===key) : [];

  if(!matches.length){ closeEventsModal(); return; }

  /* fill modal */
  const d = new Date(key);
  mTitle.textContent = d.toLocaleDateString(undefined,
                    {weekday:"long",month:"short",day:"numeric",year:"numeric"});
  mBody.innerHTML = "";
  matches.forEach(ev=>{
    const c = document.createElement("div");
    c.className = "task-card p-4 bg-pink-50 rounded-lg";
    c.innerHTML = `
       <h4 class="font-semibold">${ev.title||"Untitled"}</h4>
       ${ev.desc ? `<p class="text-sm text-gray-600">${ev.desc}</p>` : ""}
       <p class="text-xs mt-2">
         <span class="font-medium">Priority:</span>
         <span class="${ev.priority==='urgent' ? 'text-red-600 glow' :
                       ev.priority==='mid'    ? 'text-yellow-500 glow' :
                                                'text-green-600 glow'}">
           ${ev.priority}
         </span>
       </p>`;
    mBody.appendChild(c);
  });
  openEventsModal();
});

/* ---------- initialise ---------- */
render();
