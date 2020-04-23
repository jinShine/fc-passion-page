// View Load
$(document).ready(function() {
})

// Logic
function mathSchedulePost() {   
    let $title = $('#math-area-title').val();
    let $date = $('#match-date').val();
    let $time = $('#match-time').val();
    let $description = $('#match-description').val();

    if ($title == "") {
        alert('장소를 입력해주세요.')
        return
    }

    if (($date.match(/-/g) || []).length != 2 || checkSpace($date)) {
        alert('날짜형식을 맞춰주세요.')
        return
    }

    if (($time.match(/-/g) || []).length != 1 || ($time.match(/:/g) || []).length != 2 || checkSpace($time)) {
        alert('시간형식을 맞춰주세요.')
        return
    }

    $.ajax({
        type: "POST",
        url: "/schedule/write",
        data: {
            'title': $title,
            'description': $description,
            'date': $date,
            'time': $time
        },
        success: function(response) {
            if (response['result'] == 'success') {
                window.location.href = '/schedule/list'
            } else {
                alert('DB에러, 관리자에 문의 바랍니다.')
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function checkSpace(str) { 
    if(str.search(/\s/) != -1) { return true; }
    else { return false; } }