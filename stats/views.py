# -*- coding: utf-8 -*-
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from examinations.models import Context as Question
from promotions.models import Lesson, Stage
from promotions.utils import user_is_professor
from resources.models import KhanAcademy, Sesamath
from skills.models import Skill
from users.models import Professor, Student
from .utils import user_is_superuser


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

    return render(request, "stats/viewstats.haml", {
        "lesson": lesson,
        "predefined_timespan": predefined_timespan,
        "list_stats": list_statistics,
    })


def stat_student(request, pk_lesson, pk_student):
    lesson = get_object_or_404(Lesson, pk=pk_lesson)
    student = get_object_or_404(Student, pk=pk_student)

    return render(request, "stats/stat_student.haml", {
        "lesson": lesson,
        "student": student
    })
