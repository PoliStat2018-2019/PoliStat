$(function() {
    var mobile_button = document.getElementById('sidenav-mobile-btn');
    var sidenav = document.getElementById('sidenav-mobile-target');
    var main = document.getElementById('main');
    var footer = document.getElementById('footer');

    function showNavOnMobile() {
        sidenav.classList.add("show-nav");
        main.classList.add("darken-on-navbar");
        footer.classList.add("darken-on-navbar");
    }
    
    function hideNavOnMobile() {
        sidenav.classList.remove("show-nav");
        main.classList.remove("darken-on-navbar");
        footer.classList.remove("darken-on-navbar");
    }

    mobile_button.addEventListener("click", showNavOnMobile);
    main.addEventListener("click", hideNavOnMobile);
    window.addEventListener("resize", hideNavOnMobile);
    window.addEventListener("scroll", hideNavOnMobile);
});