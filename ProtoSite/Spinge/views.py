
# Create your views here.

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Note, Profile, Course, Enrollment
from .forms import NoteForm, CourseForm
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

# Create your views here.


def user_only(user):
    return user.is_authenticated


def professor_only(user):
    return user.is_authenticated and user.profile.is_professor


def student_only(user):
    return user.is_authenticated and user.profile.is_student


@user_passes_test(user_only, login_url="/")
def index_view(request):
    return render(request, 'spinge/index.html', {'user': request.user})


@user_passes_test(professor_only, login_url="/")
def add_note(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    id1 = request.GET.get('id', None)
    if id1 is not None:
        note = get_object_or_404(Note, pk=id1)
    else:
        note = None

    if request.method == 'POST':
        check = 0
        if request.POST.get('control') == 'delete':
            note.delete()
            messages.add_message(request, messages.INFO, 'Note Deleted!')
            return render(request, 'spinge/course_detail.html', {'course': course, 'user': user, 'check': check})

        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.course = course
            note.save()
            messages.add_message(request, messages.INFO, 'Note Added!')
            return render(request, 'spinge/course_detail.html', {'course': course, 'user': user, 'check': check})

    else:
        form = NoteForm(instance=note)

    return render(request, 'spinge/addnote.html', {'form': form, 'note': note})


@user_passes_test(professor_only, login_url="/")
def addcourse(request):
    user = request.user
    id2 = request.GET.get('id', None)
    if id2 is not None:
        course = get_object_or_404(Course, id=id2, owner=user)
    else:
        course = None

    if request.method == 'POST':
        if request.POST.get('control') == 'delete':
            course.delete()
            messages.add_message(request, messages.INFO, 'Course Deleted!')
            return HttpResponseRedirect(reverse('spinge:index'))

        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = user
            course.save()
            messages.add_message(request, messages.INFO, 'Course Added!')
            return HttpResponseRedirect(reverse('spinge:index'))

    else:
        form = CourseForm(instance=course)

    return render(request, 'spinge/addcourse.html', {'form': form, 'course': course})


@user_passes_test(user_only, login_url="/")
def courses_view(request):
    user = request.user;
    courses = Course.objects.order_by('-timestamp')
    return render(request, 'spinge/allcourses.html', {'courses': courses, 'user': user})


@user_passes_test(user_only, login_url="/")
def user_view(request):
    user = request.user
    check = 0

    if user.profile.is_professor:
        check = 1
        courses = Course.objects.filter(owner=user)
    elif user.profile.is_student:
        check = 2
        courses = Course.objects.filter(students=user)

    orderedcourses = courses.order_by('-timestamp')
    return render(request, 'spinge/mycourses.html', {'courses': orderedcourses, 'check': check})


@user_passes_test(user_only, login_url="/")
def course_detail(request, course_id):
    user = request.user
    check = 0
    course = get_object_or_404(Course, pk=course_id)
    if Course.objects.filter(students=user, pk=course_id).exists():
        check = 1
    return render(request, 'spinge/course_detail.html', {'course': course, 'user': user, 'check': check})


@user_passes_test(user_only, login_url="/")
def notes_view(request, course_id):
    user = request.user
    check = 0
    course = get_object_or_404(Course, pk=course_id)
    if course.owner == user:
        notes = Note.objects.filter(course=course)
        check = 1
    else:
        enroll_set = Enrollment.objects.filter(course=course, student=user)
        limit = datetime.now()
        for enroll in enroll_set:
            limit = enroll.enrollmentTime
        notes = Note.objects.filter(timestamp__range=(limit, datetime.now()), course=course)
    return render(request, 'spinge/notes_view.html', {'course': course, 'notes': notes, 'check': check})


@user_passes_test(student_only, login_url="/")
def join_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user == course.owner:
        return render(request, 'spinge/course_detail.html', {'course': course,
                                                             'error_message': "You can't join your own course."})
    elif Course.objects.filter(students=request.user, pk=course_id).exists():
        return render(request, 'spinge/course_detail.html', {'course': course,
                                                             'error_message': "You have already joined this course once."})
    else:
        course.students.add(request.user)
        course.save()
        e = Enrollment(course=course, student=request.user)
        e.save()
        messages.add_message(request, messages.INFO, 'Course Joined Successfully!')
        return render(request, 'spinge/course_detail.html', {'course': course,})

