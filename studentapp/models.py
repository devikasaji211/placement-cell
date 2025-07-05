from django.db import models
from django.contrib.auth.models import User

from articleapp.models import VacancyPost


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    sro = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)
    orientation_completed = models.BooleanField(default=False)
    itt_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class ReferralRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_requests')
    vacancy = models.ForeignKey(VacancyPost, on_delete=models.CASCADE, related_name='referral_requests')
    message = models.TextField()
    resume = models.URLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral Request by {self.student.username} for {self.vacancy.firm_name}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    vacancy = models.ForeignKey(VacancyPost, null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message}"
    

class Bookmark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(VacancyPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'vacancy')

    def __str__(self):
        return f"{self.student.username} bookmarked {self.vacancy.firm_name} - {self.vacancy.branch}"