// Logic
function loginPost() {
    
    let $id = $('#inputID').val();
    let $pw = $('#inputPW').val();

    $.ajax({
        type: "POST",
        url: "/api/login",
        data: {
            'input_id' : $id,
            'input_pw' : $pw
        },
        success: function(response) {
            if (response['result'] == 'failure') {
                let errorMsg = response['msg']
                makeAlert(errorMsg)
                return
            } else {
                $('#error-alert').empty()
                window.location.href = '/'
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });  
}

function makeAlert(errorMsg) {
    let alert = '<div class="alert alert-red alert-solid" role="alert">' + errorMsg + '</div>'
    $('#error-alert').empty()
    $('#error-alert').append(alert)
}
