function learningPathController($scope, $http) {

    $scope.nextStudent = function nextStudent(index) {
        $('table > tbody > tr');
        window.location.href = "../" + index + "/";
    }
}
