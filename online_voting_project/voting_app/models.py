from django.db import models

# Create your models here.

from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import SQLiteNumericMixin

# Create your models here.

class ContestantsDetail(models.Model):
    ContestantName = models.CharField(max_length=80)
    ProgramName = models.CharField(max_length=120)
    Level = models.CharField(max_length=4)

    class Meta:
        db_table = 'contestantsdetails'

    def __str__(self):
        self.ContestantName
        self.ProgramName
        self.Level
        return self.ContestantName

    def clean_contestantname(self):
        ContestantName = self.ContestantName

        sql = ContestantsDetail.objects.filter(ContestantName__iexact = ContestantName)
        if sql.exists():
            return ContestantName


class StudentsRegistration(models.Model):
    FullName = models.CharField(max_length=80)
    IndexNumber = models.CharField(max_length=10)
    password = models.CharField(max_length=8)

    class Meta:
        db_table = 'studentsregistration'

    def __str__(self):
        self.FullName
        self.IndexNumber
        return '{} {}'.format(self.FullName, self.IndexNumber)
    
    def __str__indexnumber(self):
        IndexNumber = self.IndexNumber

        IndexQuery = StudentsRegistration.objects.filter(IndexNumber__iexact = IndexNumber)
        if IndexQuery.count() == 1:
            # index number exist already
            return '{}'.format(IndexNumber)

class VoteVerification(models.Model):
    IndexNumber = models.CharField(max_length=10)
    # ContestantName = models.CharField(max_length=80)
    class Meta:
        db_table = 'votes'

    def __str__(self):
        self.IndexNumber
        return '{}'.format(self.IndexNumber)

    def clean_index(self):
        IndexNumber = self.IndexNumber
        sql = VoteVerification.objects.filter(IndexNumber__iexact = IndexNumber)
        if sql.count() == 1:
            return IndexNumber
