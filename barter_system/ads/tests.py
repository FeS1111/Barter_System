from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Иван', password='qwerty')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Продаю велосипед',
            description='Почти новый, ездил мало',
            category='Велосипеды',
            condition='New'
        )

    def test_ad_creation(self):
        self.assertEqual(self.ad.title, 'Продаю велосипед')
        self.assertEqual(self.ad.category, 'Велосипеды')
        self.assertEqual(self.ad.get_condition_display(), 'Новый')
        self.assertEqual(str(self.ad), 'Продаю велосипед')


class ExchangeProposalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='Алексей', password='asdf1234')
        self.user2 = User.objects.create_user(username='Мария', password='zxcv5678')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Смартфон Xiaomi',
            description='Отдам в отличном состоянии',
            category='Электроника',
            condition='Used'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Гитара акустическая',
            description='Практически новая',
            category='Музыка',
            condition='New'
        )
        self.ad3 = Ad.objects.create(
            user=self.user2,
            title='Настольная лампа',
            description='Работает отлично',
            category='Освещение',
            condition='Used'
        )

        self.proposal1 = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Готов обменять смартфон на вашу гитару',
            status='Pending'
        )
        self.proposal2 = ExchangeProposal.objects.create(
            ad_sender=self.ad2,
            ad_receiver=self.ad3,
            comment='Обменяю гитару на лампу',
            status='Accepted'
        )
        self.proposal3 = ExchangeProposal.objects.create(
            ad_sender=self.ad3,
            ad_receiver=self.ad1,
            comment='Лампу на смартфон поменяете?',
            status='Declined'
        )

    def test_proposal_fields(self):
        self.assertEqual(self.proposal1.comment, 'Готов обменять смартфон на вашу гитару')
        self.assertEqual(self.proposal1.status, 'Pending')
        self.assertEqual(self.proposal2.status, 'Accepted')
        self.assertEqual(self.proposal3.status, 'Declined')

    def test_exchange_str(self):
        self.assertIn('Гитара акустическая', str(self.proposal1))
        self.assertIn('Лампу на смартфон поменяете?', self.proposal3.comment)

    def test_ad_relations(self):
        self.assertEqual(self.proposal1.ad_sender.title, 'Смартфон Xiaomi')
        self.assertEqual(self.proposal1.ad_receiver.title, 'Гитара акустическая')
        self.assertEqual(self.proposal2.ad_sender.user.username, 'Мария')
        self.assertEqual(self.proposal3.ad_receiver.user.username, 'Иван' if hasattr(self, 'user') else 'Алексей')

