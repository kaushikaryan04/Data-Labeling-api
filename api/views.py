from rest_framework.decorators import api_view
from .serializers import TagSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Statement , Tag
import pandas as pd
import os 
from core import settings

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    def post(self , request , *args , **kwargs ): 
        file = request.FILES.get('file')
        if file :
            destination_path = os.path.join(settings.BASE_DIR ,'files', file.name)
            file_format = is_file_xlsx(file.name)
            if file_format == "xlsx" : 
                df = pd.read_excel(file,engine='openpyxl')
                df.to_excel(destination_path , index = False )
            elif file_format == "csv" :
                df = pd.read_csv(file)
                
                # df.drop(df.index[[0,1,2]] ,inplace = True)
                # df = df.drop(columns=[df.columns[0]])
                print(df)
                df.to_csv(destination_path)
            else :
                return Response({
                    "status" : "File upload failed check server logs"
                })

            statements = df['Statement']

            for statement in statements:
                s = Statement.objects.create(
                    text = str(statement)
                )
                s.save()
            return Response({
                "status" : "file uploadSuccessfull" 
            })
        return Response({
            "status" : "File upload failed check server logs"
        })

class TagStatementView(APIView) :
    def post(self , request ,*args , **kwargs) :
        data = request.data.get('data', [])
        serialized = TagSerializer(data = data , many = True)

        if serialized.is_valid() :
            serialized_data = serialized.data 
            for data in serialized_data :

                tag = Tag.objects.create(
                    statement = Statement.objects.get(text = data["statement"]),
                    aspect = data["aspect"],
                    sentiment = data["sentiment"]
                )
                tag.save()
                print(f"tag saved for statement {tag.statement}")

        else :
            return Response({
                "not ok":"no ok"
            })

        return Response({"ok":"ok"})



def is_file_xlsx(filename):
    if ".xlsx" in filename :
        return "xlsx"
    elif ".csv" in filename:
        return "csv" 
    return None 