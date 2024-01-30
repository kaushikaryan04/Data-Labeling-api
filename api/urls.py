from .views import FileUploadView ,TagStatementView
from django.urls import path
urlpatterns = [
    path("fileupload" , FileUploadView.as_view()),
    path("tagstatement" , TagStatementView.as_view() )

]