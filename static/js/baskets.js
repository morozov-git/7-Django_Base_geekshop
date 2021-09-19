window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function (){
        let t_href = event.target;
        // console.log(t_href);
        // console.log(t_href.value);

        $.ajax({
            url : '/baskets/edit/' + t_href.name + '/' + t_href.value,
            success: function (data){
                $('.basket_list').html(data.result)
                $('.basket_icon').html(data.result_icon)
            },

        });
    // Event.preventDefault();
    })

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

}