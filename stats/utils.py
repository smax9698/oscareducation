from django.contrib.auth.decorators import user_passes_test

import stats.models as models
from promotions.models import Lesson
from skills.models import StudentSkill
from users.models import Student


def user_is_superuser(function):
    return user_passes_test(lambda x: x.is_superuser)(function)


###################
# Access database #
###################

###################
#    Update       #
###################


def add_exam_done_by_student(student, exam_id):
    """
    Each time a student is done with an exam we use this method to add the field in the table ExamStudent

    Keyword arguments:
    student -- the student who passed the exam
    exam_id -- id of the finished exam

    """
    new_entry = models.ExamStudent(student=student, exam=exam_id)
    new_entry.save()


def add_skill_acquired_by_student(student, skill_id):
    """
    Each time a student acquires a skill we use this method to add the field in the table SkillStudent

    Keyword arguments:
    student -- the student who acquired the skill
    skill_id -- id of the mastered skill
    status -- status of the mastering level of the skill (unmastered, in progress, mastered)

    """
    new_entry = models.SkillStudent(student=student, skill=skill_id, progress="mastered")
    new_entry.save()


def add_authentication_by_student(student, end_date):
    """
    Each time a student logs in we use this method to add the field in the table AuthenticationStudent

    Keyword arguments:
    student -- student who logged in
    start_date -- date object in the same form as datetime.datetime, which times the beginning of the session
    end_date -- date object in the same form as datetime.datetime, which times the end of the session

    """
    new_entry = models.AuthenticationStudent(student=student, end_of_session=end_date)
    new_entry.save()


def add_resource_accessed_by_student(student, resource_id):
    """
    Each time a student access to a particular resource we use this method to add the field in the table ResourceStudent

    Keyword arguments:
    student -- student who accessed the resource
    resource_id -- id of the resource
    """
    new_entry = models.ResourceStudent(resource=resource_id, student=student)
    new_entry.save()


###################
#      Get        #
###################


def get_resources_accessed_by_student(student):
    accessed_by_resources = {}

    query = models.ResourceStudent.objects.get(student=student)

    for item in query:
        if item.resource in accessed_by_resources:
            accessed_by_resources[item.resource] += 1
        else:
            accessed_by_resources[item.resource] = 1

    return accessed_by_resources


def get_number_of_authentication_by_student(student):
    query = models.AuthenticationStudent.objects.get(student=student)

    return len(query)


def get_authentication_info_by_student(student):
    return models.AuthenticationStudent.objects.get(student=student)


def get_skill_acquired_by_student(student):
    query = models.SkillStudent.objects.get(student=student)
    return len(query)


def get_number_succeeded_exam_by_student(student):
    query = models.ExamStudent.objects.get(student=student, succeeded=True)

    return len(query)


def get_exam_by_student(student):
    query = models.ExamStudent.objects.get(student=student)
    # TODO find exam_id


def get_time_spent_on_exam(exam):
    """exam : examination.TestStudent"""
    return exam.finished_at - exam.started_at


def get_skill_status(skill_student):
    return skill_student.progress


def get_students_by_professor(professor):
    """
    Returns all students of all classes that the professor have
    :param professor: Professor object
    :return: a list with all students related to a professor
    """
    query = Lesson.objects.filter(professors=professor)
    students_dico = {}

    for item in query:
        students = Student.objects.filter(lesson=item)
        for student in students:
            if str(student) not in students_dico:
                yield student
                students_dico[str(student)] = True


def get_average_skill_acquired(lesson, function):
    """
    Returns the average of skill acquired by students
    :param lesson: Lesson object
    :param function:
    :return: Average of skill acquired by students
    """
    count = 0
    students = Student.objects.filter(lesson=lesson)
    skills = lesson.stage.skills.all()  # skills lesson
    for i in students:
        skills_student = StudentSkill.objects.filter(student=i)
        for j in skills:
            skill = skills_student.get(skill=j)
            if skill.acquired and function(skill):
                count += 1
    return count / len(students)


def get_latest_skill_acquired(student, lesson):
    """
    Return the last skill acquired by the student
    :param student: Student object
    :param lesson: Lesson object
    :return: Return the lastest skill mastered by the student in the lesson
    """
    query = StudentSkill.objects.filter(student=student)
    skills = lesson.stage.skills.all()
    max = None
    for i in query:
        if i.skill in skills:
            if i.acquired is not None:
                if max is None:
                    max = i
                elif i.acquired > max.acquired:
                    max = i
    return max.skill if max is not None else None


def least_mastered_skill(lesson, function):
    """
    Return the least_mastered_skill by the student of the lesson
    :param lesson: Lesson object
    :param function:
    :return: the least mastered skill by the student of the lesson
    """
    students = Student.objects.filter(lesson=lesson)
    skills = lesson.stage.skills.all()
    min_skill = None
    min = None
    count = 0
    for i in skills:
        for j in students:
            skill_student = StudentSkill.objects.get(student=j, skill=i)
            if skill_student.acquired and function(skill_student):
                count += 1
        if min is None and count > 0:
            min = count
            min_skill = i
        elif min < count and count > 0:
            min = count
            min_skill = i
        count = 0
    return min_skill


def most_mastered_skill(lesson, function):
    """
    Return the most_mastered skill by the student of the lesson
    :param lesson: Lesson object
    :return: the most mastered skill by the student of the lesson
    """
    students = Student.objects.filter(lesson=lesson)
    skills = lesson.stage.skills.all()
    max_skill = None
    max = None
    count = 0
    for i in skills:
        for j in students:
            skill_student = StudentSkill.objects.get(student=j, skill=i)
            if skill_student.acquired and function(skill_student):
                count += 1
        if max is None and count > 0:
            max = count
            max_skill = i
        elif max < count and count > 0:
            max = count
            max_skill = i
        count = 0
    return max_skill


def time_between_two_skills(student, skill_a, skill_b):
    """
    Return the time between
    :param student: Student object
    :param skill_a:
    :param skill_b:
    :return: The time between by two skill mastered by the student
    """
    query = StudentSkill.objects.filter(student=student)
    date_a = query.get(skill_a).acquired
    date_b = query.get(skill_b).acquired
    return date_a - date_b


def get_latest_test_succeeded(student, lesson):
    """
    Return the latest test succeeded of a specific student
    :param student:
    :param lesson:
    :return: the latest test succeeded of a specific student in lesson
    """
    query = models.ExamStudent.objects.filter(student=student)
    skills = lesson.stage.skills.all()
    latest = None
    for i in query:
        skill_tested = models.ExamStudentSkill.object.get(skill_student=i)
        if i.succeeded and skill_tested.skill in skills:  # check if skill_tested.skill is ok
            if latest is None:
                latest = i
            elif latest < i.exam.finished_at:
                latest = i
    return latest.exam.test if latest is not None else None


def number_of_test_pass(student, lesson):
    """
    Return the number of test succeeded
    :param student: Student object
    :param lesson: Lesson object
    :return: Number of test succeeded in lesson
    """
    count = 0
    query = models.ExamStudent.objects.filter(student=student)
    skills = lesson.stage.skills.all()
    for i in query:
        skill_tested = models.ExamStudentSkill.object.get(skill_student=i)
        if i.succeeded and skill_tested.skill in skills:  # check if skill_tested.skill is ok
            count += 1
    return count


def filter(date_a, date_b):
    """
    :param date_a:
    :param date_b:
    :return:
    """

    def h(element):
        date = element.acquired
        return date_b >= date >= date_a

    return h
