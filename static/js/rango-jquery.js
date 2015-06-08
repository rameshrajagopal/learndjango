$(document).ready(function() {
    $('#about-btn').addClass('btn btn-primary');
    $('#about-btn').click( function(event) {
     msg_str =  $('#msg').html()
     msg_str = msg_str + 'o'
     $('#msg').html(msg_str)
        });
    $("p").hover( function() {
        $(this).css('color', 'red');
        },
        function() {
        $(this).css('color', 'blue');
        });
});
