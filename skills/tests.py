from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student
from skills.models import Skill, LearningTrack, Relations, StudentSkill, Criteria, Section, ProfessorCriteria
from exceptions import TypeError, ValueError
from django.utils import timezone
'''  
    To run tests, make sure the oscar user in your DB has the can create DB option checked 
    Do a makemigrations and migrate to have the last version of the DB (professor criteria included) 
    If the migrate doesn't work, you're going to have to delete everything (DB and project included) and do 
    the whole installation again. 
    Once it's done, just do python manage.py tests (It's going to check every tests and the 3 from promotions 
    are failing but it has nothing to do with our work. 
'''


class LearningTrackTests(TestCase):
    def setUp(self):
        user_stud = User.objects.create(username="user")
        self.stud = Student.objects.create(user=user_stud, is_pending=False)
        user_prof = User.objects.create(username="teacher")
        self.prof = Professor.objects.create(user=user_prof)

        self.level = Criteria.objects.create(name="Level")
        self.section = Criteria.objects.create(name="Group")
        self.time = Criteria.objects.create(name="Time")

        ProfessorCriteria.objects.create(professor=self.prof,criteria=self.level,order=0)
        ProfessorCriteria.objects.create(professor=self.prof,criteria=self.section,order=1)
        ProfessorCriteria.objects.create(professor=self.prof,criteria=self.time,order=2)

        self.skills = []
        section_a = Section.objects.create(name="A")
        section_b = Section.objects.create(name="B")
        section_c = Section.objects.create(name="C")
        section_d = Section.objects.create(name="D")
        self.sections = [section_a, section_b, section_c, section_d]

        tmp = Skill.objects.create(code=0, name="Alpha", section=self.sections[0], estimated_time_to_master=250)
        self.skills.append(tmp)
        tmp = Skill.objects.create(code=1, name="Beta", section=self.sections[0], estimated_time_to_master=250)
        self.skills.append(tmp)
        tmp = Skill.objects.create(code=2, name="Gamma", section=self.sections[1], estimated_time_to_master=250)
        self.skills.append(tmp)
        tmp = Skill.objects.create(code=3, name="Omega", section=self.sections[2], estimated_time_to_master=250)
        self.skills.append(tmp)
        tmp = Skill.objects.create(code=4, name="Theta", section=self.sections[1], estimated_time_to_master=250)
        self.skills.append(tmp)
        tmp = Skill.objects.create(code=5, name="Epsilon", section=self.sections[3], estimated_time_to_master=250)
        self.skills.append(tmp)

        self.student_skills = []

        for skill in self.skills:
            sk = StudentSkill.objects.create(student=self.stud, skill=skill, is_target=True,acquired=timezone.now())
            self.student_skills.append(sk)

        self.student_skill = self.student_skills[0]
        self.skills_section_map = {}
        self.skills_depth_map = {}

        Relations.objects.create(from_skill=self.skills[0], to_skill=self.skills[1], relation_type="depend_on")
        Relations.objects.create(from_skill=self.skills[0], to_skill=self.skills[2], relation_type="depend_on")
        Relations.objects.create(from_skill=self.skills[1], to_skill=self.skills[3], relation_type="depend_on")
        Relations.objects.create(from_skill=self.skills[1], to_skill=self.skills[4], relation_type="depend_on")
        Relations.objects.create(from_skill=self.skills[2], to_skill=self.skills[5], relation_type="depend_on")
        Relations.objects.create(from_skill=self.skills[2], to_skill=self.skills[1], relation_type="depend_on")

    # ------------------------------------------------------------------------------------------#

    def test_set_skill_depth_with_incorrect_student_skill(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_skill_depth(None, 0, self.skills_depth_map)

    def test_set_skill_depth_with_incorrect_skills_depth_map(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_skill_depth(self.student_skill, 0, None)

    def test_set_skill_depth_with_incorrect_depth(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_skill_depth(self.student_skill, None, self.skills_depth_map)

    def test_set_skill_depth_with_negative_depth(self):
        with self.assertRaises(ValueError):
            LearningTrack._set_skill_depth(self.student_skill, -1, self.skills_depth_map)

    def test_set_skill_depth_correct_update_without_override(self):
        zero = 0
        LearningTrack._set_skill_depth(self.student_skill, zero,self.skills_depth_map)
        self.assertEquals(self.skills_depth_map[self.student_skill], zero)

    def test_set_skill_depth_correct_update_with_override(self):
        zero = 0
        old_value = 3
        new_value = 4

        self.skills_depth_map[self.student_skill] = old_value
        LearningTrack._set_skill_depth(self.student_skill, zero, self.skills_depth_map)
        self.assertEquals(self.skills_depth_map[self.student_skill], old_value)

        LearningTrack._set_skill_depth(self.student_skill, new_value, self.skills_depth_map)
        self.assertEquals(self.skills_depth_map[self.student_skill], new_value)

    # ------------------------------------------------------------------------------------------#

    def test_set_level_with_incorrect_student_skill(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_level(None, self.skills_depth_map, 0)

    def test_set_level_with_incorrect_skills_depth_map(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_level(self.student_skill, None, 0)

    def test_set_level_depth_with_incorrect_level(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_level(self.student_skill, self.skills_depth_map, None)

    def test_set_level_with_negative_level(self):
        with self.assertRaises(ValueError):
            LearningTrack._set_level(self.student_skill, self.skills_depth_map, -1)

    def test_set_level_correct_update(self):
        LearningTrack._set_level(self.student_skill, self.skills_depth_map, 0)
        self.assertEquals(self.skills_depth_map[self.student_skills[0]], 0)
        self.assertEquals(self.skills_depth_map[self.student_skills[1]], 2)
        self.assertEquals(self.skills_depth_map[self.student_skills[2]], 1)
        self.assertEquals(self.skills_depth_map[self.student_skills[3]], 3)
        self.assertEquals(self.skills_depth_map[self.student_skills[4]], 3)
        self.assertEquals(self.skills_depth_map[self.student_skills[5]], 2)

    # ------------------------------------------------------------------------------------------#

    def test_get_criteria_functions_with_incorrect_targets(self):
        with self.assertRaises(TypeError):
            LearningTrack._get_criteria_functions(None)

    def test_get_criteria_functions_correct_update(self):
        targets = [self.student_skills[0], self.student_skills[1]]
        maps = LearningTrack._get_criteria_functions(targets)

        get_level = maps[self.level.name]
        get_section = maps[self.section.name]
        get_time = maps[self.time.name]

        self.assertEquals(get_level(self.student_skills[0]), 0)
        self.assertEquals(get_level(self.student_skills[1]), 2)
        self.assertEquals(get_level(self.student_skills[2]), 1)
        self.assertEquals(get_level(self.student_skills[3]), 3)
        self.assertEquals(get_level(self.student_skills[4]), 3)
        self.assertEquals(get_level(self.student_skills[5]), 2)

        for student_skill in self.student_skills:
            self.assertEquals(get_section(student_skill), student_skill.skill.section.name)
            self.assertEquals(get_time(student_skill), student_skill.skill.estimated_time_to_master)

    # ------------------------------------------------------------------------------------------#

    def test_sorting_with_incorrect_ordered_criteria_names(self):
        targets = [self.student_skills[0], self.student_skills[1]]
        maps = LearningTrack._get_criteria_functions(targets)
        with self.assertRaises(TypeError):
            LearningTrack._sorting(None, maps, self.student_skills)

    def test_sorting_with_incorrect_criteria_functions(self):
        ordered_criteria_names = [self.level.name, self.section.name, self.time.name]
        with self.assertRaises(TypeError):
            LearningTrack._sorting(ordered_criteria_names, None, self.student_skills)

    def test_sorting_with_incorrect_student_skills(self):
        ordered_criteria_names = [self.level.name, self.section.name, self.time.name]
        targets = [self.student_skills[0], self.student_skills[1]]
        maps = LearningTrack._get_criteria_functions(targets)
        with self.assertRaises(TypeError):
            LearningTrack._sorting(ordered_criteria_names, maps, None)

    def test_sorting_with_invalid_criteria_names(self):
        with self.assertRaises(ValueError):
            targets = [self.student_skills[0], self.student_skills[1]]
            maps = LearningTrack._get_criteria_functions(targets)
            LearningTrack._sorting(['abc','xyz'], maps, self.student_skills)

    def test_sorting_correct_sort(self):
        targets = [self.student_skills[0], self.student_skills[1]]
        student_skills_list = LearningTrack._build_student_skills_list(targets)

        ordered_criteria_names = LearningTrack._get_ordered_criteria_names(self.prof)
        criteria_functions = LearningTrack._get_criteria_functions(targets)
        lt = LearningTrack._sorting(ordered_criteria_names, criteria_functions, student_skills_list)

        self.assertEquals(lt[0].skill.code, self.student_skills[4].skill.code)
        self.assertEquals(lt[1].skill.code, self.student_skills[3].skill.code)
        self.assertEquals(lt[2].skill.code, self.student_skills[5].skill.code)
        self.assertEquals(lt[3].skill.code, self.student_skills[1].skill.code)
        self.assertEquals(lt[4].skill.code, self.student_skills[2].skill.code)
        self.assertEquals(lt[5].skill.code, self.student_skills[0].skill.code)


    # ------------------------------------------------------------------------------------------#

    def test_higher_in_prerequisites_tree_incorrect_params(self):
        with self.assertRaises(TypeError):
            LearningTrack._higher_in_prerequisites_tree(None,None)

    def test_higher_in_prerequisites_tree_a_parent_of_b(self):
        result = LearningTrack._higher_in_prerequisites_tree(self.student_skills[0],self.student_skills[3])
        self.assertEquals(result,1)

    def test_higher_in_prerequisites_tree_b_parent_of_a(self):
        result = LearningTrack._higher_in_prerequisites_tree(self.student_skills[3],self.student_skills[0])
        self.assertEquals(result,-1)

    def test_higher_in_prerequisites_tree_a_equals_b(self):
        result = LearningTrack._higher_in_prerequisites_tree(self.student_skills[2],self.student_skills[2])
        self.assertEquals(result,0)

    def test_higher_in_prerequisites_tree_neighbours(self):
        result = LearningTrack._higher_in_prerequisites_tree(self.student_skills[3],self.student_skills[4])
        self.assertEquals(result,0)

    # ------------------------------------------------------------------------------------------#

    def test_prerequisite_list_incorrect_student_skill(self):
        with self.assertRaises(TypeError):
            LearningTrack._prerequisite_list(None)

    def test_prerequisite_list_correct_result(self):
        student_skills = LearningTrack._prerequisite_list(self.student_skill)
        for sk in student_skills:
            print sk.skill.name ,"\n"
            self.assertTrue(sk in self.student_skills)
        self.assertEquals(student_skills.__len__(), 6)

    # ------------------------------------------------------------------------------------------#

    def test_new_learning_track_incorrect_student(self):
        with self.assertRaises(TypeError):
            LearningTrack.new_learning_track(None,self.prof)

    def test_new_learning_track_incorrect_professor(self):
        with self.assertRaises(TypeError):
            LearningTrack.new_learning_track(self.stud,None)

    # ------------------------------------------------------------------------------------------#

    def test_build_student_skills_list_incorrect_targets(self):
        with self.assertRaises(TypeError):
            LearningTrack._build_student_skills_list(None)

    def test_build_student_skills_list_correct_result(self):
        targets = [self.student_skills[0], self.student_skills[1]]
        student_skills_list = LearningTrack._build_student_skills_list(targets)
        for student_skill in student_skills_list:
            self.assertTrue(student_skill in self.student_skills)
        self.assertEquals(student_skills_list.__len__(), 6)
