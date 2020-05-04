// auto link check
$(document).ready(function() {
    autolink("notice-content-body")
});

// Logic

function autolink(id) {
    var container = document.getElementById(id);
    var doc = container.innerHTML;
    var regURL = new RegExp("(http|https|ftp|telnet|news|irc)://([-/.a-zA-Z0-9_~#%$?&=:200-377()]+)","gi");
    var regEmail = new RegExp("([xA1-xFEa-z0-9_-]+@[xA1-xFEa-z0-9-]+\.[a-z0-9-]+)","gi");
    container.innerHTML = doc.replace(regURL,"<a href='$1://$2' target='_blank'>$1://$2</a>").replace(regEmail,"<a href='mailto:$1'>$1</a>");
}

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