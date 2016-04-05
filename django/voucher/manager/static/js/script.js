$(document).ready(function() {

  $('#submitimplicit').on('click', function(event) {
    event.preventDefault();

    $.post('/addLog/', {
      'date': $('#dateinput').val(),
      'theme': $('#themeinput').val(),
      'notes': $('#notesinput').val(),
      'is_implicit': 'true'
    }, function(r) {
      console.log(r);
    });
  });

});
