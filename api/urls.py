from .views import FileUploadView ,TagStatementView , DownloadTaggedFile , get_all_aspects,TagStatementCSView
from django.urls import path
urlpatterns = [
    path("fileupload" , FileUploadView.as_view()),
    path("tagstatement" , TagStatementView.as_view() ),
    path("tagstatementcsv" , TagStatementCSView.as_view()),
    path("downloadfile" , DownloadTaggedFile.as_view()),
    path("getaspects" ,get_all_aspects )


]