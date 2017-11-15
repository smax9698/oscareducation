# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import random
from django.db.models import Count
from django.contrib.auth.models import User

from skills.models import LearningTrack, StudentSkill


class AuthUserManager(models.Manager):
    def get_queryset(self):
        return super(AuthUserManager, self).get_queryset().select_related('user')


class Professor(models.Model):

    objects = AuthUserManager()
    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.BigIntegerField(null=True, blank=True)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class Student(models.Model):

    objects = AuthUserManager()

    user = models.OneToOneField(User)
    is_pending = models.BooleanField(default=True)
    code = models.IntegerField(null=True, blank=True)
    code_created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return ("%s %s" % (
        self.user.first_name, self.user.last_name)) if self.user.first_name or self.user.last_name else self.user.username


    def generate_new_code(self):
        """Generate studenty password"""
        new_code = "%s" % (random.randint(1000, 9999))
        self.code = new_code
        self.is_pending = True
        self.save()
        return new_code

    class Meta:
        ordering = ['user__last_name']

    def get_email(self):
        if self.user.email.endswith("@example.com"):
            return ""
        return self.user.email

    def done_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=False)

    def todo_tests(self):
        return self.teststudent_set.filter(finished_at__isnull=True)

    def get_last_test(self):
        return self.teststudent_set.order_by('-test__created_at').first()

    def has_recommended_skills(self):
        for student_skill in self.studentskill_set.all():
            if student_skill.recommended_to_learn():
                return True

        return False

    def get_recommended_skills(self):
        """
        :return: Recommended skills of this student, ordered by group and required time.
        """
        def get_section(student_skill):
            return student_skill.skill.section.name

        def get_time(student_skill):
            return student_skill.skill.estimated_time_to_master

        # TODO At the moment sorting criterias of recommended skills are hardcoded
        return LearningTrack.sorting(['Group', 'Time'], {'Group': get_section, 'Time': get_time}, filter(lambda s: s.recommended_to_learn(), self.studentskill_set.all()))[:3]

    def get_three_next_recommended(self):
        """
        :return: The three first recommended skills of this student
        """
        return self.get_recommended_skills()[:3]

    def clear_targets(self):
        """Removes the target flag on all student skills"""
        student_skills = StudentSkill.objects.filter(student=self)
        for student_skill in student_skills:
            student_skill.is_target = False
            student_skill.save()

    def set_targets(self, target_skills):
        """ Assign at most 3 target skills to the student

            Set the is_target flag on matching student skills.
            If there is none, then a student skill is created for the target and for each prerequisite skill.

            :param target_skills A list of at most 3 Skills that should be targeted by this student.
        """
        if target_skills is None:
            raise ValueError("Null targets")

        if len(target_skills) == 0:
            raise ValueError("At least one target must be assigned and maximum 3.")

        if len(target_skills) > 3:
            raise ValueError("At most 3 target skills can be defined per student.")


        #Clear all target to run the learning_track algorithm with the new targets
        self.clear_targets()
        #recover all the student_skill for the current student
        student_skills = StudentSkill.objects.filter(student=self)
        for target_skill in target_skills:
            found = False
            for student_skill in student_skills:
                if student_skill.skill == target_skill:
                    student_skill.is_target = True
                    student_skill.save()
                    found = True
                    break
            # If the student skill is not found create a new one
            if not found:
                StudentSkill.objects.create(
                    student=self,
                    skill=target_skill,
                    is_target=True
                )
                #create a student skill for all the prerequisites of the target
                for prerequisite in target_skill.get_prerequisites_skills():
                    found = False

                    for student_skill in student_skills:
                        if student_skill.skill == prerequisite:
                            found = True
                            break
                    # if prerequisite not found in the studentskills create a new one
                    if not found:
                        StudentSkill.objects.create(
                            student=self,
                            skill=prerequisite,
                        )
    
    def get_three_next(self):
        """ Method that will get the three next skills to show to the student

            Return  an empty list if there is not
        """
        lt = LearningTrack.objects.filter(student=self).order_by('order')
        list = []
        i = 0
        for item in lt:
            if not item.student_skill.acquired:
                list.append(item)
                i += 1
            if i >= 3:
                break
        return list

    def get_learning_track(self):
        lt = LearningTrack.objects.filter(student=self).order_by('order')
        list_return = []
        for item in lt:
            list_return.append(item)

        return list_return

    def get_targeted_skills(self):
        return StudentSkill.objects.filter(is_target=True, student=self)
