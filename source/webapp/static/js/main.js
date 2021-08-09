

$(function(){
    // let stickyNavTop = $('.category-navbar').offset().top;
    // let stickyNav = function(){
    //     let scrollTop = $(window).scrollTop();
    //     if (scrollTop > stickyNavTop) {
    //         $('.category-navbar').addClass('sticky');
    //     } else {
    //         $('.category-navbar').removeClass('sticky');
    //     }
    // };
    // stickyNav();
    // $(window).scroll(function() {
    //     stickyNav();
    // });

    // $('.to-cart-btn').click(function(){
    //     $(this).closest('.card').find('img').clone()
    //         .css({'position' : 'absolute', 'z-index' : '1000'})
    //         .appendTo("body").animate({
    //         top: $(".cart").offset()['top'],
    //         left: $(".cart").offset()['left'],
    //         opacity: 0,
    //         width: 40
    //     },1500, function(){
    //         $(this).remove();
    //
    //     });
    // });



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getCookie('csrftoken');

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
        let url = $(this).attr('data-ajax-target');
        let count_1 = $(this).prev().find('.quantity');
        let img = $(this).closest('.card').find('img');
        let cart = $(".cart");
        let w = img.width();
        img.clone()
            .css({'width' : w,
                'position' : 'absolute',
                'z-index' : '9999',
                top: img.offset().top,
                left:img.offset().left})
            .appendTo("body")
            .animate({opacity: 0.05,
                left: cart.offset()['left'],
                top: cart.offset()['top'],
                width: 20}, 1000, function() {
                $(this).remove();
            });
        $.ajax({
            url: url,
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
                count_1.html('1');
                $('.count').html(data.products_count);
            }
        });
    });
});