from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_content, name="following"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile_page, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("like/<int:post_id>", views.like_post, name="like"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>", views.delete_post, name="delete_post")
]
