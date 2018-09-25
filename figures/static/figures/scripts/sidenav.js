var mobile_button = document.getElementById('sidenav-mobile-btn');
var sidenav = document.getElementById('sidenav-mobile-target');
var maint = document.getElementById('main');

function showNavOnMobile() {
    sidenav.classList.add("show-nav");
    main.classList.add("darken-main");
}

function hideNavOnMobile() {
    sidenav.classList.remove("show-nav");
    main.classList.remove("darken-main");
}

mobile_button.addEventListener("click", showNavOnMobile);
main.addEventListener("click", hideNavOnMobile);
window.addEventListener("resize", hideNavOnMobile);