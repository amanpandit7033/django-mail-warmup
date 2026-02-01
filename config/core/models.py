from django.db import models

class SenderMail(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    email = models.EmailField(unique=True)
    app_password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class RecipientMail(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class SubjectLine(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class MailBody(models.Model):
    body = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]


class WarmupControl(models.Model):
    time_gap_seconds = models.IntegerField(default=60)
    daily_limit_per_sender = models.IntegerField(default=10)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return "Warmup Settings"


class MailWarmupLog(models.Model):
    sender = models.ForeignKey(SenderMail, on_delete=models.CASCADE)
    recipient = models.ForeignKey(RecipientMail, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectLine, on_delete=models.CASCADE)
    body = models.ForeignKey(MailBody, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)