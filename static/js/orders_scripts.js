window.onload = function () {
    let _quantity, _price, _product_total_price, _orderitemnum, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = []
    let price_arr = []
    let product_total_price_arr = []
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    console.log(total_forms)

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;
    let product_total_price

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'));
        //*****//
        _product_total_price = parseInt($('.orderitems-' + i + '-product_total_price').text().replace(',', '.'));
        //*****//


        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0
        }

        //*****//
        if (_product_total_price) {
            product_total_price_arr[i] = _product_total_price;
        } else {
            product_total_price_arr[i] = 0
        }
        //*****//
    }
    console.info('price:', price_arr);
    //*****//
    console.info('product_total_price:', product_total_price_arr);
    //*****//
    console.info('quantity:', quantity_arr);


    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummeryUpdate(price_arr[orderitem_num], delta_quantity, orderitem_num)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummeryUpdate(price_arr[orderitem_num], delta_quantity, orderitem_num)

    });


    function orderSummeryUpdate(orderitem_price, delta_quantity, orderitem_num) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = order_total_price + delta_cost;
        order_total_quantity = order_total_quantity + delta_quantity;
        _product_total_price = parseInt($('.orderitems-' + orderitem_num + '-product_total_price').text().replace(',', '.'));
        let product_total_price = _product_total_price + delta_cost

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(order_total_price.toString() + ',00');
        $('.orderitems-' + orderitem_num + '-product_total_price').html(product_total_price.toString() + ',00');
    }


    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });
    function deleteOrderItem(row){
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-','').replace('-quantity',''));
        delta_quantity = -quantity_arr[orderitem_num]
        orderSummeryUpdate(price_arr[orderitem_num], delta_quantity, orderitem_num)
    }

}