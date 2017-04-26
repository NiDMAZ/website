from django.shortcuts import render
from .read_madrasa_db import GDriveMadrasaDatabase
# Create your views here.

g_drive_db = GDriveMadrasaDatabase()

def homepage(request):

    page_context = { 'info' :  g_drive_db.get_students_infos([8000, 8011])}

    return render(request, 'madrasa/homepage.html', page_context)