from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tag(models.Model):
    """
    Tag Model
    To link every question with at least one tag
    """
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Question(models.Model):
    """
    Question Model
    Contains Stackoverflow questions and attributes
    """
    title = models.CharField(max_length=300, blank=False)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='questions', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title



class Answer(models.Model):
    """
    Answer Model
    Contains Stackoverflow answers for each question
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.content



class BaseComment(models.Model):
    """
    Abstract Model
    To define the bases of every question/answer comment
    """
    published = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.comment



class QuestionComment(BaseComment):
    """
    Question Comment Model
    Contains the comments for each question
    """
    comment = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')



class AnswerComment(BaseComment):
    """
    Answer Comment Model
    Contains the comments for each Answer
    """
    comment = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='comments')