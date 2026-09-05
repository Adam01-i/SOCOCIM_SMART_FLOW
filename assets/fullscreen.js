document.addEventListener("click", function (event) {
  const button = event.target.closest(".map-fullscreen-btn");
  if (!button) return;

  const frame = document.getElementById(button.dataset.target);
  if (!frame) return;

  if (document.fullscreenElement === frame) {
    document.exitFullscreen();
  } else if (frame.requestFullscreen) {
    frame.requestFullscreen();
  }
});

document.addEventListener("fullscreenchange", function () {
  document.querySelectorAll(".map-fullscreen-btn").forEach(function (button) {
    const frame = document.getElementById(button.dataset.target);
    const isFullscreen = frame && document.fullscreenElement === frame;
    button.textContent = isFullscreen ? button.dataset.exitLabel : button.dataset.enterLabel;
    button.title = button.textContent;
  });
});