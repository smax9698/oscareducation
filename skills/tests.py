from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student
from skills.models import Skill, LearningTrack, Relations,StudentSkill, Criteria

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
        user_stud.save()
        self.stud = Student.objects.create(user=user_stud, is_pending=False)
        self.stud.save()
        self.skills = []
        for i in range(0, 10):
            tmp = Skill.objects.create(code=i, name=i, section=i%3, estimated_time_to_master=250)
            tmp.save()
            self.skills.append(tmp)
        self.student_skills = []

        for skill in self.skills:
            sk = StudentSkill.objects.create(student=self.stud, skill=self.skills[1], is_target=True)
            self.student_skills.append(sk)

        self.student_skill = self.student_skill[0]
        self.skills_section_map = {}
        self.skills_depth_map = {}

        i = 1
        j = 0
        for skill in self.skills:
            Relations.objects.create(from_skill=self.skills[j], to_skill=self.skills[i], relation_type="depend_on")
            i+=1
            if i % 2 == 0:
                j+=1
            Relations.objects.create(from_skill=self.skills[2], to_skill=self.skills[1], relation_type="depend_on")

        self.level = Criteria.objects.create(name="Level")
        self.group = Criteria.objects.create(name="Group")
        self.time = Criteria.objects.create(name="Time")

    # # Create your tests here.
    # def test_set_skill_section_with_incorrect_params(self):
    #     with self.assertRaises(TypeError):
    #         LearningTrack._set_skill_section(None, None)
    #         LearningTrack._set_skill_section(None, self.skills_section_map)
    #         LearningTrack._set_skill_section(self.student_skill, None)
    #         LearningTrack._set_skill_section(self.student_skill, [])
    #
    # def test_set_skill_section_correct_update(self):
    #     LearningTrack._set_skill_section(self.student_skill, self.skills_section_map)
    #     section = self.student_skill.skill.section
    #     self.assertEquals(self.skills_section_map[self.student_skill], section)

    def test_set_skill_depth_with_incorrect_params(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_skill_depth(None, 0, None)
            LearningTrack._set_skill_depth(None, 0, self.skills_depth_map)
            LearningTrack._set_skill_depth(self.student_skill, 0, None)
            LearningTrack._set_skill_depth(self.student_skill, 0, [])
        with self.assertRaises(ValueError):
            LearningTrack._set_skill_depth(self.student_skill, -1, {})

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

    def test_set_level_with_incorrect_params(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_level(None,None,0)
            LearningTrack._set_level(None, self.skills_depth_map, 0)
            LearningTrack._set_level(self.student_skill, None, 0)
            LearningTrack._set_level(self.student_skill, [], 0)
        with self.assertRaises(ValueError):
            LearningTrack._set_level(self.student_skill,self.skills_depth_map,-1)

    def test_set_level_correct_update(self):
        LearningTrack._set_level(self.student_skill, self.skills_depth_map, 0)
        self.assertEquals(self.skills_depth_map[self.student_skill[0]], 0)
        self.assertEquals(self.skills_depth_map[self.student_skill[1]], 1)
        self.assertEquals(self.skills_depth_map[self.student_skill[2]], 1)
        self.assertEquals(self.skills_depth_map[self.student_skill[3]], 2)
        self.assertEquals(self.skills_depth_map[self.student_skill[4]], 2)
        self.assertEquals(self.skills_depth_map[self.student_skill[5]], 2)
        self.assertEquals(self.skills_depth_map[self.student_skill[6]], 2)
        self.assertEquals(self.skills_depth_map[self.student_skill[7]], 3)
        self.assertEquals(self.skills_depth_map[self.student_skill[8]], 3)
        self.assertEquals(self.skills_depth_map[self.student_skill[9]], 3)
        self.assertEquals(self.skills_depth_map[self.student_skill[10]], 3)

    def test_get_criteria_functions_with_incorrect_params(self):
        targets = [self.student_skills[1], self.student_skills[3]]
        with self.assertRaises(TypeError):
            LearningTrack._get_criteria_functions(None)

    def test_get_criteria_maps_correct_update(self):

        targets = [self.student_skills[0], self.student_skills[1]]
        maps = LearningTrack._get_criteria_functions(targets)
        get_level = maps[self.level.name]
        get_section = maps[self.section.name]
        get_time = maps[self.time.name]

        self.assertEquals(get_level(self.student_skill[0]), 0)
        self.assertEquals(get_level(self.student_skill[1]), 2)
        self.assertEquals(get_level(self.student_skill[2]), 1)
        self.assertEquals(get_level(self.student_skill[3]), 3)
        self.assertEquals(get_level(self.student_skill[4]), 3)
        self.assertEquals(get_level(self.student_skill[5]), 2)
        self.assertEquals(get_level(self.student_skill[6]), 2)
        self.assertEquals(get_level(self.student_skill[7]), 4)
        self.assertEquals(get_level(self.student_skill[8]), 4)
        self.assertEquals(get_level(self.student_skill[9]), 4)
        self.assertEquals(get_level(self.student_skill[10]), 4)

        for student_skill in self.student_skills:
            self.assertEquals(get_section(student_skill), student_skill.skill.section.name)
            self.assertEquals(get_time(student_skill), student_skill.skill.estimated_time_to_master)

    def test_sorting_with_incorrect_param(self):

        ordered_criteria_names = [self.level.name, self.group.name, self.time.name]
        targets = [self.student_skills[0],self.student_skills[1]]
        maps = LearningTrack._get_criteria_functions(targets)
        get_level = maps[self.level.name]
        get_section = maps[self.section.name]
        get_time = maps[self.time.name]

        with self.assertRaises(TypeError):
            LearningTrack._sorting(None,None,None)
            LearningTrack._sorting(None, maps,self.student_skills)
            LearningTrack._sorting(ordered_criteria_names, None, self.student_skills)
            LearningTrack._sorting(ordered_criteria_names, maps, None)

        with self.assertRaises(ValueError):
            LearningTrack._sorting(['abc','xyz'], maps, self.student_skills)

