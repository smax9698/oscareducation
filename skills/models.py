# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from examinations.models import Context
import numbers
from django.contrib.postgres.fields import ArrayField


class Skill(models.Model):
    """[FR] Compétence

        A Skill can be evaluated through questions answered by a student.
        Thus, when evaluated, a Skill can be acquired by a student, or not.

    """

    code = models.CharField(max_length=20, unique=True, db_index=True)
    """The Skill reference code"""

    name = models.CharField(max_length=255)
    """The Skill name"""

    description = models.CharField(max_length=255)
    """The Skill description"""

    section = models.ForeignKey('Section', null=True)
    """The Section to which the Skill belongs @to remove after """

    # depends_on = models.ManyToManyField('Skill', related_name="depends_on+")
    """If a Skill depends on another (i.e. a prerequisite), this is set in this relation"""

    # similar_to = models.ManyToManyField('Skill', related_name="similar_to+")
    """The Skills that are similar, but with different references"""

    resource = models.ManyToManyField('resources.Resource', related_name="skill_resource+")
    """The Resources linked to this Skill. A Resource can be linked to several Skills"""

    image = models.CharField(max_length=255, null=True, blank=True)
    """Icon used to categorize the Skill"""

    oscar_synthese = models.TextField(null=True, blank=True)
    """The Skill abstract provided by Oscar"""

    modified_by = models.ForeignKey(User, null=True)
    """The last user that modified this Skill"""

    relations = models.ManyToManyField("self", through="Relations", related_name="related_to", symmetrical=False)
    """ Make relation between skills through a relation Model with a strict options : depended_on , similar_to  and identic_to """

    estimated_time_to_master = models.PositiveIntegerField(null=False, default=250)
    """ The time an average student would take to finish this Skill """

    def __unicode__(self):
        return self.code + " : " + self.name

    def skills_with_exercice_count(self):
        """ Count Context in relation with the current Skills"""
        return Context.objects.filter(skill=self).count()

    def get_prerequisites_skills(self):
        """

        :return: Queryset of prerequisites Skills for the current Skill
        """

        return self.relations.filter(
            to_skill__relation_type="depend_on"
        )

    def get_depending_skills(self):
        """

        :return: Queryset of Skills depending on the current Skill
        """

        return self.related_to.filter(
            from_skill__relation_type="depend_on"
        )


class Relations(models.Model):
    """ The through relation skill model """

    from_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='from_skill', default=0)
    to_skill = models.ForeignKey(Skill, null=False, blank=False, related_name='to_skill', default=0)
    relation_type = models.CharField(max_length=255, null=False, blank=False, choices=(

        ("depend_on", "dépend de"),
        ("similar_to", "similaire à"),
        ("identic_to", "identique à"),
    ))

    def __unicode__(self):
        return self.from_skill.code + " , " + self.to_skill.code + ", " + self.relation_type

    class Meta:
        verbose_name = 'Relations between Skill'
        verbose_name_plural = 'Relations between Skill\'s'


class Section(models.Model):
    """[FR] Rubrique

        A Section regroups a list of CodeR and a list
        of Skills. Sections form socles (most of the
        time, a socle represents a year of mathematics
        class)

    """

    name = models.CharField(max_length=255)
    """The Section name"""
    # editable=False,
    resource = models.ManyToManyField('resources.Resource', related_name="section_resource+")
    """The resources linked to this Section. A resource can be linked to several Sections"""

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CodeR(models.Model):
    """[FR] Ressource (ou Code R),
    à ne pas confondre avec une ressource pédagogique

        A CodeR describes concept(s) to master, in orderskills_coder_skill
        to acquire the skill(s) based on that CodeR.
        Unlike a Skill, A CodeR cannot be evaluated
        directly.

    """

    section = models.ForeignKey('Section', null=True)
    """The Section to which the CodeR belongs"""

    sub_code = models.CharField(max_length=10)
    """The CodeR reference code"""

    name = models.CharField(max_length=255)
    """The CodeR name"""

    # paired_to = models.ManyToManyField('CodeR', related_name="paired_to+")
    """@todo remove """

    resource = models.ManyToManyField('resources.Resource', related_name="coder_resource+")
    """The Resources linked to this CodeR. A Resource can be linked to several CodeR"""

    skill = models.ManyToManyField('Skill', related_name="coder_skill+")
    """The Skills linked to this CodeR. A Skill can be linked to several CodeR"""

    def __unicode__(self):
        return self.sub_code + " : " + self.name

    class Meta:
        verbose_name = 'CodeR'
        verbose_name_plural = 'CodeR'


class CodeR_relations(models.Model):
    """ The through relation CodeR model  """

    from_coder = models.ForeignKey(CodeR, null=False, blank=False, related_name='from_coder', default=0)
    to_coder = models.ForeignKey(CodeR, null=False, blank=False, related_name='to_coder', default=0)
    relation_type = models.CharField(max_length=255, null=False, blank=False, choices=(

        ("depend_on", "dépend de"),
        ("similar_to", "similaire à"),
        ("identic_to", "identique à"),
    ))

    def __unicode__(self):
        return self.from_coder.name + " , " + self.to_coder.name + ", " + self.relation_type

    class Meta:
        verbose_name = 'Relations between CodeR'
        verbose_name_plural = 'Relations between CodeR\'s'


class SkillHistory(models.Model):
    """
        The reason why a Skill is acquired or not,
        or not yet, when and by who/how

    """

    skill = models.ForeignKey(Skill)
    """The Skill to validate"""
    student = models.ForeignKey('users.Student')
    """The Student concerned by this Skill"""
    datetime = models.DateTimeField(auto_now_add=True)
    """The date the Skill status was created"""
    value = models.CharField(max_length=255, choices=(
        ('unknown', 'Inconnu'),
        ('acquired', 'Acquise'),
        ('not acquired', 'None Acquise'),
    ))
    """The Skill status : unknown, acquired or not acquired"""

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    reason_object = GenericForeignKey('content_type', 'object_id')
    reason = models.CharField(max_length=255)
    """Why the Skill is validated or not"""

    by_who = models.ForeignKey(User)

    class Meta:
        ordering = ['datetime']


class StudentSkill(models.Model):
    """
        The link between a Skill and a Student
    """
    student = models.ForeignKey('users.Student')
    """The Student concerned by the Skill"""
    skill = models.ForeignKey(Skill)
    """The Skill the Student acquired/did not acquired"""
    tested = models.DateTimeField(default=None, null=True)
    """When the Skill was tested"""
    acquired = models.DateTimeField(default=None, null=True)
    """When the Skill was acquired"""
    is_target = models.NullBooleanField(null=True, default=False, blank=True)
    """Whether the Skill is targeted by this student or not"""
    # bad: doesn't support regression

    def __unicode__(self):
        return u"%s - %s - %s" % (
            self.student, self.skill, "green" if self.acquired else ("orange" if self.tested else "white"))

    def go_down_visitor(self, function):
        """Help function to explore and validate prerequisites when a Skill is validated"""
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(
                    skill__in=student_skill.skill.get_prerequisites_skills(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    # TODO: Does not work, need to create a reverse to the Manytomany relation
    def go_up_visitor(self, function):
        """
        Help function to explore and invalidate (parent) Skill that depends on the failed Skill.
        A failed prerequisite implies that the Skills that depends on it must be failed too.
        """
        # protective code against loops in skill tree
        already_done = set()

        def traverse(student_skill):
            function(student_skill)

            for sub_student_skill in StudentSkill.objects.filter(
                    skill__in=student_skill.skill.get_prerequisites_skills(), student=self.student):
                if sub_student_skill.id not in already_done:
                    already_done.add(sub_student_skill.id)
                    traverse(sub_student_skill)

        traverse(self)

    def validate(self, who, reason, reason_object):
        """Validates a Skill (change its status to "acquired")"""

        def validate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.acquired = datetime.now()
            student_skill.save()

        self.go_down_visitor(validate_student_skill)

    def unvalidate(self, who, reason, reason_object):
        """Invalidates a Skill (change its status to "not acquired")"""

        def unvalidate_student_skill(student_skill):
            SkillHistory.objects.create(
                skill=self.skill,
                student=self.student,
                value="not acquired",
                by_who=who,
                reason=reason if student_skill == self else "Déterminé depuis une réponse précédente.",
                reason_object=reason_object,
            )

            student_skill.acquired = None
            student_skill.tested = datetime.now()
            student_skill.save()

        # Up traversal does not work, disabled
        # self.go_up_visitor(unvalidate_student_skill)

        # TODO: erase the following lines when go_up_visitor is repaired
        SkillHistory.objects.create(
            skill=self.skill,
            student=self.student,
            value="not acquired",
            by_who=who,
            reason=reason,
            reason_object=reason_object,
        )
        self.acquired = None
        self.tested = datetime.now()
        self.save()

    def default(self, who, reason, reason_object):
        """"Reset" a Skill (change its status to "unknown")"""
        SkillHistory.objects.create(
            skill=self.skill,
            student=self.student,
            value="unknown",
            by_who=who,
            reason=reason,
            reason_object=reason_object,
        )

        self.acquired = None
        self.tested = None
        self.save()

    def recommended_to_learn(self):
        """
        Determines if the Skill is to recommend to the Student.
        All the tested and not acquired Skills will be recommended,
        except if at least one of its prerequisites is not acquired
        """
        if self.acquired or not self.tested:
            return False

        for skill in self.skill.get_prerequisites_skills():
            skill = StudentSkill.objects.get(student=self.student, skill=skill)
            if not skill.acquired and skill.tested:
                return False

        return True

    class Meta:
        indexes = [
            models.Index(fields=['student', 'skill'])
        ]

class LearningTrack(models.Model):
    """[FR] Chemin d'apprentissage

        A learning track is an ordered sequence of skills the student should learn.
        Skills student should learns are the targeted skills (at most 3) and all their non-acquired prerequisites.
        Each object points to a StudentSkill of the whole track.

    """

    # TODO Remove as we can already get it from student_skill
    student = models.ForeignKey('users.Student')
    """The Student concerned by this LT"""

    student_skill = models.ForeignKey('StudentSkill')
    """This StudentSkill objects links with the Student and the Skill as well as its acquired status."""

    order = models.PositiveIntegerField()
    """Order of the skill in the learning track"""

    locked = models.BooleanField(default=False)
    """Whether the LT is locked or not"""

    cleared = models.BooleanField(default=False)
    """Whether the LT is cleared or not"""

    @staticmethod
    def new_learning_track(student, professor):
        """
        Create a new learning track for student based on the criteria of professor
        Any previously existing learning track will be overridden

        :param student:the student who owns the learning track
        :param professor:the teacher who has specified the targets skills for student
        """

        LearningTrack.objects.filter(student=student).delete()  # Clear previous learning track, if any

        targets = StudentSkill.objects.filter(student=student, is_target=True)

        student_skills_list = LearningTrack._build_student_skills_list(targets)

        ordered_criteria_names = LearningTrack._get_ordered_criteria_names(professor)
        criteria_functions = LearningTrack._get_criteria_functions(targets)

        learning_track = LearningTrack._sorting(ordered_criteria_names, criteria_functions, student_skills_list)
        for i in range(0, len(learning_track)):
            LearningTrack.objects.create(
                student=student,
                student_skill=learning_track[i],
                order=i
            )

    @staticmethod
    def _get_ordered_criteria_names(professor):
        """
        :param professor: A professor
        :return: The ordered criteria names defined by hand by the professor
        """
        return list(
            map(lambda x: x.criteria.name, ProfessorCriteria.objects.filter(professor=professor).order_by('order')))

    @staticmethod
    def _build_student_skills_list(targets):
        """
        :return a list of StudentSkill objects with targets and their prerequisites
        We know targets&prerequisites have been added in :func:'users.models.Student.set_targets'
        """
        student_skills = set()

        for target in targets:
            student_skills.update(LearningTrack._prerequisite_list(target))

        return list(student_skills)

    @staticmethod
    def _prerequisite_list(student_skill):
        """
        List to iterate through a student skill and all its prerequisites if they are not acquired
        NOTE : THE STUDENT SKILL IN PARAMETER IS INCLUDED
        """
        # TODO Avoid always recomputing the prerequisites ?
        if student_skill.acquired is None:
            student_skills = [student_skill]
            for prerequisite in StudentSkill.objects.filter(skill__in=student_skill.skill.get_prerequisites_skills(),
                                                            student=student_skill.student):
                student_skills.extend(LearningTrack._prerequisite_list(prerequisite))
            return student_skills
        else:
            return []

    @staticmethod
    def _higher_in_prerequisites_tree(a, b):
        """
        Relation of requirement between two student skills
        Check whether b is direct or indirect prerequisite (even through a long chain) of a
        :param a A StudentSkill
        :param b Another StudentSkill
        :return 0 if equal or unrelated; 1 if b prerequisite of a, -1 if a prerequisite of b
        """
        if a.skill == b.skill:
            return 0
        elif b in LearningTrack._prerequisite_list(a):
            return 1
        elif a in LearningTrack._prerequisite_list(b):
            return -1
        else:  # not related
            return 0

    @staticmethod
    def _sorting(ordered_criteria_names, criteria_functions, student_skills_list):
        """
        Sort skills list to return the learning track
        :param ordered_criteria_names: list of criteria names ordered by importance
        :param criteria_functions:Dictionary(criteria name, dictionary(skill,value based on the criteria))
        :param student_skills_list:List of all the skills to be ordered
        :return: the list of the learning track
        """

        if ordered_criteria_names is None or type(ordered_criteria_names) is not list \
                or criteria_functions is None or type(criteria_functions) is not dict \
                or student_skills_list is None or type(student_skills_list) is not list:
            raise TypeError

        for criteria_name in reversed(ordered_criteria_names):
            if criteria_name not in criteria_functions:
                raise ValueError("Unknown criteria : " + criteria_name)
            criteria_function = criteria_functions[criteria_name]
            student_skills_list.sort(key=criteria_function)
        student_skills_list.sort(LearningTrack._higher_in_prerequisites_tree)
        return student_skills_list

    @staticmethod
    def _get_criteria_functions(targets):
        """
        Get the key functions of each criteria used for the sorting
        :param targets:Targeted student skills of the student
        :return Dictionary mapping from the criteria name in database to its key function used for sorting
        """

        def get_section(student_skill):
            return student_skill.skill.section.name

        def get_time(student_skill):
            return student_skill.skill.estimated_time_to_master

        skills_depth_map = {}
        for target in targets:
            LearningTrack._set_level(target, skills_depth_map, 0)

        def get_level(student_skill):
            return skills_depth_map[student_skill]

        return {'Level': get_level, 'Group': get_section, 'Time': get_time}

    @staticmethod
    def _set_level(student_skill, skills_depth_map, level):
        """
        Fill recursively the skill levels map with values for the student skill and its prerequisites.
        The level of a prerequisite is the level of the skill plus one.
        If the level of the skill is already superior to the level parameter, this function will not have any effect.

        :param student_skill: a StudentSkill
        :param skills_depth_map: Map for the level criteria
        :param level: The level of student_skill
        :return: void
        """

        if student_skill is None or type(student_skill) is not StudentSkill \
                or skills_depth_map is None or type(skills_depth_map) is not dict \
                or level is None  or type(level) is not numbers.Number:
            raise TypeError
        if level < 0:
            raise ValueError

        LearningTrack._set_skill_depth(student_skill, level, skills_depth_map)
        for prerequisite_skill in student_skill.skill.get_prerequisites_skills():
            prerequisite_student_skill = StudentSkill.objects.filter(skill=prerequisite_skill)[0]
            LearningTrack._set_level(prerequisite_student_skill, skills_depth_map, level + 1)

    @staticmethod
    def _set_skill_depth(student_skill, depth, skills_depth_map):
        """
        Method to put the max skill depth in the dictionary if there are several values
        :param student_skill: The skill to update in the dictionary
        :param depth: The depth of the skill
        :param skills_depth_map:Dictionary(skill,depth)
        :return:void
        """
        if student_skill is None or type(student_skill) is not StudentSkill \
                or skills_depth_map is None or type(skills_depth_map) is not dict \
                or depth is None  or type(depth) is not numbers.Number:
            raise TypeError
        if depth < 0:
            raise ValueError

        if student_skill not in skills_depth_map:
            skills_depth_map[student_skill] = depth
        elif skills_depth_map[student_skill] < depth:
            skills_depth_map[student_skill] = depth


class Criteria(models.Model):
    """[FR] Critère

        A criteria is a value taken into account for the ordering of the Learning Track

    """
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class ProfessorCriteria(models.Model):
    """
    The order to "walk" on the learning track
    """

    professor = models.ForeignKey('users.Professor', null=True, default=None, blank=True)

    criteria = models.ForeignKey('Criteria')

    order = models.PositiveIntegerField()

    def __unicode__(self):
        if self.professor:
            return str(self.professor) + " - " + str(self.order) + " : " + self.criteria.name

        return "All - " + str(self.order) + " : " + self.criteria.name


