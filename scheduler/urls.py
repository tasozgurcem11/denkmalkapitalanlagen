from django.urls import include, path
from scheduler import views

app_name = "scheduler"
urlpatterns = [
    path('schedule/', views.schedule_view, name="schedule"),
    path('schedule/week/<slug:start_date>', views.week_view, name="week"),
    path('schedule/week/slot/<int:id>/', views.slot_view, name="slot_detail"),
]
