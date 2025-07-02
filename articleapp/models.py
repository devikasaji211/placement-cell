from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ArticleProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    firm_name = models.CharField(max_length=100)
    dob = models.DateField()
    sro = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    year_of_commencement = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



# articleapp/models.py

class VacancyPost(models.Model):
    article = models.ForeignKey(User, on_delete=models.CASCADE)
    firm_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    other_branches = models.CharField(max_length=200, blank=True, null=True)
    vacancies = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField(blank=True)
    statutory_audit_rating = models.PositiveSmallIntegerField(default=0)
    internal_audit_rating = models.PositiveSmallIntegerField(default=0)
    direct_tax_rating = models.PositiveSmallIntegerField(default=0)
    gst_rating = models.PositiveSmallIntegerField(default=0)
    compliance_rating = models.PositiveSmallIntegerField(default=0)
    consultancy_rating = models.PositiveSmallIntegerField(default=0)
    other_specialisation = models.CharField(max_length=255, blank=True, null=True)
    other_specialisation_rating = models.PositiveSmallIntegerField(default=0)
    stipend = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    share_contact = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firm_name} - {self.branch}"


