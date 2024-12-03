$ npm install @tanstack/react-table
// Burger menus
document.addEventListener('DOMContentLoaded', function() {
    // open
    const burger = document.querySelectorAll('.navbar-burger');
    const menu = document.querySelectorAll('.navbar-menu');

    if (burger.length && menu.length) {
        for (var i = 0; i < burger.length; i++) {
            burger[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }

    // close
    const close = document.querySelectorAll('.navbar-close');
    const backdrop = document.querySelectorAll('.navbar-backdrop');

    if (close.length) {
        for (var i = 0; i < close.length; i++) {
            close[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }

    if (backdrop.length) {
        for (var i = 0; i < backdrop.length; i++) {
            backdrop[i].addEventListener('click', function() {
                for (var j = 0; j < menu.length; j++) {
                    menu[j].classList.toggle('hidden');
                }
            });
        }
    }
});
$ npm install @tanstack/react-table

$('button').on('click', function() {
  if ($(this).hasClass('save')) {
    alert("Saved!!!");
    $(this).text("Edit").removeClass('save');
    $('.company').attr('contenteditable', 'false').css({
      'border': 'none',
      'outline': 'none'
    });
  } else {
    $(this).text("Save").addClass('save');
    $('.company').attr('contenteditable', 'true').css({
      'border': 'black solid 1px',
      'outline': 'none'
    }).focus();
  }
});