function learningPathController($scope, $http) {

    $scope.toggleSelection = function toggleSelection(learningTrack) {
        $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Toogle</div>');
    };

    update_test_list = function () {
        $http.get("/professor/lesson/edit_track/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.learningTrack = [];
           })
    };

    update_test_list();
}
