from email.policy import default
from pyexpat import model
from tkinter import CASCADE
# from turtle import title
# from unicodedata import name
from django.db import models
import uuid
from users.models import Profile

from django.test import tag
# Create your models here.


class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile,null=True, blank=True, on_delete=models.SET_NULL )
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField( max_length=200)
    description = models.TextField(max_length= 2000)
    featured_image = models.ImageField(null=True, blank=True,default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True) #many to many relationship
    vote_total = models.IntegerField(default=0,null=True, blank=True )
    vote_ratio = models.IntegerField(default=0,null=True, blank=True )

    def __str__(self) :
        return self.title



class Review(models.Model):
    VOTE_TYPE = (
            ('up', 'UP'),
            ('down', 'Down'),
        )
    project = models.ForeignKey(Project, on_delete=models.CASCADE) #one to many relationship
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    value = models.TextField(max_length= 2000, choices=VOTE_TYPE)
    body = models.TextField(max_length= 2000, null=True, blank=True)

    def __str__(self) :
        return self.value

    
class Tag(models.Model):
    name = models.CharField( max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
                    