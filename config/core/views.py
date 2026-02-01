from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SenderMailForm
from .models import SenderMail
from django.shortcuts import get_object_or_404
from .models import RecipientMail
from .forms import RecipientMailForm
from .models import SubjectLine
from .forms import SubjectLineForm
from .models import MailBody
from .forms import MailBodyForm
from .models import WarmupControl, MailWarmupLog
import csv
from io import TextIOWrapper
from .forms import CSVUploadForm


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def sender_mails(request):
    mail_id = request.POST.get('mail_id')

    if request.method == 'POST':
        if mail_id:  # EDIT
            mail = get_object_or_404(SenderMail, id=mail_id)
            form = SenderMailForm(request.POST, instance=mail)
        else:  # ADD
            form = SenderMailForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('sender_mails')
    else:
        form = SenderMailForm()

    mails = SenderMail.objects.all().order_by('-created_at')

    return render(request, 'sender_mails.html', {
        'form': form,
        'mails': mails
    })


@login_required
def delete_sender_mail(request, pk):
    mail = get_object_or_404(SenderMail, pk=pk)
    mail.delete()
    return redirect('sender_mails')





@login_required
def recipient_mails(request):
    mail_id = request.POST.get('mail_id')

    if request.method == 'POST':
        if mail_id:  # EDIT
            mail = get_object_or_404(RecipientMail, id=mail_id)
            form = RecipientMailForm(request.POST, instance=mail)
        else:  # ADD
            form = RecipientMailForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('recipient_mails')
    else:
        form = RecipientMailForm()

    mails = RecipientMail.objects.all().order_by('-created_at')

    return render(request, 'recipient_mails.html', {
        'form': form,
        'mails': mails
    })

# @login_required
# def update_recipient_mail(request, pk):
#     mail = get_object_or_404(RecipientMail, pk=pk)

#     if request.method == 'POST':
#         form = RecipientMailForm(request.POST, instance=mail)
#         if form.is_valid():
#             form.save()
#             return redirect('recipient_mails')
#     else:
#         form = RecipientMailForm(instance=mail)

#     mails = RecipientMail.objects.all().order_by('-created_at')

#     return render(request, 'recipient_mails.html', {
#         'form': form,
#         'mails': mails,
#         'edit_mode': True,
#         'mail_id': pk,
#     })


@login_required
def delete_recipient_mail(request, pk):
    mail = get_object_or_404(RecipientMail, pk=pk)
    mail.delete()
    return redirect('recipient_mails')


@login_required
def subject_lines(request):
    subject_id = request.POST.get('subject_id')

    if request.method == 'POST':
        if subject_id:
            subject = get_object_or_404(SubjectLine, id=subject_id)
            form = SubjectLineForm(request.POST, instance=subject)
        else:
            form = SubjectLineForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('subject_lines')
    else:
        form = SubjectLineForm()

    subjects = SubjectLine.objects.all().order_by('-created_at')

    return render(request, 'subject_lines.html', {
        'form': form,
        'subjects': subjects
    })


@login_required
def delete_subject_line(request, pk):
    subject = get_object_or_404(SubjectLine, pk=pk)
    subject.delete()
    return redirect('subject_lines')


@login_required
def mail_bodies(request):
    body_id = request.POST.get('body_id')

    if request.method == 'POST':
        if body_id:
            body_obj = get_object_or_404(MailBody, id=body_id)
            form = MailBodyForm(request.POST, instance=body_obj)
        else:
            form = MailBodyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('mail_bodies')
    else:
        form = MailBodyForm()

    bodies = MailBody.objects.all().order_by('-created_at')

    return render(request, 'mail_bodies.html', {
        'form': form,
        'bodies': bodies
    })


@login_required
def delete_mail_body(request, pk):
    body = get_object_or_404(MailBody, pk=pk)
    body.delete()
    return redirect('mail_bodies')


@login_required
def warmup_control(request):
    control, _ = WarmupControl.objects.get_or_create(id=1)

    if request.method == "POST":
        control.time_gap_seconds = request.POST.get("time_gap")
        control.daily_limit_per_sender = request.POST.get("daily_limit")
        control.is_running = 'start' in request.POST
        control.save()
        return redirect('warmup_control')

    return render(request, 'warmup.html', {'control': control})


@login_required
def warmup_control(request):
    control, _ = WarmupControl.objects.get_or_create(id=1)

    if request.method == "POST":
        control.time_gap_seconds = request.POST.get("time_gap")
        control.daily_limit_per_sender = request.POST.get("daily_limit")
        control.is_running = 'start' in request.POST
        control.save()
        return redirect('warmup_control')

    logs = MailWarmupLog.objects.select_related(
        'sender', 'recipient', 'subject'
    ).order_by('-sent_at')[:100]

    return render(request, 'warmup.html', {
        'control': control,
        'logs': logs
    })


@login_required
def upload_csv(request, type):
    form = CSVUploadForm()

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(
                request.FILES['file'].file,
                encoding='utf-8',
                errors='replace'
            )
            reader = csv.DictReader(csv_file)

            for row in reader:
                if type == 'sender':
                    SenderMail.objects.get_or_create(
                        email=row['email'],
                        defaults={
                            'app_password': row['app_password'],
                            'status': row.get('status', 'active')
                        }
                    )

                elif type == 'recipient':
                    RecipientMail.objects.get_or_create(
                        email=row['email'],
                        defaults={
                            'status': row.get('status', 'active')
                        }
                    )

                elif type == 'subject':
                    SubjectLine.objects.get_or_create(
                        subject=row['subject'],
                        defaults={'status': row.get('status', 'active')}
                    )

                elif type == 'body':
                    MailBody.objects.get_or_create(
                        defaults={
                            'body': row['body'],
                            'status': row.get('status', 'active')
                        }
                    )

            return redirect(f'{type}_mails' if type in ['sender', 'recipient'] else f'{type}_lines')

    return render(request, 'upload_csv.html', {'form': form, 'type': type})