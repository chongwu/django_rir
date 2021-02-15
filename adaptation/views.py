from django.shortcuts import render
from .models import Map, MapPoint, MapPointValue, Conclusion, ExtraInfo


# Create your views here.
def map_list(request):
    maps = Map.objects.prefetch_related('employee').all()
    return render(request, 'map/list.html', {'maps': maps})


def map_detail(request, map_id):
    map_model = Map.objects.get(id=map_id)
    return render(request, 'map/detail.html', {'map_model': map_model})
