from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Professor, Student, StudentSkill
from skills.models import Skill, LearningTrack

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
        for i in range(1, 11):
            tmp = Skill.objects.create(code=i, name=i, section=i)
            tmp.save()
            self.skills.append(tmp)

        self.student_skill = StudentSkill.objects.create(student=self.stud, skill=self.skills[0])
        self.skills_section_map = {}
        self.skills_depth_map = {}

    # Create your tests here.
    def test_set_skill_section_with_incorrect_params(self):
        with self.assertRaises(TypeError):
            LearningTrack._set_skill_section(None, None)
            LearningTrack._set_skill_section(None, self.skills_section_map)
            LearningTrack._set_skill_section(self.student_skill, None)
            LearningTrack._set_skill_section(self.student_skill, [])

    def test_set_skill_section_correct_update(self):
        LearningTrack._set_skill_section(self.student_skill, self.skills_section_map)
        section = self.student_skill.skill.section
        self.assertEquals(self.skills_section_map[self.student_skill], section)

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
        new_value =  4

        self.skills_depth_map[self.student_skill] = old_value
        LearningTrack._set_skill_depth(self.student_skill, zero, self.skills_depth_map)
        self.assertEquals(self.skills_depth_map[self.student_skill], old_value)

        LearningTrack._set_skill_depth(self.student_skill, new_value, self.skills_depth_map)
        self.assertEquals(self.skills_depth_map[self.student_skill], new_value)

    def test_set_level_with_incorrect_params(self):
