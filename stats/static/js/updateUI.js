$('#select_timespan').change(function () {

    var newVal = $('#select_timespan option:selected').val().split("-");
    $('#timespan').children('#startDate').val(newVal[0]);
    $('#timespan').children('#endDate').val(newVal[1]);
});

$('#menu-toggle').click(function (e) {
    e.preventDefault();
    $('#wrapper').toggleClass('toggled');
});