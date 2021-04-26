from uuid import uuid4
import uuid
from django.http import response
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from .models import User
import uuid





class StatusTest(TestCase):
    
    def test_leaderboard_status(self):
        client = APIClient()
        response = client.get('/leaderboard/', format='json')
        print(response)
        assert response.status_code == 200

    def test_leaderboard_country_status(self):
        client = APIClient()
        response = client.get('/leaderboard/TR', format='json')
        assert response.status_code == 200

        response = client.get('/leaderboard/UK', format='json')
        assert response.status_code == 200

# This is the test in order to check ordered leaderboard
class GetLeaderBoard(TestCase):

    def setUp(self):
        
        self.user_uuid1 = uuid4()
        self.user_uuid2 = uuid4()
        self.user_uuid3 = uuid4()

        User.objects.create(
            user_id=self.user_uuid1,
            display_name='username1',
            iso_code='tr',
            points = 4000,
            rank=20
        )
        User.objects.create(
            user_id=self.user_uuid2,
            display_name='username2',
            iso_code='tr',
            points = 2000,
            rank=20
        )
        User.objects.create(
            user_id=self.user_uuid3,
            display_name='username3',
            iso_code='tr',
            points = 8000,
            rank=20
        )
    def test_get_all_users(self):
        client = APIClient()
        response = client.get('/leaderboard/', format='json')
        assert response.json()[0]['user_id'] == str(self.user_uuid3)
        assert response.json()[1]['user_id'] == str(self.user_uuid1)
        assert response.json()[2]['user_id'] == str(self.user_uuid2)


# This test checks the rankings after submission
class Submission(TestCase):

    def setUp(self):
        
        self.user_uuid1 = uuid4()
        self.user_uuid2 = uuid4()
        self.user_uuid3 = uuid4()
        self.user_uuid4 = uuid4()

        User.objects.create(
            user_id=self.user_uuid1,
            display_name='username1',
            iso_code='TR',
            points = 4000,
            rank=20
        )
        User.objects.create(
            user_id=self.user_uuid2,
            display_name='username2',
            iso_code='TR',
            points = 2000,
            rank=20
        )
        User.objects.create(
            user_id=self.user_uuid3,
            display_name='username3',
            iso_code='TR',
            points = 8000,
            rank=20
        )
        User.objects.create(
            user_id=self.user_uuid4,
            display_name='username4',
            iso_code='TR',
            points = 248,
            rank=20
        )

    def test_get_all_users(self):
        client = APIClient()
        user_info = {
            'score_worth': 4800,
            'user_id': self.user_uuid4
        }
        response = client.post('/submit/score/', user_info, format='json')
        leaderboard_info = client.get('/leaderboard/', format='json')

        print(leaderboard_info.json()[1]['user_id'])
        print(str(self.user_uuid4))
        print(leaderboard_info.json())
        assert leaderboard_info.json()[0]['user_id'] == str(self.user_uuid3)
        assert leaderboard_info.json()[1]['user_id'] == str(self.user_uuid4)
        assert leaderboard_info.json()[2]['user_id'] == str(self.user_uuid1)
        assert leaderboard_info.json()[3]['user_id'] == str(self.user_uuid2)

class UserDataBase(TestCase):

    def setUp(self):
        self.user_uuid = uuid4()
        User.objects.create(
            user_id=self.user_uuid,
            display_name='username1',
            iso_code='TR',
            points = 4000,
            rank=20
        )

    def test_user(self):
        client = APIClient()
        response = client.get('/user/profile/'+str(self.user_uuid), format='json')
        print(response.json())
        print(self.user_uuid)
        assert response.json()['user_id'] == str(self.user_uuid)

        



# Create your tests here.
