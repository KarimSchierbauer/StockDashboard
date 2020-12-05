from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PostSerializer, StockSerializer, SymbolSerializer
from .models import Post, Stock, Symbol


class TestView(APIView):

    permission_classes = (IsAuthenticated, )
 

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SymbolView(APIView):
     permission_classes = (IsAuthenticated, )

     def get(self, request, *args, **kwargs):
        qs = Symbol.objects.all()
        symbol = qs.first()
        #serializer = StockSerializer(qs, many=True)
        serializer = SymbolSerializer(symbol)
        return Response(serializer.data)


class StockView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = Stock.objects.all()
        stock = qs.first()
        #serializer = StockSerializer(qs, many=True)
        serializer = StockSerializer(stock)
        return Response(serializer.data)