from rest_framework import serializers
from orders.models import DeliveryTeam


class OrderCreateSerializer(serializers.Serializer):
	customer_name = serializers.CharField(required=True)
	customer_address = serializers.CharField(required=True)
	customer_distance = serializers.DecimalField(required=True, max_digits=2, decimal_places=2)
	total_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
	products = serializers.JSONField(required=True)
	

class DeliveryTeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliveryTeam
		fields = ['team_name']
		
		
class OutForDeliverySerializer(serializers.Serializer):
	order_num = serializers.CharField(required=True)