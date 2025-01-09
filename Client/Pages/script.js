const moreOpt = document.querySelector(".moreOpt");
const dropdownNav = document.querySelector(".dropdownNav");

moreOpt.addEventListener("click", function (event) {
  event.stopPropagation();
  dropdownNav.classList.toggle("show"); // Toggle class
});

document.addEventListener("click", function () {
  dropdownNav.classList.remove("show"); // Hide when clicking outside
});
