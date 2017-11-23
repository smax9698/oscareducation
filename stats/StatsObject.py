import json
from datetime import timedelta

from examinations.models import BaseTest, TestStudent
from models import ResourceStudent, AuthenticationStudent, ExamStudent, ExamStudentSkill
from skills.models import StudentSkill, Skill, CodeR
from users.models import Student


def get_all_uaa_for_lesson(lesson):
    """
    Retains all the UAA of the lesson gave at parameter
    :param lesson: the Lesson object
    :return: A list of UAA related to this lesson
    """
    stage_for_this_lesson = lesson.stage

    uaa_list = []

    for uaa in CodeR.objects.filter(skill__in=stage_for_this_lesson.skills.all().distinct()).distinct('section'):
        uaa_list.append(uaa.section)

    return uaa_list


def get_skills_for_uaa(uaa):
    skills = {}

    for cr in CodeR.objects.filter(section=uaa):
        for skill in cr.skill.all():
            if skill.pk not in skills:
                skills[skill.pk] = skill

    return list(skills.values())


def get_stat_for_student(student, lesson, current_uaa):
    """
    Retrieve statistics about skills for a specific lesson depending of a specific UAA

    :param student: Student for which we take the data
    :param lesson: Lesson of the student
    :param current_uaa: Current UAA of the year for this lesson
    :return: JSON formatted data
    """
    uaa_skills = get_skills_for_uaa(current_uaa) if current_uaa is not None else None

    def intersection(tested_skills, section_skills):
        if section_skills is None:
            return tested_skills

        return list(set(tested_skills).intersection(section_skills))


    tests_lesson = BaseTest.objects.filter(lesson=lesson)
    tests = TestStudent.objects.filter(student=student, test__in=tests_lesson)
    data = {'data': [], 'xaxis': []}
    total_skill_tested = 0
    number_skill_acquired = 0
    for test in tests:
        skill_tested = intersection(test.test.skills.all(), uaa_skills)
        total_skill_tested += len(skill_tested)
        skills_acquired = StudentSkill.objects.filter(student=student, skill__in=skill_tested, acquired__isnull=False)
        for skill in skills_acquired:
            if skill.acquired and test.finished_at and skill.acquired - test.finished_at <= timedelta(days=1):
                number_skill_acquired += 1
        data['data'].append(
            {'acquired': number_skill_acquired, 'not-acquired': total_skill_tested - number_skill_acquired})
        data['xaxis'].append(test.test.name)

    data['student'] = {}

    data['student']['first_name'] = student.user.first_name
    data['student']['last_name'] = student.user.last_name
    data['student']['email'] = student.user.email

    return json.JSONEncoder().encode(data)


class StatisticStudent(object):
    """
    Abstract class that represent a statistic for a student. Should be subclassed and never instantiate.
    """

    def __init__(self, student):
        """

        :param student: the student on which the statistic applies.
        """
        self.student = student
        self.db_query()

    def db_query(self):
        """
        This method is responsible for the interaction with the database, more precisely getting the data from it.

        :return: nothing. Set the instance variables.
        """
        raise NotImplementedError("This method is not implemented but should be.")


class StatisticClass(object):
    """
    Abstract class that represent a statistic for a class. Should be subclassed and never instantiate.
    """

    def __init__(self, lesson):
        """

        :param lesson: lesson on which the statistic applies
        """
        self.lesson = lesson
        self.db_query()

    def db_query(self):
        """
        This method is reponsible for the interaction with the database. Same as in :class`StatisticStudent`

        :return: nothing. Set the instance variables.
        """
        raise NotImplementedError("This method is not implemented but should be.")


########################
# Statistic of student #
########################


class NumberOfLogin(StatisticStudent):
    """
    Statistic representing the number of login of the user.
    """

    def __init__(self, student):
        super(NumberOfLogin, self).__init__(student)

    def db_query(self):
        query = AuthenticationStudent.objects.filter(student=self.student).order_by('date_accessed')
        data = {}
        sum_data = 0
        for answer in query:
            date = answer.date_accessed.strftime('%b %Y')
            if date not in data:
                data[date] = sum_data
            else:
                sum_data += 1
                data[date] += 1
        self.data = data

    def __unicode__(self):
        return "Nombre de connection"


class ExerciseNumberAttempt(StatisticStudent):
    """
    Statistic representing the number of exercises attempted by the student.
    """

    # TODO: need module from other group
    def __init__(self, student):
        super(ExerciseNumberAttempt, self).__init__(student)

    def db_query(self):
        return None

    def __unicode__(self):
        return "Nombre d'exercice essayer"


class ExerciseTimeSpent(StatisticStudent):
    """
    Statistic representing the time spent on a exercise by the student.
    """

    # TODO: need module from other group
    def __init__(self, student):
        super(ExerciseTimeSpent, self).__init__(student)

    def db_query(self):
        return None

    def __unicode__(self):
        return "Temps passe sur les exercices"


class ExerciseStatus(StatisticStudent):
    """
    Statistic representing the status of an exercise.
    """

    # TODO: need module from other group
    def __init__(self, student):
        super(ExerciseStatus, self).__init__(student)

    def db_query(self):
        return None

    def __unicode__(self):
        return "Status des exercices"


class ResourcesViewed(StatisticStudent):
    """
    Statistic representing the number of time resources has been view by the student.
    """

    def __init__(self, student):
        super(ResourcesViewed, self).__init__(student)

    def db_query(self):
        query = ResourceStudent.objects.filter(student=self.student)
        data = {}
        for item in query:
            if item.resource in data:
                data[str(item.resource)] += 1
            else:
                data[str(item.resource)] = 1
        self.data = data

    def __unicode__(self):
        return "Nombre de ressources accedees"


class SkillOfStudent(StatisticStudent):
    """
    Statistic representing all the skill of the student (acquired and in progress)
    """

    def __init__(self, student):
        super(SkillOfStudent, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student)
        data = {}
        for skill in query:
            data[str(skill)] = True if skill.acquired else False
        self.data = data

    def __unicode__(self):
        return "etat des competences de l etudiant"


class TimeBetweenTwoSkills(StatisticStudent):
    """
    Statistics representing the time between two acquired skills"
    """

    def __init__(self, student):
        super(TimeBetweenTwoSkills, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student).distinct().exclude(acquired__isnull=True).order_by(
            'acquired')
        previous_time = None
        data = {}
        for skill in query:
            if previous_time is None:
                data[str(skill.skill).split(' ')[0]] = 0
                previous_time = skill.acquired
            else:
                time_spend = skill.acquired - previous_time
                data[str(skill.skill).split(' ')[0]] = time_spend.days * 24 + (time_spend.seconds / 3600)
                previous_time = skill.acquired
        self.data = data

    def __unicode__(self):
        return "Temps entre deux completion de competence"


class ExamsPassed(StatisticStudent):
    """
    Statistic representing the all the test that the student passed.
    """

    def __init__(self, student):
        super(ExamsPassed, self).__init__(student)

    def db_query(self):
        query = ExamStudent.objects.get(student=self.student, succeeded=True)
        data = {}
        for exam in query:
            data[str(exam.exam)] = exam.succeeded
        self.data = data

    def __unicode__(self):
        return "Tests de l etudiant"


class TimeSpentExam(StatisticStudent):
    """
    Statistic representing the time spent on the exams the student did.
    """

    def __init__(self, student):
        self.exams = ExamsPassed(student)
        super(TimeSpentExam, self).__init__(student)

    def db_query(self):
        data = {}
        for exam in self.exams.tests:
            data[str(exam.exam)] = exam.finished_at - exam.started_at
        self.data = data

    def __unicode__(self):
        return "Temps passe sur les tests"


class LatestTestSucceeded(StatisticStudent):
    def __init__(self, student, lesson):
        self.lesson = lesson
        super(LatestTestSucceeded, self).__init__(student)

    def db_query(self):
        """

        :return: Set data to the last succeeded test of the student (or None if there is no test succeeded)
        """
        query = ExamStudent.objects.filter(student=self.student)
        skills = self.lesson.stage.skills.all()
        latest = None
        for i in query:
            skill_tested = ExamStudentSkill.objects.get(skill_student=i)
            if i.succeeded and skill_tested.skill in skills:  # check if skill_tested.skill is ok
                if latest is None:
                    latest = i
                elif latest < i.exam.finished_at:
                    latest = i
        self.data = latest.exam.test if latest is not None else None

    def __unicode__(self):
        return "Dernier test reussi"


class NumberOfTestPass(StatisticStudent):
    def __init__(self, student, lesson):
        self.lesson = lesson
        super(NumberOfTestPass, self).__init__(student)

    def db_query(self):
        count = 0
        query = ExamStudent.objects.filter(student=self.student)
        skills = self.lesson.stage.skills.all()
        for i in query:
            skill_tested = ExamStudentSkill.objects.get(skill_student=i)
            if i.succeeded and skill_tested.skill in skills:  # check if skill_tested.skill is ok
                count += 1
        self.data = count

    def __unicode__(self):
        return "Nombre de tests passe"


class LatestSkillAcquired(StatisticClass):
    def __init__(self, student, lesson):
        self.student = student
        super(LatestSkillAcquired, self).__init__(lesson)

    def db_query(self):
        """

        :return: Set data to the last skill acquired by the student in the lesson
        """
        query = StudentSkill.objects.filter(student=self.student, skill__in=self.lesson.stage.skills.all())
        skills = self.lesson.stage.skills.all()
        max = None
        for i in query:
            if i.skill in skills:
                if i.acquired is not None:
                    if max is None:
                        max = i
                    elif i.acquired > max.acquired:
                        max = i
        self.data = max.skill if max is not None else None

    def __unicode__(self):
        return "Derniere competence acquise"


######################
# Statistic of class #
######################


class AverageSkillAcquired(StatisticClass):
    """
    Statistic representing average skill acquired for a class
    """

    def __init__(self, lesson):
        super(AverageSkillAcquired, self).__init__(lesson)

    def db_query(self):
        """

        :return: set the data to a dictionary of the form {"Month year" : average}
        """
        skills = Skill.objects.filter(stage=self.lesson.stage)
        students = Student.objects.filter(lesson=self.lesson).distinct()

        if len(students) <= 0:
            self.data = None
        else:
            students_skills = StudentSkill.objects.filter(student__in=students, skill__in=skills).exclude(
                acquired__isnull=True).order_by('acquired').distinct()
            sum_skill = 0
            data = {}

            for skill in students_skills:
                date_skill = skill.acquired.strftime('%b %Y')
                if date_skill not in data:
                    data[date_skill] = sum_skill
                else:
                    sum_skill += 1
                    data[date_skill] = sum_skill
            for keys in data:
                data[keys] /= len(students)
            self.data = data

    def __unicode__(self):
        return "Nombre de competences moyenne acquises"


class LeastMasteredSkill(StatisticClass):
    def __init__(self, lesson):
        super(LeastMasteredSkill, self).__init__(lesson)

    def db_query(self):
        """

        :return: set data to the least mastered skill by the students of the lesson
        """

        skills = self.lesson.stage.skills.all()
        students = self.lesson.students.all()
        min_skill = None
        min = None

        for i in skills:

            len_skills_student = len(
                StudentSkill.objects.filter(skill=i, student__in=students).exclude(acquired__isnull=True))

            if len_skills_student > 0 and (min is None or min > len_skills_student):
                min = len_skills_student
                min_skill = i

        self.data = min_skill

    def __unicode__(self):
        return "Competence la moins maitrisee"


class MostMasteredSkill(StatisticClass):
    def __init__(self, lesson):
        super(MostMasteredSkill, self).__init__(lesson)

    def db_query(self):
        """

        :return: Set data to the most mastered skill
        """
        skills = self.lesson.stage.skills.all()
        students = self.lesson.students.all()
        max_skill = None
        max_len = None

        for i in skills:

            len_skills_student = len(
                StudentSkill.objects.filter(skill=i, student__in=students).exclude(acquired__isnull=True))

            if len_skills_student > 0 and (max_len is None or max_len < len_skills_student):
                max_len = len_skills_student
                max_skill = i

        self.data = max_skill

    def __unicode__(self):
        return "Competence la plus maitrisee"
