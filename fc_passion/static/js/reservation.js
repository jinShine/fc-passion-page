function reserveGround() {

    let $ground = $('#selected-ground').val()

    $.ajax({
        type: "GET",
        url: "/reservation/ground?ground="+$ground,
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                console.log(response['data'])
            } else {
                alert("데이터 가져오기 실패! 관리자에게 문의 바랍니다.")
            }
        },
        error: function(request, status, error) {
            console.log(error)
        }
    });
}