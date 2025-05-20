/* global page‑loader */
(() => {
  const loader = document.getElementById('pageLoader');
  let active = 0;                       // how many async ops underway

  function show() { active++; loader.classList.add('show'); }
  function hide() { if(--active <= 0){ active = 0; loader.classList.remove('show'); } }

  /* wrap native fetch */
  const _fetch = window.fetch;
  window.fetch = (...args) => {
    show();
    return _fetch(...args).finally(hide);
  };

  /* support axios if present */
  if (window.axios) {
    axios.interceptors.request.use(c => { show(); return c; },
                                   e => { hide(); return Promise.reject(e); });
    axios.interceptors.response.use(r => { hide(); return r; },
                                    e => { hide(); return Promise.reject(e); });
  }

  /* expose manual hooks (optional) */
  window.startLoader = show;
  window.stopLoader  = hide;
})();