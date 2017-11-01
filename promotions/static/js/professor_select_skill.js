function selectSkillController($scope, $http) {
    $scope.stages = [];

    $scope.setTemporaryTargets = function(lessonPk,professorPk) {
        $http.post("/professor/lesson/" + lessonPk + "/set_learning_track_redirect/", {
            "target_skill_codes": $scope.toTargetSkills,
            "student_pk": $scope.selection,
            "professor_pk": professorPk
        }).success(function(data, status, headers, config) {
            new_url = "../set_learning_track/";
            $scope.selection.forEach(function(entry) {
                new_url += entry + "_";
            });
            window.location.href = new_url.substr(0, new_url.length - 1);
        })
    };

    $scope.addSkillToTargets = function(stage_id) {
        if ($scope.stages[stage_id].length === 0)
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
            if ($scope.stages[stage_id][index].code === $scope["stage" + stage_id + "SelectedSkill"]) {
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
    };

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
                $scope.selection = [];

                for (i in $scope.stages) {
                    $scope["stage" + i + "SelectedSkill"] = $scope.stages[i][0].code;
                }
           })
    };

    $scope.toggleSelection = function toggleSelection(student) {

        var idx = $scope.selection.indexOf(student);
        // Is currently selected
        if (idx > -1) {
          $scope.selection.splice(idx, 1);
        }
        // Is newly selected
        else {
          $scope.selection.push(student);
        }
      };

    update_test_list();
}
