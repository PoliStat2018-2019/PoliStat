$(function() {
    $('a.scroll-btn').on('click', function(e) {
      e.preventDefault();
      $('html, body').animate({
          scrollTop: $($(this).attr('href')).offset().top}, 600, 'swing');
    });
});