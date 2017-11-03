# -*- coding: utf-8 -*-
from models import ResourceStudent, AuthenticationStudent, ExamStudent, ExamStudentSkill
from skills.models import StudentSkill, Skill
from users.models import Student

# TODO: find why ExamsPassed(student) throws an error and add TimeSpentExam(student), ExamPassed(student) to the list
def get_student_stat(student, lesson):
    return [NumberOfLogin(student), ResourcesViewed(student), SkillOfStudent(student), TimeBetweenTwoSkills(student),
              LatestTestSucceeded(student, lesson),
            NumberOfTestPass(student, lesson), LatestSkillAcquired(student, lesson)]


def get_class_stat(lesson):
    return [AverageSkillAcquired(lesson), LeastMasteredSkill(lesson), MostMasteredSkill(lesson)]


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
        self.representation = "barchart"
        self.id = self.representation + "-nblog"
        self.xtitle = "date"
        self.ytitle = "Nombre de conncection"
        self.title = "Nombre de connection par mois (cummulatif)"
        super(NumberOfLogin, self).__init__(student)

    def db_query(self):
        query = AuthenticationStudent.objects.filter(student=self.student).order_by('date_accessed')
        data = {}
        sum = 0
        for answer in query:
            date = answer.date_accessed.strftime('%b %Y')
            if date not in data:
                data[date] = sum
            else:
                sum += 1
                data[date] += 1
        xaxis = []
        yaxis = []
        for key in data:
            xaxis.append(key)
            yaxis.append(data[key])
        self.xaxis = xaxis
        self.yaxis = yaxis

    def __str__(self):
        return "Nombre de connection"


class ExerciseNumberAttempt(StatisticStudent):
    """
    Statistic representing the number of exercises attempted by the student.
    """
    # TODO: need module from other group
    def __init__(self, student):
        self.representation = "barchart"
        self.id = self.representation + "-nbExAtt"
        super(ExerciseNumberAttempt, self).__init__(student)

    def db_query(self):
        return None

    def __str__(self):
        return "Nombre d'exercice essayé"


class ExerciseTimeSpent(StatisticStudent):
    """
    Statistic representing the time spent on a exercise by the student.
    """
    # TODO: need module from other group
    def __init__(self, student):
        self.representation = "barchart"
        self.id = self.representation + "-tsEx"
        super(ExerciseTimeSpent, self).__init__(student)

    def db_query(self):
        return None

    def __str__(self):
        return "Temps passé sur les exercices"


class ExerciseStatus(StatisticStudent):
    """
    Statistic representing the status of an exercise.
    """
    # TODO: need module from other group
    def __init__(self, student):
        self.representation = "heat map"
        self.id = self.representation + "-exStatus"
        super(ExerciseStatus, self).__init__(student)

    def db_query(self):
        return None

    def __str__(self):
        return "Status des exercices"


class ResourcesViewed(StatisticStudent):
    """
    Statistic representing the number of time resources has been view by the student.
    """

    def __init__(self, student):
        self.representation = "barchart"
        self.id = self.representation + "-resView"
        self.xtitle = "Ressources"
        self.ytitle = "Nombre de vue"
        self.title = "Nombre de ressource vue"
        super(ResourcesViewed, self).__init__(student)

    def db_query(self):
        query = ResourceStudent.objects.filter(student=self.student)
        data = {}
        for item in query:
            if item.resource in data:
                data[str(item.resource)] += 1
            else:
                data[str(item.resource)] = 1
        xaxis = []
        yaxis = []
        for key in data:
            xaxis.append(key)
            yaxis.append(data[key])
        self.xaxis = xaxis
        self.yaxis = yaxis

    def __str__(self):
        return "Nombre de ressources accédées"


class SkillOfStudent(StatisticStudent):
    """
    Statistic representing all the skill of the student (acquired and in progress)
    """
    def __init__(self, student):
        self.representation = "heat map"
        self.id = self.representation + "-skStu"
        super(SkillOfStudent, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student)
        data = {}
        for skill in query:
            data[str(skill)] = True if skill.acquired else False
        self.data = data

    def __str__(self):
        return "État des compétences de l'étudiant"


class TimeBetweenTwoSkills(StatisticStudent):
    """
    Statistics representing the time between two acquired skills"
    """
    def __init__(self, student):
        self.representation = "barchart"
        self.id = self.representation + "-tsBetSk"
        self.xtitle = "Compétence"
        self.ytitle = "Temps depuis la précédente compétence"
        self.title = r"Temps passé entre l\'acquisition de deux compétence"
        super(TimeBetweenTwoSkills, self).__init__(student)

    def db_query(self):
        query = StudentSkill.objects.filter(student=self.student).distinct().exclude(acquired__isnull=True).order_by('acquired')
        previous_time = None
        data = {}
        for skill in query:
            if previous_time is None:
                data[str(skill.skill).split(' ')[0]] = 0
                previous_time = skill.acquired
            else:
                time_spend = skill.acquired - previous_time
                data[str(skill.skill).split(' ')[0]] = time_spend.days*24 + (time_spend.seconds/3600)
                previous_time = skill.acquired
        xaxis = []
        yaxis = []
        for key in data:
            xaxis.append(key)
            yaxis.append(data[key])

        self.xaxis = xaxis
        self.yaxis = yaxis

    def __str__(self):
        return "Temps entre deux complétion de compétence"


class ExamsPassed(StatisticStudent):
    """
    Statistic representing the all the test that the student passed.
    """

    def __init__(self, student):
        self.representation = "heat map"
        self.id = self.representation + "-nblog"
        super(ExamsPassed, self).__init__(student)

    def db_query(self):

        query = ExamStudent.objects.get(student=self.student, succeeded=True)
        data = {}
        for exam in query:
            data[str(exam.exam)] = exam.succeeded
        self.data = data

    def __str__(self):
        return "Tests de l'étudiant"


class TimeSpentExam(StatisticStudent):
    """
    Statistic representing the time spent on the exams the student did.
    """

    def __init__(self, student):
        self.representation = "barchart"
        self.id = self.representation + "-tsSpentExam"
        self.xtitle = "Test"
        self.ytitle = "Temps"
        self.title = "Temps passé sur les tests"
        self.exams = ExamsPassed(student)
        super(TimeSpentExam, self).__init__(student)

    def db_query(self):
        data = {}
        for exam in self.exams.tests:
            data[str(exam.exam)] = exam.finished_at - exam.started_at
        xaxis = []
        yaxis = []
        for key in data:
            xaxis.append(key)
            yaxis.append(data[key])
        self.xaxis = xaxis
        self.yaxis = yaxis

    def __str__(self):
        return "Temps passé sur les tests"


class LatestTestSucceeded(StatisticStudent):

    def __init__(self, student, lesson):
        self.representation = None
        self.id = "lstTestSucc"
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

    def __str__(self):
        return "Dernier test réussi"


class NumberOfTestPass(StatisticStudent):

    def __init__(self, student, lesson):
        self.representation = None
        self.id = "nbTestPass"
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

    def __str__(self):
        return "Nombre de tests passé"


class LatestSkillAcquired(StatisticClass):

    def __init__(self, student, lesson):
        self.representation = None
        self.id = "lstSkAcqui"
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

    def __str__(self):
        return "Dernière compétence acquise"


######################
# Statistic of class #
######################


class AverageSkillAcquired(StatisticClass):
    """
    Statistic representing average skill acquired for a class
    """

    def __init__(self, lesson):
        self.representation = "barchart"
        self.id = self.representation + "-classAvSkAcqui"
        self.xtitle = "Date"
        self.ytitle = "Moyenne"
        self.title = "Nombre moyen de compétence acquise par chaque étudiant"
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
            xaxis = []
            yaxis = []
            for key in data:
                xaxis.append(key)
                yaxis.append(data[key])
            self.xaxis = xaxis
            self.yaxis = yaxis

    def __str__(self):
        return "Nombre de compétences moyenne acquises"



class LeastMasteredSkill(StatisticClass):

    def __init__(self, lesson):
        self.representation = None
        self.id = "classLeastMastSk"
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

    def __str__(self):
        return "Compétence la moins maîtrisée"


class MostMasteredSkill(StatisticClass):

    def __init__(self, lesson):
        self.representation = None
        self.id = "classMostMastSk"
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

    def __str__(self):
        return "Compétence la plus maîtrisée"

