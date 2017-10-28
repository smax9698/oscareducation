class Statistic:
    """
    Abstract class that represent a statistic. Should be subclassed and never instantiate.
    """

    def __init__(self, student):
        """

        :param student: the student on which the statistic applies.
        """
        self.student = student

    def db_query(self):
        """
        This method is responsible for the interaction with the database, more precisely getting the data from it.

        :return: return the data corresponding to the statistic.
        """
        raise NotImplementedError("This method is not implemented but should be.")


class NumberOfLogin(Statistic):
    """
    Statistic representing the number of login of the user.
    """

    def db_query(self):
        return None


class ExerciseNumberAttempt(Statistic):
    """
    Statistic representing the number of exercises attempted by the student.
    """

    def db_query(self):
        return None


class ExerciseTimeSpent(Statistic):
    """
    Statistic representing the time spent on a exercise by the student.
    """

    def db_query(self):
        return None


class ExerciseStatus(Statistic):
    """
    Statistic representing the status of an exercise.
    """

    def db_query(self):
        return None


class ResourcesViewed(Statistic):
    """
    Statistic representing the number of time resources has been view by the student.
    """

    def db_query(self):
        return None


class SkillsAcquired(Statistic):
    """
    Statistic representing all the acquired skill of the student.
    """

    def db_query(self):
        return None


class SkillsInProgress(Statistic):
    """
    Statistic representing all the skill that the student is learning.
    """

    def db_query(self):
        return None


class ExamsPassed(Statistic):
    """
    Statistic representing the all the test that the student passed.
    """

    def db_query(self):
        return None


class TimeSpentExam(Statistic):
    """
    Statistic representing the time spent on the exams the student did.
    """
    
    def db_query(self):
        return None
