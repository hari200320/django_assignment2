from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import StudentForm
from .models import Student
import csv
from reportlab.pdfgen import canvas

# View for student registration
def student_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = StudentForm()
    return render(request, 'enrollment/registration.html', {'form': form})

# View to export students to CSV
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Enrolled Date'])

    students = Student.objects.all()
    for student in students:
        writer.writerow([student.first_name, student.last_name, student.email, student.enrolled_date])

    return response

# View to export students to PDF
def export_students_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Student Enrollment List")
    p.drawString(100, 735, "=======================")

    students = Student.objects.all()
    y = 700
    for student in students:
        p.drawString(100, y, f"{student.first_name} {student.last_name} ({student.email})")
        y -= 15

    p.showPage()
    p.save()
    return response