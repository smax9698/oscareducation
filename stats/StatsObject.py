from models import ResourceStudent, AuthenticationStudent, ExamStudent
from skills.models import StudentSkill, Skill
from users.models import Student

import datetime

class StatisticStudent:
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


class StatisticClass:
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


class NumberOfLogin(StatisticStudent):
    """
    Statistic representing the number of login of the user.
    """

    def __init__(self, student):
        self.representation = "barchart"
        self.auth = []
        super(NumberOfLogin, self).__init__(student)

    def db_query(self):
        query = AuthenticationStudent.objects.filter(student=self.student)
        self.auth = list(query)


class ExerciseNumberAttempt(StatisticStudent):
    """
    Statistic representing the number of exercises attempted by the student.
    """

    def __init__(self, student):
        self.representation = "barchart"
        super(ExerciseNumberAttempt, self).__init__(student)

    def db_query(self):
        return None


class ExerciseTimeSpent(StatisticStudent):
    """
    Statistic representing the time spent on a exercise by the student.
    """

    def __init__(self, student):
        self.representation = "barchart"
        super(ExerciseTimeSpent, self).__init__(student)

    def db_query(self):
        return None


class ExerciseStatus(StatisticStudent):
    """
    Statistic representing the status of an exercise.
    """

    def __init__(self, student):
        # TODO: change repr to heat map
        self.representation = "piechart"
        super(ExerciseStatus, self).__init__(student)

    def db_query(self):
        return None


class ResourcesViewed(StatisticStudent):
    """
    Statistic representing the number of time resources has been view by the student.
    """

    def __init__(self, student):
        self.representation = "heat map"
        self.accessed_by_resources = {}
        super(ResourcesViewed, self).__init__(student)

    def db_query(self):
        query = ResourceStudent.objects.filter(student=self.student)

        for item in query:
            if item.resource in self.accessed_by_resources:
                self.accessed_by_resources[str(item.resource)] += 1
            else:
                self.accessed_by_resources[str(item.resource)] = 1


class SkillOfStudent(StatisticStudent):
    """
    Statistic representing all the skill of the student (acquired and in progress)
    """
    def __init__(self, student):
        self.representation = "heat map"
        self.skills = []
        super(SkillOfStudent, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student)
        self.skills = list(query)


class TimeBetweenTwoSkills(StatisticStudent):
    """
    Statistics representing the time between two acquired skills"
    """
    def __init__(self, student):
        self.representation = "heat map"
        self.skills = {}
        super(TimeBetweenTwoSkills, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student).exclude(acquired__isnull=True).order_by('acquired')
        previous_time = None
        for skill in query:
            if previous_time is None:
                self.skills[str(skill)] = 0
            else:
                time_spend = skill.acquired - previous_time
                self.skills[str(skill)] = time_spend.days*24*60 + time_spend.minutes


class ExamsPassed(StatisticStudent):
    """
    Statistic representing the all the test that the student passed.
    """

    def __init__(self, student):
        self.representation = "heat map"
        self.tests = []
        super(ExamsPassed, self).__init__(student)

    def db_query(self):
        query = ExamStudent.objects.get(student=self.student, succeeded=True)
        self.tests = list(query)


class TimeSpentExam(StatisticStudent):
    """
    Statistic representing the time spent on the exams the student did.
    """

    def __init__(self, student):
        self.representation = "barchart"
        self.exams = ExamsPassed(self.student)
        self.times = []
        super(TimeSpentExam, self).__init__(student)

    def db_query(self):
        for exam in self.exams.tests:
            self.times.append(exam.finished_at - exam.started_at)


class AverageSkillAcquired(StatisticClass):
    """
    Statistic representing average skill acquired for a class
    """

    def __init__(self, lesson):
        self.representation = "barchart"
        super(AverageSkillAcquired, self).__init__(lesson)

    def db_query(self):
        """

            :return: set the data to a dictionary of the form {"Month year" : average}
        """
        skills = Skill.objects.filter(stage=self.lesson.stage)
        students = Student.objects.filter(lesson=self.lesson).distinct()
        students_skills = StudentSkill.objects.filter(student_in=students, skill_in=skills).exclude(
            acquired__isnull=True).group_by('acquired').distinct()
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

