// View Load
$(document).ready(function() {
    $('#date-box').hide()
    $('#loader').hide()
})

function reserveGround() {

    $('#loader').show();

    let $ground = $('#selected-ground').val()

    $.ajax({
        type: "POST",
        url: "/reservation",
        data: {
            'ground_name': $ground
        },
        success: function(response) {
            console.log("제발", response)
            if (response['result'] == 'success') {
                $('#date-box').show()
                
                selectedChange()

                dates = response['data']
                dates.forEach( date => {
                    makeDatesItem(date)
                })

                $('#loader').hide();
            } else {
                alert(response['msg'])
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function selectedChange() {
    
    $("#drop-items").change(function () {

        $('#loader').show();
        $('#reservation-date-box').empty()
        
        $.ajax({
            type: "POST",
            url: "/reservation/date",
            data: {
                'date': $(this).val()
            },
            success: function(response) {
                console.log("제발", response)
                if (response['result'] == 'success') {
                    
                    dates = response['data']
                    dates.forEach( date => {
                        makeReservationDateItem(date)
                    })
                    $('#loader').hide();
                }
            },
            error: function(request, status, error) {
                console.log(error)
            }
        });
    });    
}

function makeDatesItem(date) {
    let dateItems = '<option>' + date + '</option>'
    $('#drop-items').append(dateItems) 
}

function makeReservationDateItem(date) {
    let dateItems = ''
    
    if (date.split(',')[1] == "예약 불가") {
        dateItems = '<li>' + date + '</li>'
    } else {
        // 예약 가능
        dateItems = '<li><a href="/reservation/' + date.split(',')[0] + '">' + date + '</a></li>'
    }

    $('#reservation-date-box').append(dateItems)
}