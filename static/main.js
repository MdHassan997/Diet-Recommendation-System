// Active Navbar
let nav = document.querySelector(".navigation-wrap");
window.onscroll = function () {
    if(document.documentElement.scrollTop > 20){
        nav.classList.add("scroll-on");
    }else{
        nav.classList.remove("scroll-on");
    }
}

// Navbar Hide
let navBar = document.querySelectorAll('.nav-link');
let navCollapse = document.querySelector('.navbar-collapse.collapse');
navBar.forEach(function(a){
    a.addEventListener("click", function(){
        navCollapse.classList.remove("show");
    })
})


// Back to Top Button
document.addEventListener('DOMContentLoaded', function () {
    var backToTopButton = document.getElementById('back-to-top');

    backToTopButton.style.display = 'none';

    function toggleBackToTopButton() {
        if (window.scrollY > 160) { 
            backToTopButton.style.display = 'grid'; 
        } else {
            backToTopButton.style.display = 'none'; 
        }
    }
    toggleBackToTopButton();
    window.addEventListener('scroll', toggleBackToTopButton);
});