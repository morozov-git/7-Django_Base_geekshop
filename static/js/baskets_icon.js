window.onload = function () {
    $('.row').on('click', 'a[class="btn btn-outline-success"]', function (){
        let t_href = event.target;
        console.log(t_href);
        console.log(t_href.value);

        // $.ajax({
        //     url : '/baskets_add/' + t_href.name,
        //     success: function (data){
        //         $('.basket_icon').html(data.result_icon)
        //     },
        //
        // });
    // Event.preventDefault();
    })

}