from django.urls import path

from . import views


app_name = "wiki"


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_entry_page, name="entry"),
    path("/random", views.get_random_page, name="random"),
    path("/search", views.search_page, name="search"),
    path("/new_page", views.create_new_page, name="new_page"),
    path("/edit_page", views.edit_page, name="edit_page"),
    path("/save_changes", views.save_edited_page, name="save_changes")
]
