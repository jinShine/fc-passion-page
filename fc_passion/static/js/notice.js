// View Load
$(document).ready(function() {
    noticeAllItems()
})

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
                window.location.href = '/notice'
            } else {

            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function noticeAllItems() {
    $.ajax({
        type: "GET",
        url: "/notice/list",
        data: {},
        success: function(response) {
            let items = response['data']
            items.forEach(item => {
                makeNoticeBox(item.title, item.content, item.name, item.date)
            })
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}


function makeNoticeBox(title, content, name, date) {
    let notice_html = '<div class="col-xl-4 col-lg-0 col-md-6 mb-5">\
                        <a class="card post-preview lift h-100" href="#!">\
                            <div class="card-body body-ellipsis mb-2">\
                                <h5 class="card-title">' + title + '</h5>\
                                <p class="card-text">' + content + '</p>\
                            </div>\
                            <div class="card-footer">\
                                <div class="post-preview-meta">\
                                    <div class="post-preview-meta-details">\
                                        <div class="post-preview-meta-details-name">' + name + '</div>\
                                        <div class="post-preview-meta-details-date">' + date + '</div>\
                                    </div>\
                                </div>\
                            </div>\
                        </a>\
                    </div>';

    $('#notice-box').append(notice_html)
}