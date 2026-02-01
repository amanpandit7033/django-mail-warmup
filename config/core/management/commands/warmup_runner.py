from django.core.management.base import BaseCommand
from core.models import *
from django.utils import timezone
import time
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Command(BaseCommand):
    help = "Run mail warmup engine"

    def handle(self, *args, **kwargs):
        print("Warmup engine started...")

        while True:
            control = WarmupControl.objects.first()

            if not control or not control.is_running:
                time.sleep(5)
                continue

            today = timezone.now().date()

            senders = SenderMail.objects.filter(status='active')
            available_senders = []

            for s in senders:
                sent_today = MailWarmupLog.objects.filter(
                    sender=s,
                    sent_at__date=today,
                    status='success'
                ).count()

                if sent_today < control.daily_limit_per_sender:
                    available_senders.append(s)

            if not available_senders:
                print("All senders reached daily limit. Waiting for changes...")

                control.is_running = False
                control.save()

                time.sleep(60)
                continue


            sender = random.choice(available_senders)
            recipient = random.choice(list(RecipientMail.objects.filter(status='active')))
            subject = random.choice(list(SubjectLine.objects.filter(status='active')))
            body = random.choice(list(MailBody.objects.filter(status='active')))

            try:
                msg = MIMEMultipart("alternative")
                msg['Subject'] = subject.subject
                msg['From'] = sender.email
                msg['To'] = recipient.email

                # Plain text fallback
                text_part = MIMEText("Warmup email", "plain")

                # HTML from DB (exactly as stored)
                html_part = MIMEText(body.body, "html")

                msg.attach(text_part)
                msg.attach(html_part)       

                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(sender.email, sender.app_password)
                server.send_message(msg)
                server.quit()

                MailWarmupLog.objects.create(
                    sender=sender,
                    recipient=recipient,
                    subject=subject,
                    body=body,
                    status='success'
                )

                print(f"Sent from {sender.email} to {recipient.email}")

            except Exception as e:
                MailWarmupLog.objects.create(
                    sender=sender,
                    recipient=recipient,
                    subject=subject,
                    body=body,
                    status='failed'
                )
                print("Error:", e)

            time.sleep(control.time_gap_seconds)
