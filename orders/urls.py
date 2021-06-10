from django.urls import path
from .views import (OrderCreateAPI,
                    DeliveryTeamList,
                    AddDeliveryTeamAPI,
                    OrderHistory,
                    GenerateReport
                    )

urlpatterns = [
    path('order_create/', OrderCreateAPI.as_view(), name="order_create"),
    path('delivery_team_list/', DeliveryTeamList.as_view(), name="delivery_team_list"),
    path('add_delivery_team/', AddDeliveryTeamAPI.as_view(), name="add_delivery_team"),
    path('order_history/', OrderHistory.as_view(), name="order_history"),
    path('generate_report', GenerateReport.as_view(), name='generate_report')
]
