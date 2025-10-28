from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache the view response for 15 minutes
def property_list(request):
    properties = get_all_properties()  # Now uses Redis low-level cache
    return JsonResponse({
        "data": properties
    })
