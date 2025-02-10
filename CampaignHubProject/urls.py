from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import FileUploadView, CampaignDataListView, UploadedFileListView, AggregateMonthlyDataView, UniqueFilterValuesView

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    path("filter/", CampaignDataListView.as_view(), name="data-filter"),
    path("files/", UploadedFileListView.as_view(), name="file-list"),
    path("aggregate/<int:file_id>/", AggregateMonthlyDataView.as_view(), name="aggregate-monthly-data"),  # Added aggregator view
    path('file/<int:file_id>/unique-values/', UniqueFilterValuesView.as_view(), name='unique_filter_values'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
