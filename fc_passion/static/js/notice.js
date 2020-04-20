// View Load
$(document).ready(function() {
})

// Logic
function noticePost() {
    
    let $title = $('#notice-title').val();
    let $content = $('#notice-content').val();

    $.ajax({
        type: "POST",
        url: "/api/notice/write",
        data: {
            'input_title' : $title,
            'input_content' : $content
        },
        success: function(response) {
            if (response['result'] == 'success') {
                window.location.href = '/notice/list'
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function searchQuery() {

    let $option = $('#selected-title').val()
    let $query = $('#input-query').val()

    $.ajax({
        type: "GET",
        url: "/api/notice/search?option="+$option+"&query="+$query,
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                window.location.href = '/notice/search?option='+$option+'&query='+$query
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function selectDropDown() {
    let $selectedTitle = $('#selected-title')
    let $selectedContent = $('#selected-content')
    
    if ($selectedTitle.text() == '제목') {
        if ($selectedContent.text() == '본문') {
            $selectedContent.click(function() {
                $selectedTitle.val('content')
                $selectedTitle.text('본문')
                $selectedContent.text('제목');
            })
        }
        
    } else {
        if ($selectedContent.text() == '제목') {
            $selectedContent.click(function() {
                $selectedTitle.val('title')
                $selectedTitle.text('제목');
                $selectedContent.text('본문');
            });
        }
    }
}