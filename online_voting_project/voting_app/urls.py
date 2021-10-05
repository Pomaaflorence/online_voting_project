from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from .views import ChangePassword

from . import views


urlpatterns = [
    # admin path
    path('admin-login', views.admin_login_page, name= "admin-page"),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name = "password-change-done.html"), name= "password_change_done"),
    path('password_change/', ChangePassword.as_view(template_name = "change-password.html"), name= "password_change"),
    path('add-new-contestant', views.add_contestant, name= "add-contestant"),
    path('delete/<int:id>', views.delete_contestant, name= "delete"),
    path('delete-all', views.delete_all_contestants, name= "delete-all"),
    path('edit/<int:id>', views.edit_contestants_details, name= "edit-contestant-data"),
    path('update/<int:id>', views.contestants_update, name= "contestants-update"),
    path('logout/', views.logout_admin, name= "logout"),
    # end of admin path
    
    #students template
    path('registration', views.students_registration, name= "registration"),
    path('', views.students_login_page, name="student-login"),
    path('vote', views.vote, name= "vote"),
    path('rank/', views.ranking, name= "rank"),
]