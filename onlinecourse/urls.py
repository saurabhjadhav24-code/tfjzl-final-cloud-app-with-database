```python
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='index'),

    path('registration/', views.registration_request, name='registration'),

    path('login/', views.login_request, name='login'),

    path('logout/', views.logout_request, name='logout'),

    path(
        'courses/<int:pk>/',
        views.CourseDetailView.as_view(),
        name='course_details'
    ),

    path(
        'enroll/<int:course_id>/',
        views.enroll,
        name='enroll'
    ),

    path(
        'submit/<int:course_id>/',
        views.submit,
        name='submit'
    ),

    path(
        'exam-result/<int:submission_id>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
```
