from imp import source_from_cache
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from stackoverflow.models import Question, Answer, Tag, QuestionComment, AnswerComment



class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'questions']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, value: str) -> str:
        return make_password(value)




class TagSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Tag
        fields = ('id', 'name', 'questions', 'owner')



class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'content', 'answers', 'comments', 'published', 'tags', 'user',)



class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    question = serializers.ReadOnlyField(source='question.id')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Answer
        fields = ('id', 'question', 'content', 'comments', 'published', 'user',)



class QuestionCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    question = serializers.ReadOnlyField(source='question.id')

    class Meta:
        model = QuestionComment
        fields = ('id', 'question', 'comment', 'published', 'user')



class AnswerCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    answer = serializers.ReadOnlyField(source='answer.id')
    
    class Meta:
        model = AnswerComment
        fields = ('id', 'answer', 'comment', 'published', 'user')