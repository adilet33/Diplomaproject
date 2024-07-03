from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import CandidateProfileSerializer, CustomTokenObtainPairSerializer, ApplicationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from application_service.models import CandidateProfile, Application

from django.core.mail import send_mail
from django.template.loader import render_to_string

from users.models import User



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CandidateProfile.objects.all()
    serializer_class = CandidateProfileSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user_data = serializer.data['user']
        user = User.objects.get(email=user_data['email'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': user_data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED, headers=headers)


class SubmitApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Not found'}, status=status.HTTP_401_UNAUTHORIZED)
        candidate_profile = CandidateProfile.objects.get(user=request.user)
        if Application.objects.filter(candidate=candidate_profile).exists():
            return Response({'detail': 'You have already submitted.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(candidate=candidate_profile)

            send_mail(
                subject='Новая заявка на стажировку',
                message=render_to_string('application_notification_email.html', {'user': request.user}),
                from_email='developerjunior5@gmail.com',
                recipient_list=['hello@reviro.io']
            )
            
            return Response({'detail': 'Заявка успешно отправлена.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)