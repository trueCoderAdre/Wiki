from django.urls import path

from . import views
import encyclopedia

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.article, name="article"),
    path("search/", views.search, name="search"),
    path("createnewpage/", views.create_new_page, name="createnewpage"),
    path("rand/", views.rand, name="rand"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit")

]
