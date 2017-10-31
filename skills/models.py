# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from examinations.models import Context
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

    """

    student = models.ForeignKey('users.Student')
    """The Student concerned by this LT"""

    student_skill = models.ForeignKey('StudentSkill')

    order = models.PositiveIntegerField()
    """Order of the skill in the learning track"""

    locked = models.BooleanField(default=False)
    """Whether the LT is locked or not"""

    cleared = models.BooleanField(default=False)
    """Whether the LT is cleared or not"""

    def new_learning_track(self,student, professor):
        """
        Create a new learning track for student based on the criteria of professor
        :param student:the student who owns the learning track
        :param professor:the teacher who has specified the targets skills for student
        :return: void
        """
        targets = StudentSkill.objects.filter(student=student, is_target=True)
        criteria_maps, skills_list  = self.get_criteria_maps(targets)
        ordered_criteria = ProfessorCriteria.objects.filter(professor=professor).order_by('order')

        self.sorting(ordered_criteria,criteria_maps,skills_list)

    def sorting(self, ordered_criteria, criteria_maps, skills_list):
        """
        Sort skills_list to return the learning track
        :param ordered_criteria: list of criteria ordered by importance
        :param criteria_maps:Dictionary(criteria, dictionary(skill,value based on the criteria))
        :param skills_list:List of all the skills to be ordered
        :return: the learning track
        """

        #Doit encore être optimiser pour ne pas être statique.
        learning_track = []
        map1 = criteria_maps[ordered_criteria[0].name]
        map2 = criteria_maps[ordered_criteria[1].name]
        map3 = criteria_maps[ordered_criteria[1].name]
        list_c1 = list(skills_list)

        sorted(list_c1, key=lambda x:  map1[x])
        for list_c2 in self.split(skills_list,map1).values():
            sorted(list_c2, key=lambda x: map2[x])
            for list_c3 in self.split(list_c2,map2).values():
                sorted(list_c3, key=lambda x: map3[x])
                for list_c4 in self.split(list_c3,map3).values():
                    self.add_to_learning_track(list_c4,learning_track,skills_list)

        return learning_track

    def add_to_learning_track(self,skills,learning_track,skills_list):
        """
        Add a skill to learning track and check if there are prerequisites to add before.
        :param skills: one or several skills have the same importance
        :param learning_track:the ordered list of skills
        :param skills_list:the list of skill to be ordered
        :return: void
        """
        lifo_queue = []
        for skill in skills:
            if skill not in learning_track :
                fifo_queue = [skill]
                lifo_queue.append(skill)
                for prereq in fifo_queue.pop(0).get_prerequisites_skills():
                    fifo_queue.append(prereq)
                    if prereq in skills_list and prereq not in learning_track and prereq not in lifo_queue:
                        lifo_queue.append(prereq)
        while lifo_queue:
            learning_track.append(lifo_queue.pop())


    def split(self, skills_list, order_map):
        """
        Split skills list to have list of skills with the same value in order_map
        :param skills_list: A list of skills
        :param order_map: Dictionary(value used for the ordering, )
        :return: Dictionary(value used for the ordering, list of skills)
        """
        map = {}
        for skill in skills_list:
            val = order_map[skill]
            if map[val] is None:
                map[val] = [skill]
            else:
                map[val].append(skill)
        return map

    def get_criteria_maps(self,targets):
        """
        Get all the dictionaries used for the sorting by criteria
        :param targets:Targeted skills of a student
        :return:Dictionary(name of a criteria, dictionary(skill,value for the criteria))
        """
        skills_depth_map = {}
        skills_section_map = {}
        skills_set = set()

        for target in targets:
            self.set_criteria_maps(target, skills_depth_map, skills_section_map, skills_set)

        criteria_map = {}
        criteria_map['level'] = skills_depth_map
        criteria_map['section'] = skills_section_map

        return criteria_map,list(skills_set)

    def set_criteria_maps(self, root, skills_depth_map, skills_section_map, skills_set):
        """
        Fill the criteria maps
        :param root: a root node of the prerequisites tree
        :param skills_depth_map: Map for the level criteria
        :param skills_section_map: Map for the section criteria
        :param skills_set: Set of skills
        :return: void
        """

        fifo_queue = [root]
        self.set_skill_depth(root, 0, skills_depth_map)
        self.add_section_skill(root, skills_section_map)
        for prereq in fifo_queue.pop(0).get_prerequisites_skills():
            fifo_queue.append(prereq)
            skills_set.add(prereq)
            self.set_skill_depth(prereq, 0, skills_depth_map)
            self.add_section_skill(prereq, skills_section_map)

    def set_skill_depth(self, student_skill, depth, skills_depth_map):
        """
        Method to put the max skill depth in the dictionary if there are several values
        :param student_skill: The skill to update in the dictionary
        :param depth: The depth of the skill
        :param skills_depth_map:Dictionary(skill,depth)
        :return:void
        """
        if skills_depth_map[student_skill] is None:
            skills_depth_map[student_skill] = depth
        elif skills_depth_map[student_skill] < depth:
            skills_depth_map[student_skill] = depth
        return

    def add_section_skill(self, student_skill, skills_section_map):
        """
        Method to put the section of a skill in the dictionary
        :param student_skill: The skill to update in the dictionary
        :param skills_section_map:Dictionary(skill,section)
        :return:void
        """
        skill = Skill.objects.filter(student_skill)
        section = Section.objects.filter(id=student_skill.id)
        skills_section_map[student_skill] = section
        return

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

        return "all - " + str(self.order) + " : " + self.criteria.name


