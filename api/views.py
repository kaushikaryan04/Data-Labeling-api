from rest_framework.decorators import api_view
from .serializers import TagSerializer
from rest_framework.parsers import FileUploadParser
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Statement , Tag
import pandas as pd
import os 
from openpyxl import load_workbook
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
        file_name = request.data.get("filename")
        serialized = TagSerializer(data = data , many = True)

        if serialized.is_valid() :
            serialized_data = serialized.data 
            data_row = []
            for data in serialized_data :
                temp = [data["statement"],data["aspect"],data["sentiment"]]
                data_row.append(temp)
                tag = Tag.objects.create(
                    statement = Statement.objects.get(text = data["statement"]),
                    aspect = data["aspect"],
                    sentiment = data["sentiment"]
                )
                tag.save()
        else :
            return Response({
                "Error":"Request format for data not valid"
            })
        headings_for_file = ["Statement" , "Aspect" , "Sentiment"]
        # try : 
        file_path = os.path.join(settings.BASE_DIR, "files" ,file_name )
        workbook = load_workbook(file_path)
        sheet_exists  = "tags" in workbook.sheetnames
        if sheet_exists :
            print("in tags sheet")
            df = pd.DataFrame(data_row, columns = headings_for_file)
            writer =   pd.ExcelWriter(file_path,  engine = 'openpyxl' , mode = "a" , if_sheet_exists= "overlay")
            df.to_excel(writer ,sheet_name="tags",index = False ,  header= False ,startrow=len(pd.read_excel(file_path , "tags"))+1 )
            writer._save()
            return Response({"Success":"Tags added successfully"})
        else :
            df = pd.DataFrame(data_row , columns = headings_for_file)
            print(file_path)
            with pd.ExcelWriter(file_path,engine="openpyxl" , mode = "a") as writer :
                df.to_excel(writer , "tags" , index= False , header=True)
            return Response({"Success":"Tags added successfully"})


class DownloadTaggedFile(APIView ) :
    def get(self , request , *args , **kwargs) :
        file_name = str(request.GET.get("file_name"))
        file_path = os.path.join(settings.BASE_DIR , "files" , file_name)
        if os.path.exists(file_path) :
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response 

        else :
            return Response({
                "Error" : "First upload file with statements"
            })

@api_view(["GET"])
def get_all_aspects(request) :
    statement = request.GET.get("statement")
    queryset = Tag.objects.filter(statement = Statement.objects.get(text = statement))
    serializer = TagSerializer(queryset , many = True)
    data = serializer.data
    return Response(data)





def is_file_xlsx(filename):
    if ".xlsx" in filename :
        return "xlsx"
    elif ".csv" in filename:
        return "csv" 
    return None 