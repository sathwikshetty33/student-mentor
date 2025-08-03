from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    leetcode = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    dateJoined = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    def __str__(self):
        return f'{self.user.username}'
    
class MentorProfile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)
    github = models.CharField(max_length=100)
    dateJoined = models.DateTimeField(auto_now_add=True)
    photo = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    def __str__(self):
        return f'{self.user.username}'
class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'

class TestScore(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.student.user.username} - {self.test.name} - {self.score}'
    
    class Meta:
        verbose_name = 'Test Score'
        verbose_name_plural = 'Test Scores'