from django.test import TestCase
from users.models import Student, LearningTrack, User, StudentSkill
from skills.models import Skill
from django.utils import timezone

# Create your tests here.

''' This class is going to test 1 methods : 
        - Get three next targeted skills 
    
'''


class RecommandedSkillsTest(TestCase):
    ''' Setup :
            - 1 student.
            - 10 skills
    '''

    def setUp(self):
        user_stud = User.objects.create(username="user")
        user_stud.save()
        self.stud = Student.objects.create(user=user_stud, is_pending=False)
        self.stud.save()
        self.skills = []
        for i in range(1, 11):
            tmp = Skill.objects.create(code=i, name=i)
            tmp.save()
            self.skills.append(tmp)

    ''' Test when the student has no learning track '''

    def testNoLearningTrack(self):
        self.assertEqual(len(self.stud.get_three_next()), 0)

    ''' Test when the student has one left skill on the learning track, 
        with >3 skills acquired before'''

    def testLearningTrack1(self):
        for i in range(0, 5):
            tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[i], acquired=timezone.now())
            tmp_ss.save()

            tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=i)
            tmp_lt.save()

        # Set up the non aqcuired here
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[5])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=5)
        tmp_lt.save()

        self.assertEqual(len(self.stud.get_three_next()), 1)
        self.assertEqual(self.stud.get_three_next()[0], tmp_lt)

    ''' Test when the students has exactly 3 skills'''

    def testLearningTrackEquals3(self):
        list_lt=[]
        for i in range(0, 3):
            tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[i])
            tmp_ss.save()

            tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=i)
            list_lt.append(tmp_lt)
            tmp_lt.save()

        self.assertEqual(len(self.stud.get_three_next()), 3)
        self.assertEqual(self.stud.get_three_next()[0], list_lt[0])
        self.assertEqual(self.stud.get_three_next()[1], list_lt[1])
        self.assertEqual(self.stud.get_three_next()[2], list_lt[2])

    ''' Test when the student has some skills acquired, and more then 3 skills left'''
    ''' 4 acquired 5 non acquired '''
    def testLearningTrackMore3(self):
        for i in range(0, 4):
            tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[i], acquired=timezone.now())
            tmp_ss.save()

            tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=i)
            tmp_lt.save()

        list_lt=[]
        for i in range(4, 9):
            tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[i])
            tmp_ss.save()

            tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=i)
            list_lt.append(tmp_lt)
            tmp_lt.save()

        self.assertEqual(len(self.stud.get_three_next()), 3)
        self.assertEqual(self.stud.get_three_next()[0], list_lt[0])
        self.assertEqual(self.stud.get_three_next()[1], list_lt[1])
        self.assertEqual(self.stud.get_three_next()[2], list_lt[2])

    ''' Test when the student has acquired some skills, but not in order : 
        Acquired, acquired, not, acquired, not not acquired, not not not ...
    '''
    def testBagdadTrack(self):
        list_lt=[]
        # acquired order = 1 2 4 7 acquired
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[0], acquired=timezone.now())
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=1)
        tmp_lt.save()
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[1], acquired=timezone.now())
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=2)
        tmp_lt.save()
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[3], acquired=timezone.now())
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=4)
        tmp_lt.save()
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[6], acquired=timezone.now())
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=7)
        tmp_lt.save()

        #Non acquired 3 5 6 8 9 10
        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[2])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=3)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[4])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=5)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[5])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=6)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[7])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=8)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[8])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=9)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        tmp_ss = StudentSkill.objects.create(student=self.stud, skill=self.skills[9])
        tmp_ss.save()
        tmp_lt = LearningTrack.objects.create(student=self.stud, student_skill=tmp_ss, order=10)
        list_lt.append(tmp_lt)
        tmp_lt.save()

        self.assertEqual(len(self.stud.get_three_next()), 3)
        self.assertEqual(self.stud.get_three_next()[0], list_lt[0])
        self.assertEqual(self.stud.get_three_next()[1], list_lt[1])
        self.assertEqual(self.stud.get_three_next()[2], list_lt[2])

