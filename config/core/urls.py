from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('sender-mails/', sender_mails, name='sender_mails'),
    path('sender-mails/delete/<int:pk>/', delete_sender_mail, name='delete_sender_mail'),
    path('recipient-mails/', recipient_mails, name='recipient_mails'),
    path('recipient-mails/delete/<int:pk>/', delete_recipient_mail, name='delete_recipient_mail'),
    path('subject-lines/', subject_lines, name='subject_lines'),
    path('subject-lines/delete/<int:pk>/', delete_subject_line, name='delete_subject_line'),
    path('mail-bodies/', mail_bodies, name='mail_bodies'),
    path('mail-bodies/delete/<int:pk>/', delete_mail_body, name='delete_mail_body'),
    path('warmup/', warmup_control, name='warmup_control'),
    path('upload/<str:type>/', upload_csv, name='upload_csv'),
]
