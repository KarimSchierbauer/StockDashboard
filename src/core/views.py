from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

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

class SymbolViewByName(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SymbolSerializer

    def get(self, request, *args, **kwargs):

        item = self.kwargs.get('pk')
        print(item)
        #return Symbol.objects.filter(symbol_name=item)
        qs = Symbol.objects.all()
        symbol = get_list_or_404(qs, symbol_name=item)
        serializer = SymbolSerializer(symbol, many=True)
        return Response(serializer.data)


class StockView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        qs = Stock.objects.all()
        stock = qs.first()
        #serializer = StockSerializer(qs, many=True)
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

class StocksViewByName(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):

        item = self.kwargs.get('pk')
        print(item)
        #return Symbol.objects.filter(symbol_name=item)
        qs = Stock.objects.all()
        stock = get_list_or_404(qs, symbol=item)
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)