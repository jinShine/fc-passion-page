// View Load
$(document).ready(function() {
    getAllItems()
})

// Logic
function getAllItems() {
    $.ajax({
        type: "GET",
        url: "/api/index",
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                console.log('success')
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function realod() {
    window.location.reload();
}