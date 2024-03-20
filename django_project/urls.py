
from django.contrib import admin
from django.urls import path ,include
from ConerstoneLimmited.admin import cornerstone_admin
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('cornestone-admin',cornerstone_admin.urls),
    path('', include('ConerstoneLimmited.urls')),

]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
