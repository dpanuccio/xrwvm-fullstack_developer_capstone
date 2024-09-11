from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include urls from your app
    path('djangoapp/', include('djangoapp.urls')),

    # Static file serving
    path('', TemplateView.as_view(template_name="index.html")),  # Serve index.html for root route
    path('about/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('contact/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('login/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('register/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('dealers/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),  # React handles the routing here
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
