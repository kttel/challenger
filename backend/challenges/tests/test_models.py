from unittest.mock import patch

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from challenges import models


def create_challenge(data, **kwargs):
    return models.Challenge.objects.create(**data, **kwargs)

def create_user():
    return get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123',
    )

def get_challenge_test_data(user):
    return {
            'title': 'Test Challenge',
            'user': user,
            'short_intro': 'Test',
            'description': 'Sample description',
            'days': 14,
    }


class RelatedFunctionsTests(APITestCase):
    """
    Tests for all functions that are used in models of the challenge app.
    """
    @patch('challenges.models.uuid4')
    def test_generate_filename(self, mock_uuid):
        mock_uuid.return_value = 'test_uuid'
        data_expected = (
            ('file123.png', f'test_uuid.png'),
            ('file.file.png', f'test_uuid.png'),
            ('jpegfile.jpeg', f'test_uuid.jpeg'),
        )
        for pair in data_expected:
            result = models.generate_uuid4_filename(pair[0])
            self.assertEqual(result, pair[1])

    @patch('challenges.models.generate_uuid4_filename')
    def test_get_file_path_for_challenges(self, mock_generate_uuid4):
        """
        Test function that generates image file path.
        """
        mock_generate_uuid4.return_value = 'generated.png'
        obj = type('TestClass', (object,), {'TYPE': 'challenges'})()
        filenames = ('testimage1.png', 'MYTESTFILE34.png', 'test.test.png')
        expected_result = 'images/challenges\generated.png'
        for filename in filenames:
            result = models.get_file_path(obj, filename)
            self.assertEqual(result, expected_result)

    @patch('challenges.models.generate_uuid4_filename')
    def test_get_file_path_for_achievements(self, mock_generate_uuid4):
        """
        Test function that generates image file path.
        """
        mock_generate_uuid4.return_value = 'generated.png'
        obj = type('TestClass', (object,), {'TYPE': 'achievements'})()
        filenames = ('testimage1.png', 'MYTESTFILE34.png', 'test.test.png')
        expected_result = 'images/achievements\generated.png'
        for filename in filenames:
            result = models.get_file_path(obj, filename)
            self.assertEqual(result, expected_result)


class ChallengeModelTests(APITestCase):
    """
    Tests related to the Challenge model.
    """
    def setUp(self):
        self.user = create_user()
        self.data = get_challenge_test_data(self.user)

    def test_correct_instance_data(self):
        """
        Test correctness of the created challenge data.
        """
        challenge = create_challenge(self.data)
        self.assertEqual(str(challenge), self.data['title'])
        self.assertEqual(challenge.user, self.user)
        self.assertEqual(challenge.image, challenge.DEFAULT_IMAGE)
        self.assertFalse(challenge.is_active)
        self.assertFalse(challenge.is_moderated)

    def test_toggle_active(self):
        """
        Test for the method of changing "is_active" attribute.
        """
        challenge = create_challenge(self.data)
        challenge.toggle_active()
        self.assertTrue(challenge.is_active)
        challenge.toggle_active()
        self.assertFalse(challenge.is_active)

    def test_moderation(self):
        """
        Test for the moderate method of challenge instance.
        """
        challenge = create_challenge(self.data)
        challenge.moderate()
        self.assertTrue(challenge.is_moderated)

    def test_delete_images(self):
        """
        Test for the deleting existing image and cover with the subsequent
        setting them to default.
        """
        filename = 'test.jpg'
        challenge = create_challenge(self.data, image=filename,
                                     cover=filename)
        self.assertEqual(challenge.image, filename)
        self.assertEqual(challenge.cover, filename)
        challenge.delete_image()
        challenge.delete_cover()
        self.assertEqual(challenge.image, challenge.DEFAULT_IMAGE)
        self.assertEqual(challenge.cover, challenge.DEFAULT_IMAGE)


class AchievementModelTests(APITestCase):
    """
    Tests related to the Achievement model.
    """
    def setUp(self):
        self.user = create_user()
        self.challenge_data = get_challenge_test_data(self.user)
        self.challenge = create_challenge(data=self.challenge_data)
        self.data = {
            'user': self.user,
            'challenge': self.challenge,
            'title': 'Test Achievement',
            'description': 'Sample description',
        }

    def test_correct_instance_data(self):
        """
        Test correctness of the created achievement data.
        """
        achievement = models.Achievement.objects.create(**self.data)
        self.assertEqual(str(achievement), self.data['title'])
        self.assertEqual(achievement.user, self.user)
        self.assertEqual(achievement.icon, achievement.DEFAULT_IMAGE)
        self.assertEqual(achievement.style,
                         models.Achievement.StyleChoices.BRONZE)
        self.assertFalse(achievement.is_available)
        self.assertFalse(achievement.is_moderated)

    def test_toggle_availability(self):
        """
        Test for the method of changing "is_available" attribute.
        """
        achievement = models.Achievement.objects.create(**self.data)
        achievement.toggle_availability()
        self.assertTrue(achievement.is_available)
        achievement.toggle_availability()
        self.assertFalse(achievement.is_available)

    def test_moderation(self):
        """
        Test for the moderate method of achievement instance.
        """
        achievement = models.Achievement.objects.create(**self.data)
        achievement.moderate()
        self.assertTrue(achievement.is_moderated)
