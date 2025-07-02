from django.urls import path
from .views import UploadedFileListCreateView, LogoutView, ProfileView
from .views import api_home, FileDeleteView, RegisterView, CustomAuthToken, ChangePasswordView, DownloadFileView   # ✅ add karo

urlpatterns = [
    path('', api_home, name='api_home'),
    path('files/', UploadedFileListCreateView.as_view(), name='file-list-create'),
    path('files/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('download/<int:pk>/', DownloadFileView.as_view(), name='download-file'),   # ✅ yeh add karo
]

from .views import DownloadFileView, ActualDownloadView

urlpatterns += [
    path('download/<int:pk>/', DownloadFileView.as_view(), name='generate-download-link'),
    path('actual-download/<str:token>/', ActualDownloadView.as_view(), name='actual-download'),
]

