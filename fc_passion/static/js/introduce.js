// View Load
$(document).ready(function() {
    getMembers()
})

// Logic
function getMembers() {
    $.ajax({
        type: "GET",
        url: "/api/introduce/member",
        data: {
        },
        success: function(response) {
            if (response['result'] == 'success') {
                memberList = response['data']
                memberList.forEach( member => {
                    makeMemeberBox(member.name, member.phone)
                })
            } else {
                alert(response['data'])
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function emergencyInfo() {
    
    $('#member-box').empty();

    $.ajax({
        type: "GET",
        url: "/api/introduce/member-phone",
        data: {
        },
        success: function(response) {
            if (response['result'] == 'success') {
                memberList = response['data']
                memberList.forEach( member => {
                    makeMemeberBox(member.name, member.phone)
                })
            } else {
                if (response['redirect_url']) {
                    window.location.href = response['redirect_url']
                } else {
                    alert(response['msg'])
                }
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}

function makeMemeberBox(name, phone) {
    let memberTag;
    let image;

    if (name == "이현승") {
        console.log("이현승")
        image = "/static/images/hyunseung.png";
    } else {
        image = "/static/images/avatar.png";
    }

    if (phone == null) {
        memberTag = '<div class="col-lg-3 col-md-6 mb-5">\
                        <a class="card lift border-bottom-lg border-purple" href="#!">\
                            <div class="card-body text-center">\
                                <img src=' + '"' + image + '" ' + 'width="100px" height="100px"></img>\
                                <div class="text-gray-800 mt-3"><b>' + name + '</b></div>\
                            </div>\
                        </a>\
                    </div>'
    } else {
        memberTag = '<div class="col-lg-3 col-md-6 mb-5">\
                        <a class="card lift border-bottom-lg border-purple" href="#!">\
                            <div class="card-body text-center">\
                                <img src=' + '"' + image + '" ' + 'width="100px" height="100px"></img>\
                                <div class="text-gray-800 mt-3"><b>' + name + '</b></div>\
                                <div class="small text-gray-600 mt-1">' + phone + '</div>\
                            </div>\
                        </a>\
                    </div>'
    }
    
    $('#member-box').append(memberTag) 
}