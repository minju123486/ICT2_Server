from django.shortcuts import render


import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.


@api_view(['POST'])
def upload_image(request):
    print("Request come")
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    print("Not error")
    # 이미지 파일 가져오기
    image_file = request.FILES['file']
    file_path = default_storage.save('uploaded_images/PartialScreenshot.png', ContentFile(image_file.read()))

    return Response({'message': 'success', 'file_path': file_path}, status=200)

def index(request):
    return HttpResponse("Communication start")