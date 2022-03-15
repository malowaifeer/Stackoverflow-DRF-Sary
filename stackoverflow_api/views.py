from rest_framework.permissions import IsAdminUser
from rest_framework import generics

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from django.contrib.auth.models import User
from stackoverflow.models import Tag, Question, Answer, QuestionComment, AnswerComment
from .serializers import (
    UserSerializer, 
    TagSerializer, 
    QuestionSerializer, 
    AnswerSerializer, 
    QuestionCommentSerializer, 
    AnswerCommentSerializer
)



class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    API to retrieve list of users or create new user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]



class TagListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list of tags or create new tag
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all() 
    permission_classes = [IsAdminUser] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)     



class TagDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete tag
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    


class QuestionListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list of questions or create new question
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class QuestionDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete question
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsOwnerOrReadOnly]



class AnswerListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list of answers for a specific question or create new answer
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        serializer.save(user=self.request.user, question=question)



class AnswerDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete answer
    """
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [IsOwnerOrReadOnly]



class QuestionCommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list comments for a specific question or create new comment
    """
    serializer_class = QuestionCommentSerializer
    queryset = QuestionComment.objects.all()

    def perform_create(self, serializer):
        question = Question.objects.get(id=self.kwargs['pk'])
        serializer.save(user=self.request.user, question=question)



class QuestionCommentDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete question's comment
    """
    serializer_class = QuestionCommentSerializer
    queryset = QuestionComment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]



class AnswerCommentListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve list comments for a specific answer or create new comment
    """
    serializer_class = AnswerCommentSerializer
    queryset = AnswerComment.objects.all()

    def perform_create(self, serializer):
        answer = Answer.objects.get(id=self.kwargs['pk'])
        serializer.save(user=self.request.user, answer=answer)



class AnswerCommentDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete answer's comment
    """
    serializer_class = AnswerCommentSerializer
    queryset = AnswerComment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
