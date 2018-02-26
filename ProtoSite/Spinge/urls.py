from django.conf.urls import url, include
from django.contrib import admin
from .views import index_view, user_view, addcourse, course_detail, add_note, notes_view, courses_view
from .views import join_course

app_name = "spinge"

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^userhome$', user_view, name='user_home'),
    url(r'^addcourse/', addcourse, name='addcourse'),
    url(r'^(?P<course_id>\d+)/$', course_detail, name='course_detail'),
    url(r'^(?P<course_id>\d+)/join/$', join_course, name='join_course'),
    url(r'^(?P<course_id>\d+)/addnote/$', add_note, name='add_note'),
    url(r'^(?P<course_id>\d+)/notes/$', notes_view, name='notes_view'),
    url(r'allcourse$', courses_view, name='courses_view'),
]
