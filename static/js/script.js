// $(document).on('click', '.delete-button', function (e) {
//     e.preventDefault();
//     var item_id = $(this).data('index');
//     $.ajax({
//         type: 'POST',
//         url: '{%url "orders:bag_delete"%}',
//         data: {
//             item: $(this).data('index'),
//             csrfmiddlewaretoken: "{{csrf_token}}",
//             action: 'post',
//         },
//         success: function (json) {
//             $('.item[data-index="' + item_id + '"]').remove();
//             if (json.quantity == 0) {
//                 subtotal = 0
//             }
//             else {
//                 subtotal = json.subtotal;
//             }
//             $('#subtotal').replaceWith = subtotal;
//             $('#bag-quantity').replaceWith("json.quantity");
//         }, error: function (xhr, errmsg, err) { },
//     });
// });

// $(document).on("click", ".update-button", function (e) {
//     e.preventDefault();
//     var item_id = $(this).data("index");
//     $.ajax({
//         type: 'POST',
//         url: '{%url "orders:bag_update"%}',
//         data: {
//             item: $(this).data("index"),
//             quantity: $('#select' + item_id + " option:selected").text(),
//             csrfmiddlewaretoken: "{{csrf_token}}",
//             action: "post"
//         },
//         success: function (json) {
//             subtotal = (parseFloat(json.subtotal)).toFixed(2);
//             $("#bag-quantity").replaceWith(json.quantity);
//             $("#subtotal").replaceWith(json.subtotal);
//         },
//         error: function (xhr, errmsg, err) { }
//     });
// });




// $(document).ready(function () {
//     $("#menu-button").on("click", function () {
//         $("#menu").toggle("fast")
//         $("#close").toggle("fast")
//         $("nav").toggleClass("translate-x-full -translate-y-full")
//     })
// })

// $(document).ready(function () {
//     // Fade out messages after 3 seconds
//     $(".fade-message").delay(3000).fadeOut(500);
// });



$(document).on("click", ".delete-button", function (e) {
    e.preventDefault();
    var item_id = $(this).data("index");

    $.ajax({
        type: "POST",
        url: "{% url 'orders:bag_delete' %}",
        data: {
            item: item_id,
            csrfmiddlewaretoken: "{{ csrf_token }}",
            action: "post",
        },
        success: function (json) {
            $('.item[data-index="' + item_id + '"]').remove();

            let subtotal = json.quantity === 0 ? 0 : json.subtotal;

            $("#subtotal").text("$" + subtotal.toFixed(2));
            $("#bag-quantity").text(json.quantity);
        },
        error: function (xhr, errmsg, err) {
            console.error("Error deleting item:", errmsg);
        },
    });
});

$(document).on("click", ".update-button", function (e) {
    e.preventDefault();
    var item_id = $(this).data("index");
    var quantity = $("#select" + item_id + " option:selected").text();

    $.ajax({
        type: "POST",
        url: "{% url 'orders:bag_update' %}",
        data: {
            item: item_id,
            quantity: quantity,
            csrfmiddlewaretoken: "{{ csrf_token }}",
            action: "post",
        },
        success: function (json) {
            let subtotal = parseFloat(json.subtotal).toFixed(2);

            $("#bag-quantity").text(json.quantity);
            $("#subtotal").text("$" + subtotal);
        },
        error: function (xhr, errmsg, err) {
            console.error("Error updating item:", errmsg);
        },
    });
});

$(document).ready(function () {
    $("#menu-button").on("click", function () {
        $("#menu").toggle("fast");
        $("#close").toggle("fast");
        $("nav").toggleClass("translate-x-full -translate-y-full");
    });

    // Fade out messages after 3 seconds
    $(".fade-message").delay(3000).fadeOut(500);
});

function showMessage(text) {
    const messageBox = $("#message-box");
    const messagesList = $(".messages");
    const newMessage = $("<li>")
        .addClass("message bg-gray-100 text-black text-lg px-4 py-2 rounded-md shadow-sm shadow-black/50")
        .text(text);

    messagesList.append(newMessage);
    messageBox.show();

    setTimeout(() => {
        newMessage.fadeOut(500, function () {
            $(this).remove();
        });
    }, 2000);
}