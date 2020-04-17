// View Load
// $(document).ready(function() {
//     noticeAllItems()
// })

// Logic
function noticePost() {
    
    let $title = $('#notice-title').val();
    let $content = $('#notice-content').val();

    $.ajax({
        type: "POST",
        url: "/notice/write",
        data: {
            'input_title' : $title,
            'input_content' : $content
        },
        success: function(response) {
            if (response['result'] == 'success') {
                window.location.href = '/notice/list'
            } else {

            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

// function noticeAllItems() {
//     $.ajax({
//         type: "GET",
//         url: "/notice/list",
//         data: {
//             'input_title' : $title,
//             'input_content' : $content
//         },
//         success: function(response) {
//             if (response['result'] == 'success') {
//                 window.location.href = '/notice/list'
//             } else {

//             }
//         },
//         error: function(request, status, error) {
//             console.log(error)
//         }
//     });
// }
