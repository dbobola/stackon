from django.contrib import admin
from django.urls import path
from mainpage import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resultJson',csrf_exempt(views.resultJson),name='Stackon'),
    path('collections/', views.collection_list),
    path('collections/<int:id>', views.collection_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)