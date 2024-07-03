from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import ApplicationForm, EditProfileForm, CommentForm
from .models import CandidateProfile, Application

@login_required
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            if Application.objects.filter(candidate=candidate_profile).exists():
                return HttpResponse('Вы уже подали заявку.')
            application = form.save(commit=False)
            application.candidate = CandidateProfile.objects.get(user=request.user)
            application.save()

            # Отправка уведомления по электронной почте
            send_mail(
                subject='',
                message=render_to_string('application_notification_email.html', {'user': request.user}),
                from_email='developerjunior5@gmail.com',
                recipient_list=['hello@reviro.io']
            )
            return redirect('application_confirmation')
    else:
        form = ApplicationForm()
    return render(request, 'submit_application.html', {'form': form})


def application_confirmation(request):
    return render(request, 'confirmation.html')


@login_required
def view_candidates(request):
    candidates = CandidateProfile.objects.all()
    return render(request, 'candidate_list.html', {'candidates': candidates})


@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    applications = Application.objects.filter(candidate=candidate)
    return render(request, 'candidate_detail.html', {'candidate': candidate, 'applications': applications})

@login_required
def edit_profile(request):
    profile = CandidateProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse('Изменения в профиле внесены успешно.')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})



@login_required
def view_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    comments = application.comments_author.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            comment.application = application
            comment.author = candidate_profile
            comment.save()
            return redirect('view_application', application_id=application_id)
    else:
        form = CommentForm()
    return render(request, 'view_application.html', {'application': application, 'comments': comments, 'form': form})

