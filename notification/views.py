from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from orders.models import DeliveryTeam, Order, DeliveryAssignment
from notification.models import Notifications
from .serializers import DeliverTeamSerializer, AssignDeliverySerializer


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class UpdateTeamAvailability(APIView):
    def post(self, request):
        try:
            serializer = DeliverTeamSerializer(data=request.data)
            if serializer.is_valid():
                order = Order.objects.get(order_number=serializer.data['order_num'])
                order.order_status = "Delivered"
                delivery_team = DeliveryTeam.objects.get(team_name=serializer.data['team_name'])
                delivery_team.is_available = True
                delivery_team.available_time = datetime.now()
                message = delivery_team.team_name + " is available for delivery now"
                Notifications.objects.create(message=message)
                order.save()
                delivery_team.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    group="chat_notification",
                message={
                    'type': "chat_message",
                    'message': message
                    }
                )
                return Response({"data": None,
                                 "message": "Success"},
                                status=status.HTTP_200_OK)
            return Response({"data": serializer.errors,
                             "message": "Input Error"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Something went Wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
        

class AssignTeamDelivery(APIView):
    def post(self, request):
        try:
            serializer = AssignDeliverySerializer(data=request.data)
            if serializer.is_valid():
                order = Order.object.get(order_number=serializer.data["order_num"])
                delivery_team = DeliveryTeam.objects.get(id=serializer.data['team_id'])
                datetime_now = datetime.now()
                if order.customer_distance < 5:
                    delivery_time = 40
                    available_time = 20
                else:
                    delivery_time = 60
                    available_time = 40
                expected_delivery_time = datetime_now + timedelta(minutes=delivery_time)
                expected_available_time = expected_delivery_time + timedelta(minutes=available_time)
                delivery_assignment = DeliveryAssignment(team_id=serializer.data["team_id"],
                                                         order=order,
                                                         created_time=datetime_now
                                                         )
                delivery_team.is_available = False
                delivery_team.available_time = expected_available_time
                order.et_delivery=expected_delivery_time
                order.team_name = delivery_team.team_name
                order.save()
                delivery_team.save()
                delivery_assignment.save()
                return Response({"data": None,
                                 "message": "Success"},
                                status=status.HTTP_200_OK)
            return Response({"data": serializer.errors,
                             "message": "Input Error"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Something went Wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
            
        
    
class NotificationList(APIView):
    def get(self, request):
        notification = Notifications.objects.all().order_by('-created_time')
        context = {
            "notifications": notification
        }
        return render(request, 'chat/notification.html', context=context)