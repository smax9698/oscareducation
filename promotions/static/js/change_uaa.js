$(document).ready(function(){

    $('li.uaaSelector').not('.active').click(function(){

        $(this).siblings('li').removeClass('active');
        $(this).addClass('active');

        var uaa = this.firstElementChild.getAttribute('uaa_name');
        var id = this.firstElementChild.getAttribute('id');
        $.post("update_uaa/",
            {uaa: uaa},
            function (data, status) {
                if (status === "success") {
                    refresh_graph(id);
                    $('#uaa_choice').text(uaa)
                }
            });
    });
});

function refresh_graph(uaa) {
    $(".graph-student").each(function() {
        $(this).empty();

        var username = $(this.getAttribute("id")).selector;
        var lesson = $(this.getAttribute("lesson")).selector;

        d3.request(encodeURI("/professor/lesson/" + lesson + "/getStat/" + username+ "/" + uaa))
            .get(function(data) {
                if (data === null) {
                    console.log("no data");
                } else {
                    var dic = data.response;
                    generateGraph(username, dic);
                }
        });

    });
}