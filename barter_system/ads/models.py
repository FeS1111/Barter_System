from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    conditions = [
        ('New', 'Новый'),
        ('Used', 'Б/У')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=conditions)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    statuses = [
        ('Pending', 'Ожидает'),
        ('Accepted', 'Принята'),
        ('Declined', 'Отклонена')
    ]
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=statuses, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} -> {self.ad_receiver} ({self.status})"
