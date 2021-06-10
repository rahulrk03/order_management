from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from inventory.serializers import ProductSerializer
from rest_framework import status
from rest_framework import generics
from inventory.models import Product


def index(request):
	return render(request, 'inventory/index.html')


class AddProductAPI(APIView):
	@staticmethod
	def post(request):
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({"data": None,
							 "message": "Success"},
							status=status.HTTP_200_OK)
		return Response({"data": serializer.errors,
						 "message": "Input error"},
						status=status.HTTP_400_BAD_REQUEST)

	
class ProductList(generics.ListCreateAPIView):
	queryset = Product.objects.filter(is_active=True)
	
	def get(self, request):
		queryset = self.get_queryset()
		context = {
			"products": queryset
		}
		return render(request, 'inventory/inventory.html', context=context)
