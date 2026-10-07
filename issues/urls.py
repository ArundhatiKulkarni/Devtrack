from django.urls import path
from .views import reporters, reporter_detail, issues

urlpatterns = [
    path("reporters/", reporters),
    path("reporters/<int:reporter_id>/", reporter_detail),
    path("issues/", issues),
]