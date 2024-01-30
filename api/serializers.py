from rest_framework import serializers

# class FileSerializer(serializers.Serializer) : 
#     file = serializers.FileField()


class TagSerializer(serializers.Serializer):
    statement = serializers.CharField()
    aspect = serializers.CharField()
    sentiment = serializers.CharField()
    
    
