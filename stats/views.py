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
from .utils import user_is_superuser

from stats.StatsObject import get_class_stat

import json


@user_is_professor
def exportCSV(request, pk):
    """Downloads a CSV file of the displayed data"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    lesson = get_object_or_404(Lesson, pk=pk)
    students = Student.objects.filter(lesson=lesson)
    #stats.ExamsPassed.



    display_type = request.POST.get("csv_type", None)

    if display_type == "euro":
        writer = csv.writer(response, delimiter=";")
    else:
        writer = csv.writer(response)
    writer.writerow([display_type])

    for student in students:
        writer.writerow([student, lesson.name])
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

    data = [0.7, 0.8, 0.9, 0.8, 0.9, 0.9, 0.9]
    name = ["Jean", "Marc", "Georges"]
    size = [18, 2, 42]

    stats = get_class_stat(lesson)
    stats_json = [json.dumps(x) if is_jsonable(x) else x for x in stats]

    return render(request, "stats/viewstats.haml", {
        "stats": stats,
        "lesson": lesson,
        "student_number": len(Student.objects.filter(lesson=lesson)),
        "data": data,
        "name": name,
        "size": size,
        "students": students,
        "predefined_timespan": predefined_timespan,

    })


def stat_student(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)
    """
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
    """


def stat_student_tab(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)

    return render(request, "stats/stat_student.haml", {
        "lesson": lesson,
        "student": student
    })

