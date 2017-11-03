# -*- coding: utf-8 -*-
import unittest

#from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

class TestSkills(unittest.TestCase):
    '''
    Changez le nom de classe avec un truc plus précis.
    '''

    def setUp(self):
        '''Initialization de vos tests'''
        pass

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