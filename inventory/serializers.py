from rest_framework import serializers
from inventory.models import Product


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('product_id', 'category', 'quantity', 'price')