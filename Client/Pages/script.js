const moreOpt = document.getElementById("moreOpt");
const dropdownNav = document.querySelector(".dropdownNav");  // Use the class selector with dot

/* moreOpt.addEventListener("click", function(){
    dropdownNav.style.opacity = "1";
    dropdownNav.style.visibility = "visible";
})*/

moreOpt.addEventListener("click", function (event) {
    event.stopPropagation(); // Prevent event bubbling
    dropdownNav.style.opacity = "1";
    dropdownNav.style.visibility = "visible";
});

// Optional: Hide dropdown when clicking outside
document.addEventListener("click", function () {
    dropdownNav.style.opacity = "0";
    dropdownNav.style.visibility = "hidden";
});
