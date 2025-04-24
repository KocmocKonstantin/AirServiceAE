from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


@api_view(['POST'])
def shorten_url_api(request):
    """API endpoint to create a shortened URL"""
    serializer = URLSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeView(View):
    """Home page with URL input form"""
    def get(self, request):
        return render(request, 'shortener/index.html')


class StatsView(View):
    """Statistics page showing URL access information"""
    def get(self, request):
        urls = URL.objects.all().order_by('-access_count')
        return render(request, 'shortener/stats.html', {'urls': urls})


def redirect_to_original(request, short_code):
    """Redirect from short URL to original URL"""
    try:
        url = URL.objects.get(short_code=short_code)
        url.access_count += 1
        url.save()
        return redirect(url.original_url)
    except URL.DoesNotExist:
        raise Http404("URL not found")
