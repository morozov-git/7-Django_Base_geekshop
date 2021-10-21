

    $('.product_list').on('click', 'button[class="btn btn-outline-success"]', function (){
        let but_href = event.target;
        // console.log(but_href);
        // console.log(but_href.name);

        $.ajax({
            url : '/baskets/baskets_add/' + but_href.name,
            success: function (data){
                $('.basket_icon').html(data.result_icon)
            },
        });
    })
