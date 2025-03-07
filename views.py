from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Recruiter
from .serializers import RecruiterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication




Recruiter = get_user_model()

@csrf_exempt
def recruiter_signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if Recruiter.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        recruiter = Recruiter.objects.create_user(username=username, email=email, password=password, status='AWAITING_APPROVAL')

        # Send email to admin for approval
        send_mail(
            'New Recruiter Signup Request',
            f'A new recruiter ({username}) has signed up and is awaiting approval.',
            settings.EMAIL_HOST_USER,
            ['admin@example.com'],  # Replace with the admin's email
            fail_silently=False,
        )

        return JsonResponse({'message': 'Signup successful, waiting for admin approval'}, status=201)
    
@csrf_exempt
def recruiter_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        recruiter = authenticate(username=username, password=password)

        if recruiter:
            if recruiter.status == 'APPROVED':
                login(request, recruiter)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Account not approved by admin'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        
@login_required
def pending_recruiters(request):
    if not request.user.is_superuser:  # Ensure only admin can view
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    pending = Recruiter.objects.filter(status='AWAITING_APPROVAL')
    recruiters_list = [{'id': r.id, 'username': r.username, 'email': r.email} for r in pending]
    return JsonResponse({'pending_recruiters': recruiters_list})


@csrf_exempt
@login_required
def approve_recruiter(request, recruiter_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    recruiter = get_object_or_404(Recruiter, id=recruiter_id)
    recruiter.status = 'APPROVED'
    recruiter.save()
    return JsonResponse({'message': f'Recruiter {recruiter.username} approved'})

@csrf_exempt
@login_required
def reject_recruiter(request, recruiter_id):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    recruiter = get_object_or_404(Recruiter, id=recruiter_id)
    recruiter.status = 'REJECTED'
    recruiter.save()
    return JsonResponse({'message': f'Recruiter {recruiter.username} rejected'})


class RecruiterSignupView(APIView):
    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)


        recruiter = Recruiter.objects.create_user(username=username, email=email, password=password, status='AWAITING_APPROVAL')

        # Send email to Admin
        send_mail(
            'New Recruiter Signup Request',
            f'A new recruiter {recruiter.username} has signed up. Approve or reject their request.',
            'your_system_email@gmail.com',  # Your system email
            ['nayanamukundan084@gmail.com'],  # Admin email
            fail_silently=False,
        )

        return Response({"message": "Recruiter account created. Awaiting approval."}, status=status.HTTP_201_CREATED)


class ApproveRecruiterView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]  # Only authenticated users (admins) can access

    def post(self, request, recruiter_id):
        recruiter = get_object_or_404(Recruiter, id=recruiter_id)

        if recruiter.status == 'APPROVED':
            return Response({"message": "Recruiter is already approved."}, status=status.HTTP_400_BAD_REQUEST)

        recruiter.status = 'APPROVED'
        recruiter.save()

        # Send approval email to recruiter
        send_mail(
            'Your Recruiter Account is Approved',
            f'Hello {recruiter.username}, your recruiter account has been approved!',
            'nayanamukundan084@gmail.com',  # Admin email (system sender)
            [recruiter.email],  # Recruiter's email
            fail_silently=False,
        )

        return Response({"message": "Recruiter approved successfully."}, status=status.HTTP_200_OK)




class RecruiterLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        if user.status == "AWAITING_APPROVAL":
            return Response({"error": "Account awaiting admin approval"}, status=status.HTTP_403_FORBIDDEN)

        if user.status == "REJECTED":
            return Response({"error": "Account rejected by admin"}, status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})