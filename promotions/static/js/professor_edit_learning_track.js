function learningPathController($scope, $http) {

    $scope.nextStudent = function nextStudent(index) {
        var listElements = $('table > tbody > tr').children();
        var listSkills = [];
        for (i = 0; i < listElements.length; i++) {
            listSkills.push(listElements[i].innerText);
        }
        $http.post("/professor/lesson/update_learning_track/", {
            "list_skills": listSkills,
            "student_pk": context.studentPk
        }).success(function(data, status, headers, config) {
            window.location.href = "../" + index + "/";
        });
    }
}
