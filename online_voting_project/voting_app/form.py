from django import forms
from django.db.models import fields
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


from .models import ContestantsDetail, StudentsRegistration


#contestants form
class ContestantDetailsForm(forms.Form):
    class Meta:
        fields = ("ContestantName", "ProgramName", "Level")

    def clean_details(self):
            ContestantName = self.cleaned_data.get("ContestantName")
            ProgramName = self.cleaned_data.get("ProgramName")
            Level = self.cleaned_data.get("Level")

    def clean_ContestantName(self):
            ContestantName = self.cleaned_data.get("ContestantName")

            sql = ContestantsDetail.objects.filter(ContestantName__iexact = ContestantName)
            if sql.exists():
                raise forms.ValidationError("This contestant name exist already.")
            return ContestantName


class RegistrationForm(forms.Form):
    class Meta:
        fields = ("FullName", "IndexNumber", "password", "password2")

    def clean_registrations(self):
            FullName = self.cleaned_data.get("FullName")
            IndexNumber = self.cleaned_data.get("IndexNumber")
            password = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("password2")


    def clean_index_number(self):
            IndexNumber = self.cleaned_data.get("IndexNumber")

            sql = StudentsRegistration.objects.filter(IndexNumber__iexact = IndexNumber)
            if sql.count() > 0:
                raise forms.ValidationError("This user exist already")
            return IndexNumber

        
    def check_password(self):
            password = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("password2")

            if password2 != password:
                raise forms.ValidationError("Password does not match")
            return password2