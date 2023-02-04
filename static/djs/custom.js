
function deleteproduct(product_id) {
  swal({
    title: "Are you sure?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {

        $.ajax({
          url: 'product_delete',
          type: 'GET',
          data: {
            'product_id': product_id
          },
          success: function (data) {
            location.href = ''
            console.log(data.value)
          }
        })

      } else {
        console.log(false)
      }
    });
}


function deletecoupon(coupon_id) {
  swal({
    title: "Are you sure?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {

        $.ajax({
          url: "{% url 'coupon_delete' coupon_id%}",
          type: 'GET',
          data: {
            'coupon_id': coupon_id
          },
          success: function (data) {
            location.href = ''
            console.log(data.value)
          }
        })

      } else {
        console.log(false)
      }
    });
}




function blockuser(productid) {
  swal({
    title: "Are you sure?",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {

        $.ajax({
          url: 'block',
          type: 'GET',
          data: {
            'productid': productid
          },
          success: function (data) {
            location.href = ''
            console.log(data.value)
          }
        })

      } else {
        console.log(false)
      }
    });
}
