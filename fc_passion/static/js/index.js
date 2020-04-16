// View Load
$(document).ready(function() {
    getAllItems()
})

// Logic
function getAllItems() {
    $.ajax({
        type: "GET",
        url: "/main",
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                console.log('성공해라!!!!!!!')
            }
        },
        error: function(request, status, error) {
            console.log("에러인가??")
        }
    });
}

function realod() {
    window.location.reload();
}