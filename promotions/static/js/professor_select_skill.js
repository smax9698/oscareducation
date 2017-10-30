function selectSkillController($scope, $http) {
    $scope.stages = [];

    // $scope.addNewTest = function() {
    //     if ($scope.name === undefined || $scope.name.length == 0)
    //     {
    //         $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Vous devez donner un nom à votre test.</div>');
    //         return;
    //     }
    //
    //     if ($scope.toTargetSkills.length == 0) {
    //         $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Vous devez sélectionner des compétences pour votre test.</div>');
    //         return;
    //     }
    //
    //     $http.post("/professor/add_test_from_class_for_lesson/", {
    //         "name": $scope.name,
    //         "lesson": context.lessonId,
    //         "skills": $scope.toTargetSkills,
    //     }).success(function(data, status, headers, config) {
    //         // TODO: don't do that in javascript
    //         window.location.href = "../" + data + "/fill/"
    //     })
    // }

    $scope.addSkillToTargets = function(stage_id) {
        if ($scope.stages[stage_id].length == 0)
            return;

        if ($scope.toTargetSkills.length >= 3)
        {
            $("#alerts").html('<div class="alert alert-warning alert-dismissible"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Vous ne pouvez sélectionner que trois compétences cibles au maximum.</div>');
            return;
        }

        var skill = $scope["stage" + stage_id + "SelectedSkill"];
        $scope.toTargetSkills.push(skill);

        var toRemoveIndex;

        for (var index = 0; index < $scope.stages[stage_id].length; index++) {
            if ($scope.stages[stage_id][index].code == $scope["stage" + stage_id + "SelectedSkill"]) {
                toRemoveIndex = index;
            }
        }
        $scope.stages[stage_id].splice(toRemoveIndex, 1);

        if ($scope.stages[stage_id].length > 0) {
            $scope["stage" + stage_id + "SelectedSkill"] = $scope.stages[stage_id][0].code;
        } else {
            $scope["stage" + stage_id + "SelectedSkill"] = "";
            $("#addSkillToTestButtonForStage" + stage_id).addClass("disabled");
        }

        $("#" + skill).hide();
    }

    $scope.removeSkill = function(skill) {
        $("#alerts").html('<div />');
        $scope.toTargetSkills.splice($scope.toTargetSkills.indexOf(skill), 1);
        $("#" + skill).show();
    }

    update_test_list = function () {
        $http.get("/professor/lesson_tests_and_skills/" + context.lessonId + ".json").
            success(function(data, status, headers, config) {
                $scope.stages = data.stages;
                $scope.toTargetSkills = [];

                for (i in $scope.stages) {
                    $scope["stage" + i + "SelectedSkill"] = $scope.stages[i][0].code;
                }
           })
    }

    update_test_list();
}
