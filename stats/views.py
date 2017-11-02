# -*- coding: utf-8 -*-
import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from examinations.models import Context as Question
from promotions.models import Lesson, Stage
from promotions.utils import user_is_professor
from resources.models import KhanAcademy, Sesamath
from skills.models import Skill
from users.models import Professor, Student
from .utils import user_is_superuser, number_of_test_pass, get_latest_test_succeeded, \
    get_number_of_authentication_by_student, get_latest_skill_acquired, time_between_two_last_skills, \
    get_average_skill_acquired, least_mastered_skill, most_mastered_skill


@user_is_professor
def exportCSV(request, pk):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)

    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
    for student in students:
        writer.writerow([student])
    # already prints student names, figure what the method is to get the data which is displayed into the CSV



    return response

@user_is_superuser
def dashboard(request):
    questions_per_stage = []
    for stage in Stage.objects.annotate(Count("skills"), Count("skills__exercice")):
        skills = stage.skills_with_exercice_count()
        questions_per_stage.append({
            "stage": stage,
            "skills_count_with_questions": skills.filter(exercice__count__gt=0),
            # "skills_count_without_questions": skills.filter(exercice__count=0),
        })

    return render(request, "stats/dashboard.haml", {
        "professors": Professor.objects.all(),
        "students": Student.objects.all(),
        "lessons": Lesson.objects.all(),
        "skills": Skill.objects.all(),
        "skills_with_khan_ressources": Skill.objects.annotate(Count('khanacademyvideoskill')).filter(
            khanacademyvideoskill__count__gt=0),
        "skills_with_sesamath_ressources": Skill.objects.annotate(Count('sesamathskill')).filter(
            sesamathskill__count__gt=0),
        "khanacademyvideoskill": KhanAcademy.objects.order_by('-created_at').select_related('skill', 'reference'),
        "sesamathskill": Sesamath.objects.order_by('-created_at').select_related('skill', 'reference'),
        "questions": Question.objects.all().order_by("-modified_at"),
        "stages_with_skills_with_questions": questions_per_stage,
        "skills_with_questions": Skill.objects.annotate(Count('exercice')).filter(exercice__count__gt=0),
    })


def view_student(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)

    return render(request, "stats/student_list.haml", {
        "lesson": lesson,
        "students": students
    })


@user_is_professor
def viewstats(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)

    # TODO: make automatic detection of timespan instead of hard coding
    predefined_timespan = {
        "-----": None,
        "Septembre 2016 - Décembre 2016": "01/09/2016-31/12/2016",
        "Janvier 2017 - Juin 2017": "01/01/2017-31/06/2017",
        "Septembre 2017 - Décembre 2017": "01/09/2017-31/12/2017",

    }

    list_statistics = ['Nombre de connexion', 'Nombre d\'exercice éssayé', 'Temps passé sur les exercice',
                       'Status des exercice', 'Nombre de ressource vue', 'Compétence acquise',
                       'Compétence en progression', 'Test passé', 'Temps passé sur les examens']
    data = [0.7, 0.8, 0.9, 0.8, 0.9, 0.9, 0.9]
    name = [1, 2, 3]  # ["Jean", "Marc", "Georges"]
    size = [18, 2, 42]

    return render(request, "stats/viewstats.haml", {
        "lesson": lesson,
        "student_number": len(Student.objects.filter(lesson=lesson)),
        "avg_skill_acquired": get_average_skill_acquired(lesson, lambda: True),
        "least_mastered_skill": least_mastered_skill(lesson, lambda: True),
        "most_mastered_skill": most_mastered_skill(lesson, lambda: True),
        "data": data,
        "name": name,
        "size": size,
        "most_mastered_skill": most_mastered_skill(lesson, lambda: True),
        "students": students,
        "predefined_timespan": predefined_timespan,
        "list_stats": list_statistics,

    })


def stat_student(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)

    last_test_passed = get_latest_test_succeeded(student, lesson)
    latest_skill = get_latest_skill_acquired(student, lesson)
    time_spent_two_skill = time_between_two_last_skills(student)

    return render(request, "stats/stat_student.haml", {
        "lesson": lesson,
        "student": student,
        "tests_passed": number_of_test_pass(student, lesson),
        "last_passed_test": last_test_passed if last_test_passed else "Aucun test realise!",
        "auth_number": get_number_of_authentication_by_student(student),
        "latest_skill": latest_skill if latest_skill else "Aucun skill encore acquis!",
        "time_spent_two_skills": time_spent_two_skill if time_spent_two_skill else "Pas assez de data pour calculer la statistique"

    })


def stat_student_tab(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)

    return render(request, "stats/stat_student.haml", {
        "lesson": lesson,
        "student": student
    })

