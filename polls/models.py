import datetime
import requests

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def generate_random_choices(self):
        if self.id is None:
            raise ValueError('You have to save your Question before you can generate choices.')
        if self.choice_set.count() > 0:
            raise ValueError('You cannot generate choices on a Question that already has choices.')
        response = requests.get('https://random-data-api.com/api/name/random_name?size=4')
        if self.assertEqual(response.status_code, 200):
            pass
        else:
            RuntimeError('Server is down')
        for name_dict in response.json():
            choice_obj = Choice(question=self, choice_text=name_dict["two_word_name"])
            choice_obj.save()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
