from django.db import models
from user_details.models import User

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # admin user
    company_name = models.CharField(max_length=100)
    reviews = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE)  # admin user
    company_profile = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_url = models.CharField(max_length=255)
    cover_letter = models.TextField()
    status = models.CharField(max_length=50)

class Connection(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_sent')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_received')
    status = models.CharField(max_length=50)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
