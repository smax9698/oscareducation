import csv
import io
#  from io import StringIO
import zipfile
import StringIO

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from examinations.models import Context as Question
from promotions.models import Stage
from promotions.utils import user_is_professor
from resources.models import KhanAcademy, Sesamath
from skills.models import Skill
from users.models import Professor
import datetime
from datetime import datetime

from stats.utils import *

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


@user_is_professor
def superuser_view_stats(request):
    # TODO: make automatic detection of timespan instead of hard coding
    predefined_timespan = {
        "-----": None,
        "Septembre 2016 - Decembre 2016": "01/09/2016-31/12/2016",
        "Janvier 2017 - Juin 2017": "01/01/2017-30/06/2017",
        "Septembre 2017 - Decembre 2017": "01/09/2017-31/12/2017",

    }

    return render(request, "stats/superuser_view_stats.haml", {

        "predefined_timespan": predefined_timespan,

    })

@user_is_professor
def superuserCSV(request):
    """Downloads a CSV file of the displayed data"""
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename=all_data.zip'

    # get what type of CSV type the user selected
    if request.POST.get("csv_type", None) == "euro":
        csvT = ";"
    else:
        csvT = ","

    # open object to create zip file
    buff = StringIO.StringIO()
    archive = zipfile.ZipFile(buff,'w',zipfile.ZIP_DEFLATED)

    # if statements for each model to check which model was selected for download
    if request.POST.get("loginStats", None) != None:
        file_like_1 = StringIO.StringIO()
        writer1 = csv.writer(file_like_1, delimiter=csvT)
        temp = []
        # if statements to check which type of user was selected to download information from
        if request.POST.get('student', None) != None:
            temp.append('student')
        if request.POST.get('professor', None) != None:
            temp.append('professor')
        if request.POST.get('admin', None) != None:
            temp.append('admin')
        # get date constraints, if no preselected date chosen it will look at the selected date options 
        if request.POST.get("preDefDateLS", None) != 'None': # gets predefined time span
            dateString  = request.POST.get("preDefDateLS", None).split('-')
            startDate = datetime.datetime.strptime(dateString[0], "%d/%m/%Y").date()
            endDate =  datetime.datetime.strptime(dateString[1], "%d/%m/%Y").date()
        else: # gets selected date options
            startDate = request.POST.get("startDateLS", None)
            endDate = request.POST.get("endDateLS", None)

         #will write the information into its own file and append it to the zip file
        for item in get_login_stats_by_professor(startDate,endDate,temp):
            writer1.writerow(item)
        # gets written into its own file
        archive.writestr('loginStats.csv',file_like_1.getvalue())
    if request.POST.get("resStudent", None) != None:
        file_like_1 = StringIO.StringIO()
        writer1 = csv.writer(file_like_1, delimiter=csvT)

        if request.POST.get("preDefDateRS", None) != 'None':
            dateString  = request.POST.get("preDefDateRS", None).split('-')
            startDate = datetime.datetime.strptime(dateString[0], "%d/%m/%Y").date()
            endDate =  datetime.datetime.strptime(dateString[1], "%d/%m/%Y").date()
            
        else:
            startDate = request.POST.get("startDateRS", None)
            endDate = request.POST.get("endDateRS", None)

        for item in get_res_students_by_professor(startDate,endDate):
            writer1.writerow(item)
        archive.writestr('resourcesStudent.csv',file_like_1.getvalue())
    if request.POST.get("authStudent", None) != None:
        file_like_1 = StringIO.StringIO()
        writer1 = csv.writer(file_like_1, delimiter=csvT)
        if request.POST.get("preDefDateAS", None) != 'None':
            dateString  = request.POST.get("preDefDateAS", None).split('-')
            startDate = datetime.datetime.strptime(dateString[0], "%d/%m/%Y").date()
            endDate =  datetime.datetime.strptime(dateString[1], "%d/%m/%Y").date()
            
        else:
            startDate = request.POST.get("startDateAS", None)
            endDate = request.POST.get("endDateAS", None)

        for item in get_auth_students_by_professor(startDate,endDate):
            writer1.writerow(item)
        archive.writestr('authenticationStudents.csv',file_like_1.getvalue())
    if request.POST.get("examStudent", None) != None:
        file_like_1 = StringIO.StringIO()
        writer1 = csv.writer(file_like_1, delimiter=csvT)
        for item in get_exam_students_by_professor():
            writer1.writerow(item)
        archive.writestr('examStudents.csv',file_like_1.getvalue())
    if request.POST.get("examStudentSkill", None) != None:
        file_like_1 = StringIO.StringIO()
        writer1 = csv.writer(file_like_1, delimiter=csvT)
        for item in get_exam_students_skill_by_professor():
            writer1.writerow(item)
        archive.writestr('examStudentSkill.csv',file_like_1.getvalue())

    archive.close()
    buff.flush()
    ret_zip = buff.getvalue()
    buff.close()
    response.write(ret_zip)
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