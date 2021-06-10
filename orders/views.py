from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.serializers import OrderCreateSerializer, DeliveryTeamSerializer
from rest_framework import status
from orders.models import Order, OrderDetail, DeliveryTeam, DeliveryAssignment
from inventory.models import Product
from django.template.loader import get_template
from django.template import Context
from fpdf import FPDF
from django.http import FileResponse


class OrderCreateAPI(APIView):
    def order_num_generation(self):
        order = Order.objects.all().last()
        if order:
            order_num = order.order_number.split('_')
            date_today = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
            order_date = datetime.strftime(date_today, "%d%m%y")
            if int(order_date) > int(order_num[0]):
                order_date = order_date
                order_digit = "_00001"
            else:
                order_date = order_num[0]
                order_digit = "_"+ str(int(order_num[1]) + 1).zfill(5)
        else:
            date_today = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
            order_date = datetime.strftime(date_today, "%d%m%y")
            order_digit = "_00001"
        return order_date + order_digit
        
    def post(self, request):
        try:
            serializer = OrderCreateSerializer(data=request.data)
            if serializer.is_valid():
                order_num = self.order_num_generation()
                datetime_now = datetime.now()
                order = Order(order_number=order_num,
                              customer_name=serializer.data['customer_name'],
                              customer_address=serializer.data['customer_address'],
                              customer_distance=serializer.data['customer_distance'],
                              order_status="Accepted",
                              total_price=serializer.data['total_price'],
                              created_time=datetime_now)
                order_item_list = []
                for item in serializer.data['products']:
                    product = Product.objects.get(product_id=item['product_id'])
                    if product.quantity > 0 or product.quantity > item['quantity']:
                        order_item = OrderDetail(order_num=order,
                                                 product_id=product,
                                                 quantity=item['quantity'])
                        product.quantity -= item['quantity']
                        product.save()
                        order_item_list.append(order_item)
                    else:
                        response_data = {
                            "product_id": product.product_id,
                            "available_quantity": product.quantity
                        }
                        return Response({"data": response_data,
                                         "message": "Product Unavailable"},
                                        status=status.HTTP_400_BAD_REQUEST)
                if float(serializer.data['customer_distance']) < 5:
                    delivery_time = 40
                    available_time = 20
                else:
                    delivery_time = 60
                    available_time = 40
                expected_delivery_time = datetime_now + timedelta(minutes=delivery_time)
                expected_available_time = expected_delivery_time + timedelta(minutes=available_time)
                delivery_team = DeliveryTeam.objects.all()
                free_team = delivery_team.exclude(is_available=False)
                if len(free_team) == 1:
                    team = free_team[0]
                    delivery_assignment = DeliveryAssignment(team=team,
                                                             order=order,
                                                             created_time=datetime_now)
                    team.is_available = False
                    team.available_time = expected_available_time
                    team.save()
                    order.et_delivery = expected_delivery_time
                    order.team_name = team.team_name
                    order.save()
                    OrderDetail.objects.bulk_create(order_item_list)
                    delivery_assignment.save()
                elif len(free_team) > 1:
                    next_available_team = free_team.order_by('-available_time')
                    # for item in next_available_team:
                    #     print(item)
                    team = next_available_team[0]
                    delivery_assignment = DeliveryAssignment(team=team,
                                                             order=order,
                                                             created_time=datetime_now
                                                             )
                    team.is_available = False
                    team.available_time = expected_available_time
                    team.save()
                    order.et_delivery = expected_delivery_time
                    order.team_name = team.team_name
                    order.save()
                    OrderDetail.objects.bulk_create(order_item_list)
                    delivery_assignment.save()
                else:
                    next_available_team = delivery_team.order_by('available_time')
                    team = next_available_team[0]
                    order.et_delivery = team.available_time + timedelta(minutes=delivery_time)
                    order.team_name = team.team_name
                    order.save()
                    OrderDetail.objects.bulk_create(order_item_list)
                return Response({"data": None,
                                 "message": "Success"},
                                status=status.HTTP_200_OK)
            return Response({"data": serializer.errors,
                             "message": "Input error"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OrderHistory(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(created_time__gte=datetime.now() - timedelta(days=1)).order_by('-created_time')
            context = {
                "orders": orders
            }
            return render(request, 'orders/orders.html', context=context)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddDeliveryTeamAPI(APIView):
    def post(self, request):
        try:
            serializer = DeliveryTeamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": None,
                                 "message": "Success"},
                                status=status.HTTP_200_OK)
            return Response({"data": serializer.errors,
                             "message": "Input error"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": str(e),
                             "message": "Something went wrong"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeliveryTeamList(APIView):
    def get(self, request):
        delivery_teams = DeliveryTeam.objects.all()
        context = {
            "delivery_teams": delivery_teams
        }
        return render(request, 'orders/delivery_team.html', context=context)
    

class GenerateReport(APIView):
    def get(self, request):
        orders = Order.objects.filter(created_time__gte=datetime.now() - timedelta(days=1))
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.set_font('courier', 'B', 16)
        pdf.cell(40, 10, 'This is what you have sold this month so far:', 0, 1)
        pdf.cell(40, 10, '', 0, 1)
        pdf.set_font('courier', '', 12)
        pdf.cell(10, 8, f"{'Item'.ljust(25) }{'Amount'.ljust(9)} {'Estimated Delivery'.rjust(1)}", 0, 1)
        for item in orders:
            deliver_time = item.et_delivery.strftime("%I:%M %p")
            pdf.cell(10, 8, f"{item.order_number.ljust(24)} {item.total_price}  {deliver_time}", 0, 1)
        pdf.output('report.pdf', 'F')
        return FileResponse(open('report.pdf', 'rb'), as_attachment=False, content_type='application/pdf')

    
