function updateCount(last_student, student, lesson, selected_uaa){
    $.ajax({ url: "/professor/lesson/" +lesson + "/getStat/" + student +"/" + selected_uaa.toString() + "/"})
        .success(function(data) {
            var obj = JSON.parse(data);
            $('#last_name').text("Nom : " + obj.student.last_name);
            $('#first_name').text("Prénom : " + obj.student.first_name);
            $('#email').text("Email : " + obj.student.email);

            $('svg[graph=graph]').empty();
            console.log(data);
            $('svg[graph=graph]').text(generateGraph(last_student, data));
            $('#breadcrumb').text(" Statistiques " + obj.student.first_name + " " + obj.student.last_name);
        })
}

$(document).ready(function(){
    $('li.stud').click(function() {
        $(this).siblings('li').removeClass('active');
        $(this).addClass('active');

        var placeholder = $('svg.graph-student').get(0).getAttribute('id');
        var student = this.firstElementChild.getAttribute('student');
        var lesson = this.firstElementChild.getAttribute('lesson');
        var uaa = -1;

        var uaaSelector = $('li.uaaSelector.active');

        if(uaaSelector.length !== 0){
            uaa = uaaSelector.get(0).firstElementChild.getAttribute('uaa');
        }

        updateCount(placeholder,student, lesson, uaa)

    });

    $('li.uaaSelector').click(function(){
        $(this).siblings('li').removeClass('active');
        $(this).addClass('active');


        var currentStudentSelector = $('li.stud.active');

        var placeHolder = $('svg.graph-student').get(0).getAttribute('id');
        var student = null;
        var lesson  = null;
        var uaa = this.firstElementChild.getAttribute('uaa');

        if (currentStudentSelector.length === 1) {
            student = currentStudentSelector.get(0).firstElementChild.getAttribute('student');
            lesson = currentStudentSelector.get(0).firstElementChild.getAttribute('lesson');
        }

        console.log(uaa);
        updateCount(placeHolder, student, lesson, uaa);

    });

});