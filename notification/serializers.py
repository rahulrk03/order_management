from rest_framework import serializers


class DeliverTeamSerializer(serializers.Serializer):
	team_name = serializers.CharField(required=True)
	order_num = serializers.CharField(required=True)

	
class AssignDeliverySerializer(serializers.Serializer):
	team_id = serializers.CharField(required=True)
	order_num = serializers.CharField(required=True)