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
from .models import User_data, Tour_place, Check, stamp_table

places = [
    "낙산사",
    "하조대",
    "낙산해수욕장",
    "오산리 선사유적박물관",
    "양양전통시장",
    "서피비치",
    "휴휴암",
    "국립미천골자연휴양림",
    "설악산 국립공원",
    "오색탄산온천",
    "남애항 스카이워크 전망대",
    "일현미술관",
    "해담체험마을캠핑장",
    "쏠비치 양양 오션플레이",
    "설악해수욕장",
    "오색주전골",
    "한계령휴게소",
    "주전골",
    "법수치계곡",
    "죽도야영장",
    "쏠비치 양양",
    "낙산비치호텔",
    "투와이호텔",
    "지오 파인트리",
    "오색그린야드호텔",
    "더앤리조트",
    "디그니티호텔",
    "모닝비치 팬션",
    "양양 하조대 썬비치 펜션",
    "하조대비치하우스",
    "센텀마크 호텔 양양",
    "스머프하우스",
    "그린비치펜션",
    "코랄로 바이 조선",
    "이엘 호텔",
    "마레몬스호텔",
    "E7 양양죽도",
    "오션벨리리조트",
    "삼팔마린리조트",
    "양양국제공항호텔",
    "송이버섯마을",
    "영광정메밀국수 본점",
    "감나무식당",
    "금강산대게횟집",
    "맛골",
    "실로암메밀국수",
    "등불",
    "싱글핀에일웍스",
    "효주네머구리횟집",
    "범바우막국수",
    "돌바우횟집",
    "거북이 서프바",
    "양양째복",
    "수산항물회",
    "자연샘식당",
    "다래횟집",
    "하조대횟집",
    "공가네감자옹심이",
    "양양한우마을",
    "오색30년할머니순두부",
    "쏠티캐빈 양양점",
    "플리즈웨잇",
    "바다뷰 제빵소",
    "메밀라운지",
    "예쁘다 하조대",
    "페이보릿",
    "바다지기 공방카페",
    "하조델리 Hajodeli",
    "하조대 커피",
    "레이크지움",
    "P.E.I Coffee",
    "피프티피프티 에스프레소&위스키",
    "헤이카페",
    "양양그곳카페이름",
    "카페 달파도",
    "컨센트릭",
    "카페맴맴",
    "워터프런트커피",
    "카페화일리",
    "숲속의빈터"
]

state_dic = dict()
for i in range(len(places)):
    state_dic[places[i]] = i

@api_view(['POST'])
def upload_image(request):
    print("Request come")
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    print("Not error")
    # 이미지 파일 가져오기
    image_file = request.FILES['file']
    sign_id = request.data.get('id')
    tour_num = request.data.get('tour_num')
    print("id" , sign_id, "tour_num", tour_num)
    
    try:
        existing_entry = Check.objects.get(key=sign_id, tour_id=tour_num)
        return Response({'error': 'This entry already exists.'}, status=400)
    except:
        new_entry = Check.objects.create(key=sign_id, tour_id=tour_num)
        user_data = User_data.objects.get(key=sign_id)
        user_data.stamp_count += 1
        user_data.save()
        new_entry = stamp_table.objects.create(key=sign_id, tour_id=tour_num, num = user_data.stamp_count)
        file_path = default_storage.save(f'{sign_id}/{user_data.stamp_count}.png', ContentFile(image_file.read()))

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