from django.shortcuts import render

from django.http import FileResponse, Http404
from django.core.files.storage import default_storage
import os
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from AR_DATA.models import User_data


@api_view(['POST'])
def upload_image(request):
    print("Request come")
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    print("Not error")
    # 이미지 파일 가져오기
    image_file = request.FILES['file']
    sign_id = request.data.get('id')
    
    user_data = User_data.objects.get(key=sign_id)
    user_data.secret_count += 1
    user_data.save()
    
    
    
    file_path = default_storage.save(f'{sign_id}/{user_data.secret_count}.png', ContentFile(image_file.read()))

    return Response({'message': 'success', 'file_path': file_path}, status=200)


@api_view(['POST'])
def transmit_image(request):
    sign_id = request.data.get('id')
    image_num = request.data.get('name')
    file_path = f'{sign_id}/{image_num}.png'  # 저장된 이미지 경로 설정

    # 파일이 존재하는지 확인하고 응답으로 반환
    if default_storage.exists(file_path):
        file = default_storage.open(file_path, 'rb')
        response = FileResponse(file, content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="PartialScreenshot.png"'
        return response
    else:
        raise Http404("File not found")


def index(request):
    return HttpResponse("Communication start")