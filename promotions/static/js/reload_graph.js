function updateCount(last_student, student, lesson){
    $.ajax({ url: "/professor/lesson/" +lesson + "/getStat/" + student +"/" + "-1/"})
        .success(function(data) {
            var obj = JSON.parse(data);
            $('#last_name').text("Nom : " + obj.student.last_name);
            $('#first_name').text("Prénom : " + obj.student.first_name);
            $('#email').text("Email : " + obj.student.email);
            $('svg[graph=graph]').text(generateGraph(last_student, data));
            $('#breadcrumb').text(" Statistiques " + obj.student.first_name + " " + obj.student.last_name);
        })
}