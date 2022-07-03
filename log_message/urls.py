from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_view),
    path('add/', views.add_note),
    path('look/<int:noteid>', views.note_look),
    path('del_note/<int:noteid>', views.del_note),
    path('update_note/<int:noteid>', views.update_note),
]