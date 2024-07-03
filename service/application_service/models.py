from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=True)
    last_name = models.CharField(max_length=255, blank=False, null=True)
    education = models.TextField(verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт работы')
    photo = models.ImageField(upload_to='candidate_photos/', blank=True, null=True, verbose_name='Фото')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        verbose_name = 'Профиль'

    def __str__(self):
        return self.user.name
    
      
    @property
    def imageUrl(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url  


class Application(models.Model):
    #STATUS_CHOICES = [
    #    ('submitted', 'Submitted'),
    #    ('under_review', 'Under Review'),
    #    ('accepted', 'Accepted'),
    #    ('rejected', 'Rejected')
    #]
    POSITION_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('mobile dev', 'Mobile dev'),
        ('devops', 'Devops'),
        ('qa', 'QA'),
        ('project manager', 'Project Manager')
    ]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, verbose_name='Кандидат')
    resume = models.FileField(upload_to='resumes/', verbose_name='Резюме', blank=False)
    cover_letter = models.TextField(blank=False, null=True, verbose_name='Сопроводительное письмо')
    #status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    comments = models.TextField(blank=True, null=True, verbose_name='Комментарии')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=False, null=True, verbose_name='Позиция кандидата')
    date_submitted = models.DateTimeField(auto_now_add=True)
    interview_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата собеседовании')
    feedback = models.TextField(blank=False, null=True, verbose_name='Фидбэк')
    rating = models.IntegerField(blank=False, null=True, verbose_name='Рейтинг')
    portfolio_link = models.URLField(blank=False, null=True, verbose_name='Ссылка на портфолио')
    github_profile = models.URLField(blank=False, null=True, verbose_name='Ссылка на гитхаб')

    def __str__(self):
        return self.candidate.name


class Comment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments_author')
    author = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.application}'