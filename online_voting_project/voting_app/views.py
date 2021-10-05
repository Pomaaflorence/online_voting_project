from django import forms
from django.db import reset_queries
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordContextMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

from .models import ContestantsDetail, StudentsRegistration, VoteVerification
from .form import ContestantDetailsForm

# Begining of funtions to hanldel the administrator operations on the voting app

# admin login
def admin_login_page(request):
    Contestants_list = ContestantsDetail.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        admin = auth.authenticate(username=username, password=password)
        User = get_user_model()
        user = User.objects.filter(username__iexact = username)
        userpassword = User.objects.filter(password__iexact = password)

        queryUsers = User.objects.filter(username__iexact = username)
        if admin is not None:
            return render(request, "add-contestant.html", {"Contestants_list":Contestants_list})
        else:
            return render(request, "admin-page.html", 
            {"queryUsers":queryUsers,
             "user":user,
             "username":username,
             "userpassword":userpassword})
    return render(request, "admin-page.html")

#change admin password
class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success = reverse_lazy("password_change_done")


# function to add a contestant to the voting
@login_required
def add_contestant(request):
    Contestants_list = ContestantsDetail.objects.all()
    if request.method == "POST":
        if request.POST.get("ContestantName") and request.POST.get("ProgramName") and request.POST.get("Level"):
            form = ContestantsDetail()
            form.ContestantName = request.POST.get("ContestantName")
            form.ProgramName = request.POST.get("ProgramName")
            form.Level = request.POST.get("Level")

            Name = form.ContestantName
            if Contestants_list.filter(ContestantName__iexact = Name):
                return render(request, "add-contestant.html", {"Name":Name})

            if not Contestants_list.filter(ContestantName__iexact = Name):
                form.save()
                return render(request, "add-contestant.html", {"Contestants_list":Contestants_list}) 
    return render(request, "add-contestant.html", {"Contestants_list":Contestants_list})


# function to delete a contestant
def delete_contestant(request, id):
    obj = ContestantsDetail.objects.get(id=id)
    obj.delete()
    Contestants_list = ContestantsDetail.objects.all()
    return render(request, "add-contestant.html", {"Contestants_list":Contestants_list})

# deleting all contestants
def delete_all_contestants(request):
    Contestants_list = ContestantsDetail.objects.all()
    Contestants_list.delete()
    return render(request, "add-contestant.html", {"Contestants_list":Contestants_list})

# edit contestants info
def edit_contestants_details(request, id):
    obj = ContestantsDetail.objects.get(id=id)
    contx = {
        "ContestantName":obj.ContestantName,
        "ProgramName":obj.ProgramName,
        "Level":obj.Level,
        "id":obj.id,
    }
    return render(request, "contestant-update.html", context=contx)

# update and save the contestants info
def contestants_update(request, id):
    Contestants_list = ContestantsDetail.objects.all()
    obj = ContestantsDetail(id=id)
    obj.ContestantName = request.POST['ContestantName']
    obj.ProgramName = request.POST['ProgramName']
    obj.Level = request.POST['Level']
    obj.save()
    return render(request, "add-contestant.html", {"Contestants_list":Contestants_list})

# logout the administrator to the login page
def logout_admin(request):
    logout(request)
    return render(request, "admin-page.html")

# end of functions acting on the action of the adminitrator


# begining of functions to work on students who are to vote
def students_registration(request):
    Registered_students = StudentsRegistration.objects.all()
    if request.method == "POST":
        if request.POST.get("FullName") and request.POST.get("IndexNumber") and request.POST.get("password"):
            form = StudentsRegistration()
            form.FullName = request.POST.get("FullName")
            form.IndexNumber = request.POST.get("IndexNumber")
            form.password = request.POST.get("password")
            password2 = request.POST.get("password2")

            Index_number = form.IndexNumber
            if Registered_students.filter(IndexNumber__iexact = Index_number):
                return render(request, "registration.html", {
                    "Registered_students":Registered_students,
                })

            password1 = form.password
            if not Registered_students.filter(IndexNumber__iexact = Index_number):
                if password2 == password1:
                    form.save()
                    return redirect("student-login")
                
                Queryindex = StudentsRegistration.objects.filter(IndexNumber__iexact = Index_number)
                if Queryindex == 1:
                    return render(request, "registration.html", {
                    "Registered_students":Registered_students,
                    })
    return render(request, "registration.html")


def students_login_page(request):
    loginQuery = StudentsRegistration.objects.all()
    if request.method == "POST":
        index_number = request.POST['IndexNumber']
        password = request.POST['password']
        Queryindex = StudentsRegistration.objects.filter(IndexNumber__iexact = index_number)
        QueryPassword = StudentsRegistration.objects.filter(password__exact = password)
        if Queryindex and QueryPassword:
            return redirect("vote")
        return render(request, "student-login.html", {
            "Queryindex":Queryindex,
            "index_number":index_number,
            "QueryPassword":QueryPassword,
            "password":password
            })
    return render(request, "student-login.html",{
        "loginQuery":loginQuery,
        # "QueryPassword":QueryPassword,
    })



#storing all the contestants details in variable in order to access only their names 
All_contestants_list = ContestantsDetail.objects.all()
# a dictionary to hold the counted vote
contestants = dict()


login_required(login_url="student-login")
def vote(request):
    IndexNumber_Query = VoteVerification.objects.all()
    if request.method == "POST":
        if request.POST.get("IndexNumber"):
            form = VoteVerification()
            form.IndexNumber = request.POST.get("IndexNumber")
            form.ContestantName = request.POST.get("ContestantName")
            CandidateName = form.ContestantName
            
            index_number = form.IndexNumber
            Registered_vote = StudentsRegistration.objects.filter(IndexNumber__iexact = index_number).exists()
            list_of_Index = IndexNumber_Query.filter(IndexNumber__iexact = index_number).exists()
            if Registered_vote and list_of_Index:
                return render(request, "vote.html", {
                    "list_of_Index":list_of_Index, 
                    "Registered_vote":Registered_vote
                    })

            if Registered_vote and not list_of_Index:
                form.save()            
                # after capturing the index number of the student who voted count his vote for the candidate they voted for.
                if CandidateName in contestants:
                    # count if the candidate vote exist alreaady
                    contestants[CandidateName] = contestants[CandidateName] + 1
                    return render(request, "rank.html", {"contestants":contestants})
                else:
                    # count as first vote if candidate has no vote
                    contestants[CandidateName] = 1
                    return render(request, "rank.html", {"contestants":contestants})
            return render(request, "rank.html", {
                    "contestants":contestants,
                    "All_contestants_list":All_contestants_list,
                    })
    return render(request, "vote.html", {"All_contestants_list":All_contestants_list})


def ranking(request):
    return render(request, "rank.html",  {
                    "contestants":contestants,
                    "All_contestants_list":All_contestants_list,
                    })