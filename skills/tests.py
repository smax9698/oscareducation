# -*- coding: utf-8 -*-
import unittest
from mock import patch

#from __future__ import unicode_literals

from django.test import TestCase
from django.conf import settings
from skills.models import StudentSkill

# Create your tests here.

class TestSkills(TestCase):
    '''
    Changez le nom de classe avec un truc plus précis.
    '''

    def setUp(self):
        settings.configure()
        '''Initialization de vos tests'''
        patcher_StudentSkill = patch(StudentSkill)
        set = patcher_StudentSkill.objects.all()
        #remove = set.exclude(is_objective = None)
        test_student = set.first().student
        test_student_skills = set.filter(student=test_student)
        test_objective_skills = test_student_skills.exclude(is_objective=None)


    def tearDown(self):
        '''De-init apres chaque test'''
        pass

    def test_example(self):
        un   = 1
        deux = 2
        self.assertEqual(un + un, deux)

    def test_example2(self):
        un   = 1
        deux = 2
        self.assertEqual(un + un + un, deux)

    def test_no_objective(self):
        settings.configure()
        patcher_StudentSkill = patch(StudentSkill)
        set = patcher_StudentSkill.objects.all()
        # remove = set.exclude(is_objective = None)
        test_student = set.first().student
        test_student_skills = set.filter(student=test_student)
        test_objective_skills = test_student_skills.exclude(is_objective=None)

        for test_objective_skill in test_objective_skills:
            patcher_StudentSkill.remove_objective(test_objective_skill)
        self.assertEqual(patcher_StudentSkill.objects.filter(student=test_student, is_objective=True),Queryset())

    def test_one_objective(self):
        settings.configure()
        patcher_StudentSkill = patch(StudentSkill)
        set = patcher_StudentSkill.objects.all()
        # remove = set.exclude(is_objective = None)
        test_student = set.first().student
        test_student_skills = set.filter(student=test_student)
        test_objective_skills = test_student_skills.exclude(is_objective=None)

        first_objective = test_student_skills.first()
        patcher_StudentSkill.set_objective(first_objective)
        self.assertEqual(patcher_StudentSkill.objects.filter(student=test_student, is_objective=True).first(),first_objective)
        #TODO assert children
