from django.urls import path
from notification.views import room, UpdateTeamAvailability, NotificationList

urlpatterns = [
    path('chat/<str:room_name>/', room, name='room'),
    path('updateTeamAvailability/', UpdateTeamAvailability.as_view(), name='updateTeamAvailability'),
    path('notification_list/', NotificationList.as_view(), name='notification_list')
]