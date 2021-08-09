

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

    // $( ".plus-quantity" ).click(function() {
    //     let countDiv = $(this).prev('div');
    //     let newCount = parseInt(countDiv.html()) + 1;
    //     countDiv.html(newCount);
    // });
    // $( ".minus-quantity" ).click(function() {
    //     let countDiv = $(this).next('div');
    //     if (parseInt(countDiv.html()) > 1) {
    //         let newCount = parseInt(countDiv.html()) - 1;
    //         countDiv.html(newCount);
    //     }
    // });
    $('.delete-from-cart').on('click', function() {
        let url = $(this).attr('data-ajax-target');
        let elem = $(this);
        let pk = $(this).attr('data');
        $.ajax({
            url: url,
            type: 'post',
            data: {
                pk: pk,
                action: 'remove'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                elem.closest('tr').remove();
                $('.cart-total').html(data.total);
                let delivery = $('.delivery-value').html();
                if (delivery === '---'){
                    $('.cart-total-delivery').html(data.total);
                }else {
                    let summ = parseInt(data.total)+parseInt(delivery);
                    $('.cart-total-delivery').html(summ);
                }
            }
        });
    });
    $('#id_shipping_district').on('change', function() {
        let cartTotal = parseInt($('.cart-total').html());
        let sum = parseInt($(this).val());
        $('.delivery-value').html(sum);
        $('.cart-total-delivery').html(cartTotal + sum);
    });
    $( ".plus-quantity-2" ).click(function() {
        let pk = $(this).attr('data');
        let url = $(this).attr('data-ajax-target');
        let countDiv = $(this).prev('div');
        let newCount = parseInt(countDiv.html()) + 1;
        $.ajax({
            url: url,
            type: 'post',
            data: {
                pk: pk,
                count: '1',
                action: 'add'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                countDiv.html(newCount);
                $( ".total-"+pk).html(data.product_summ);
                $('.cart-total').html(data.total);
                let delivery = $('.delivery-value').html();
                if (delivery === '---'){
                    $('.cart-total-delivery').html(data.total);
                }else {
                    let summ = parseInt(data.total)+parseInt(delivery);
                    $('.cart-total-delivery').html(summ);
                }
            }
        });

    });
    $( ".minus-quantity-2" ).click(function() {
        let elem = $(this);
        let pk = $(this).attr('data');
        let url = $(this).attr('data-ajax-target');
        let countDiv = $(this).next('div');
        let newCount = parseInt(countDiv.html()) - 1;
        $.ajax({
            url: url,
            type: 'post',
            data: {
                pk: pk,
                count: '1',
                action: 'minus'
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                if (newCount === 0){
                    elem.closest('tr').remove();
                }else {
                    countDiv.html(newCount);
                }
                $( ".total-"+pk).html(data.product_summ);
                $('.cart-total').html(data.total);
                let delivery = $('.delivery-value').html();
                if (delivery === '---'){
                    $('.cart-total-delivery').html(data.total);
                }else {
                    let summ = parseInt(data.total)+parseInt(delivery);
                    $('.cart-total-delivery').html(summ);
                }
            }
        });
    });
    // $('.to-cart-btn').on('click', function() {
    //     let pk = $(this).attr('data');
    //     let url = $(this).attr('data-ajax-target');
    //     let count_1 = $(this).prev().find('.quantity');
    //     $.ajax({
    //         url: url,
    //         type: 'post',
    //         data: {
    //             pk: pk,
    //             count: count_1.html(),
    //             action: 'add'
    //         },
    //         headers: {
    //             'X-CSRFToken': csrftoken
    //         },
    //         dataType: 'json',
    //         success: function (data) {
    //             $('.count').html(data.products_count);
    //         }
    //     });
    // });
});