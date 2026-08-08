// EDIT THIS: your own website, shown as the safe alternative destination
const HOME_SITE_URL = "http://localhost:3000/upload";
const HOME_SITE_LABEL = "Analyze the risk of the URL"; // shown on the button

const params = new URLSearchParams(window.location.search);
const target = params.get("target");
document.getElementById("targetUrl").textContent = target || "";

document.getElementById("back").addEventListener("click", () => {
  history.back();
});

document.getElementById("homeSite").addEventListener("click", () => {
  window.location.href = HOME_SITE_URL;
});
document.getElementById("homeSite").textContent = `${HOME_SITE_LABEL}`;

// 10 second countdown before "Proceed Anyway" becomes clickable
const proceedBtn = document.getElementById("proceed");
let secondsLeft = 10;

const countdown = setInterval(() => {
  secondsLeft -= 1;
  if (secondsLeft <= 0) {
    clearInterval(countdown);
    proceedBtn.disabled = false;
    proceedBtn.textContent = "Proceed Anyway";
  } else {
    proceedBtn.textContent = `Proceed Anyway (${secondsLeft})`;
  }
}, 1000);

proceedBtn.addEventListener("click", () => {
  if (target && !proceedBtn.disabled) {
    window.location.href = target;
  }
});
