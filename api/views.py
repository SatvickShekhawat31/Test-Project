from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import UserRegisterSerializer, UploadedFileSerializer
from .models import UploadedFile

from rest_framework.exceptions import PermissionDenied

User = get_user_model()


# ✅ Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        print(f"User registered: {user.username}")


# ✅ Login View - Return Token
from rest_framework.authtoken.views import ObtainAuthToken

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id, 'username': token.user.username})


# ✅ Logout View - Delete token
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)


# ✅ Profile View
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "verified": user.verified
        }
        return Response(data)


# ✅ Change Password View
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})


# ✅ Upload File - only ops users
class UploadedFileListCreateView(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'ops':
            raise PermissionDenied("Only ops users can upload files.")

        uploaded_file = self.request.FILES['file']
        allowed_types = [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # docx
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # pptx
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # xlsx
        ]
        if uploaded_file.content_type not in allowed_types:
            raise serializers.ValidationError("Invalid file type. Only pptx, docx, and xlsx allowed.")

        serializer.save(uploader=user)


# ✅ List Files - only client users
class FileListCreateView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'client':
            raise permissions.PermissionDenied("Only client users can view the list.")
        return UploadedFile.objects.all()


# ✅ Delete File - only ops users
class FileDeleteView(generics.DestroyAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'ops':
            raise permissions.PermissionDenied("Only ops users can delete files.")
        instance.delete()


# ✅ Download File - return secure encrypted link (only client users)
class DownloadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.role != 'client':
            return Response({"error": "Only client users can download files."}, status=403)

        try:
            file = UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            return Response({"error": "File not found."}, status=404)

        encrypted_id = urlsafe_base64_encode(force_bytes(file.pk))
        download_link = request.build_absolute_uri(
            reverse('secure-download', kwargs={'encrypted_id': encrypted_id})
        )
        return Response({
            "download-link": download_link,
            "message": "success"
        })


# ✅ Simple home/test view
from rest_framework.decorators import api_view
@api_view(['GET'])
def api_home(request):
    return Response({"message": "API working 🚀"})


from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings

# Secure download link view
class GenerateDownloadLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        if user.role != 'client':
            return Response({"error": "Only client users can generate download links."}, status=403)
        
        # Find file
        uploaded_file = get_object_or_404(UploadedFile, pk=pk)

        # Generate random token
        token = get_random_string(32)

        # Optionally save token somewhere (skip for now)

        # Create download URL (you can make a real download view later)
        download_url = request.build_absolute_uri(
            reverse('download-file', kwargs={'token': token})
        )

        return Response({
            "download-link": download_url,
            "message": "success"
        })

# Actual download view
class DownloadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, token):
        user = request.user
        if user.role != 'client':
            return Response({"error": "Access denied."}, status=403)

        # For demo: just return success (real code would map token → file)
        # You would have to store token:file mapping in DB or cache
        return Response({"message": f"File download allowed for token {token}"})

from itsdangerous import URLSafeSerializer
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class DownloadFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Sirf client user hi download kare
        if request.user.role != 'client':
            return Response({'error': 'Access denied'}, status=403)
        
        serializer = URLSafeSerializer(settings.SECRET_KEY, salt='file-download')
        token = serializer.dumps(pk)

        # Return encrypted link
        download_link = request.build_absolute_uri(f"/api/actual-download/{token}/")

        return Response({"download-link": download_link, "message": "success"})

from django.http import FileResponse

class ActualDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        if request.user.role != 'client':
            return Response({'error': 'Access denied'}, status=403)

        serializer = URLSafeSerializer(settings.SECRET_KEY, salt='file-download')
        try:
            file_id = serializer.loads(token)
        except Exception:
            return Response({'error': 'Invalid or expired link'}, status=400)
        
        uploaded_file = get_object_or_404(UploadedFile, pk=file_id)
        return FileResponse(uploaded_file.file, as_attachment=True)
