

$(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $( ".plus-quantity" ).click(function() {
        let countDiv = $(this).prev('div');
        let newCount = parseInt(countDiv.html()) + 1;
        countDiv.html(newCount);
    });
    $( ".minus-quantity" ).click(function() {
        let countDiv = $(this).next('div');
        if (parseInt(countDiv.html()) > 1) {
            let newCount = parseInt(countDiv.html()) - 1;
            countDiv.html(newCount);
        }
    });
    $('.to-cart-btn').on('click', function() {
        let pk = $(this).attr('data');
        let count_1 = $(this).prev().find('.quantity');
        $.ajax({
            url: 'http://localhost:8000/cart/change/',
            type: 'post',
            data: {
                pk: pk,
                count: count_1.html(),
                action: 'add'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                $('.count').html(data.products_count);
                console.info(data);
            }
        });
    });
});