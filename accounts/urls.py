from django.urls import path
from .views import AccountCreateAPIView, UserDetailAPIView

urlpatterns = [
    path('create/', AccountCreateAPIView.as_view(), name='account-create'),
    path('user/<str:username>/', UserDetailAPIView.as_view(), name='user-detail-by-username'),
    path('user/id/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail-by-id'),
]
