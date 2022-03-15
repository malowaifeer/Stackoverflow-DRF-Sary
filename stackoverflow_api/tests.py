from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from stackoverflow.models import (
    Tag,
    Question,
    Answer,
    QuestionComment,
    AnswerComment
)


class TagListCreateAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.url = reverse('stackoverflow_api:api-tag-list')
        self.jwt_url = reverse('token_obtain_pair')

        # Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "admin", "password": "admin"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_list_tag(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_tag(self):
        data = {"name": "django2"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class TagDetailsAPITest(APITestCase):

    def setUp(self) -> None:
        # Setup Data
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.url = reverse('stackoverflow_api:api-tag-details', kwargs={'pk': self.tag.pk})
        self.jwt_url = reverse('token_obtain_pair')

        # Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "admin", "password": "admin"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_get_tag(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_udpate_tag(self):
        data = {"name": "django-updated"}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tag = Tag.objects.get(id=self.tag.pk)
        self.assertEqual(f'{self.tag.name}', data['name'])
    
    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class QuestionListCreateAPITest(APITestCase):

    def setUp(self) -> None:
        # Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.url = reverse('stackoverflow_api:api-question-list')
        self.jwt_url = reverse('token_obtain_pair')

        # Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_list_question(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_question(self):
        data = {"title": "test question title", "content": "test question content", "tags": [self.tag.pk]}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionDetailsAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.url = reverse('stackoverflow_api:api-question-details', kwargs={'pk': self.question.pk})
        self.jwt_url = reverse('token_obtain_pair')

        #Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_get_question(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question(self):
        data = {"title": "test question title updated", "content": "test question content updated", "tags": [self.tag.pk]}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question = Question.objects.get(id=self.question.pk)
        self.assertEqual(f'{self.question.title}', data['title'])
        self.assertEqual(f'{self.question.content}', data['content'])
    
    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class AnswerListCreateAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.url = reverse('stackoverflow_api:api-answer-list', kwargs={'pk': self.question.pk})
        self.jwt_url = reverse('token_obtain_pair')

        #Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_list_answer(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_answer(self):
        data = {"content": "test answer content"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class AnswerDetailsAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.answer = Answer.objects.create(user=self.user, question=self.question, content='test answer')
        self.url = reverse('stackoverflow_api:api-answer-details', kwargs={'pk': self.answer.pk})
        self.jwt_url = reverse('token_obtain_pair')

        #Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_get_answer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_answer(self):
        data = {"content": "test answer content updated"}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.answer = Answer.objects.get(id=self.answer.pk)
        self.assertEqual(f'{self.answer.content}', data['content'])
    
    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class QuestionCommentListCreateAPITest(APITestCase):

    def setUp(self) -> None:
        # Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.url = reverse('stackoverflow_api:api-question-comment-list', kwargs={'pk': self.question.pk})
        self.jwt_url = reverse('token_obtain_pair')

        # Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_list_question_comments(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_question_comment(self):
        data = {"comment": "test question content"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class QuestionCommentDetailsAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.question_comment = QuestionComment.objects.create(user=self.user, question=self.question, comment='test comment')
        self.url = reverse('stackoverflow_api:api-question-comment-details', kwargs={'pk': self.question_comment.pk})
        self.jwt_url = reverse('token_obtain_pair')

        #Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_get_question_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_comment(self):
        data = {"comment": "test comment updated"}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question_comment = QuestionComment.objects.get(id=self.question_comment.pk)
        self.assertEqual(f'{self.question_comment.comment}', data['comment'])
    
    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class AnswerCommentListCreateAPITest(APITestCase):

    def setUp(self) -> None:
        # Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.answer = Answer.objects.create(user=self.user, question=self.question, content='test answer')
        self.url = reverse('stackoverflow_api:api-answer-comment-list', kwargs={'pk': self.answer.pk})
        self.jwt_url = reverse('token_obtain_pair')

        # Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_list_answer_comments(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_answer_comment(self):
        data = {"comment": "test answer content"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AnswerCommentDetailsAPITest(APITestCase):

    def setUp(self) -> None:
        #Setup Data
        self.user = User.objects.create_superuser(username='user', password='user')
        self.tag = Tag.objects.create(name='django', owner=self.user)
        self.question = Question.objects.create(user=self.user, title='test question title', content='test question content')
        self.question.tags.add(self.tag.pk)
        self.answer = Answer.objects.create(user=self.user, question=self.question, content='test answer')
        self.answer_comment = AnswerComment.objects.create(user=self.user, answer=self.answer, comment='test comment')
        self.url = reverse('stackoverflow_api:api-answer-comment-details', kwargs={'pk': self.answer_comment.pk})
        self.jwt_url = reverse('token_obtain_pair')

        #Setup Authorization
        jwt_response = self.client.post(self.jwt_url, {"username": "user", "password": "user"}, format="json")
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        jwt_token = jwt_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')

    def test_get_answer_comment(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_answer_comment(self):
        data = {"comment": "test comment updated"}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.answer_comment = AnswerComment.objects.get(id=self.answer_comment.pk)
        self.assertEqual(f'{self.answer_comment.comment}', data['comment'])
    
    def test_delete_tag(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

