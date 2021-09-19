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

}