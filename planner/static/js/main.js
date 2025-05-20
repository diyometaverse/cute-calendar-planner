// demo: show loader for 2 s after every page load
document.addEventListener('DOMContentLoaded', () => {
  startLoader();
  setTimeout(stopLoader, 500);
});