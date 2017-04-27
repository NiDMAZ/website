from django.shortcuts import render
from .read_madrasa_db import GDriveMadrasaDatabase
from .forms import StudentIdsForm, ClassSelectionForm
# Create your views here.

g_drive_db = GDriveMadrasaDatabase()

def homepage(request):
    page_context = {}
    return render(request, 'madrasa/homepage.html', page_context)

def students(request):
    page_context = {
        'page_title': 'Students Information By ID',
        'form': StudentIdsForm(),
        'button_text': 'Search',
        'page_body': 'Enter Student Ids separated by a comma'
    }

    if request.method == "POST":
        post_info = request.POST.dict()
        if post_info.get('student_ids').lower() == 'all':
            html_results = g_drive_db.get_students_infos(student_ids=None)
        else:
            student_ids = [int(i) for i in post_info.get('student_ids').split(',')]
            html_results = g_drive_db.get_students_infos(student_ids)

        page_context['html_results'] = html_results

        return render(request, 'madrasa/result_page.html', page_context)

    return render(request, 'madrasa/request_page.html', page_context)


def madrasa_classes(request):
    page_context = {
        'page_title': 'Students by Class',
        'form': ClassSelectionForm(),
        'button_text': 'Search',
        'page_body': 'Select a class'
    }

    if request.method == "POST":
        post_info = request.POST.dict()
        class_name =post_info.get('madrasa_class')

        html_results = g_drive_db.get_students_by_class(class_name=class_name)
        page_context['html_results'] = html_results

        return render(request, 'madrasa/result_page.html', page_context)

    return render(request, 'madrasa/request_page.html', page_context)

