window.onload = function () {
    $('.container-fluid').on('click', 'a[id="admins_content"]', function (){
            let elem = event.target;
            console.log(elem);
            console.log(elem.getAttribute('link'));
            let link = elem.getAttribute('link')
            if (!link){
               link = elem.parentNode.getAttribute('link')
            }
            console.log(link);
            $.ajax({
                url : link,
                success: function (data){
                $('body').html(data)
            },

        });

    })
}