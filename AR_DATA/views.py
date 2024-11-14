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
import pandas as pd
import time
import google.generativeai as genai
# Create your views here.
from .models import User_data, Tour_place, Check, StampTable, history
from django.conf import settings

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
# User_data.objects.all().delete()
# Tour_place.objects.all().delete()
# Check.objects.all().delete()
# StampTable.objects.all().delete()

# import json

# json_file_path = os.path.join(settings.BASE_DIR,'data.json')

# with open(json_file_path, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # # 데이터 추가하기
# cnt = 0
# for item in data['Sheet1']:
#     # Tour_place 모델에 저장
#     try:
#         Tour_place.object.get(tour_id=cnt)
#         print("Already created")
        
#     except:
#         Tour_place.objects.create(
#             tour_id = cnt,
#             place=item['place'],
#             address=item['address'],
#             phone=str(item['phone']),  # phone 번호를 문자열로 저장
#             lat=str(item['lat']),
#             lng=str(item['lng']),
#             text=item['text'][:1000]  # text 필드는 최대 1000자로 제한
#         )
#     cnt += 1

# # print("Data added successfully!")

# for i in range(4):
#     try:
#         User_data.objects.get(key=i)
#         print("Already created")
#     except:
#         User_data.objects.create(key=i, stamp_count=0, store_count = 0, tour_count =0, secret_count=0)
#         print(f'key  : {i} created')



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
        new_entry = StampTable.objects.create(key=sign_id, tour_id=tour_num, num = user_data.stamp_count)
        file_path = default_storage.save(f'uploads/{sign_id}/{user_data.stamp_count}.png', ContentFile(image_file.read()))

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

@api_view(['POST'])
def stamp_data(request):
    sign_id = request.data.get('id')
    
    entries = StampTable.objects.filter(key=sign_id).order_by('timestamp')
    
    entry_list = [
        {
            "tour_id": entry.tour_id,
            "location" : Tour_place.objects.get(tour_id=entry.tour_id).place,
            "timestamp": entry.timestamp
        }
        for entry in entries
    ]
    return Response(entry_list, status=200)

from django.utils import timezone

@api_view(['POST'])
def mock_stamp_data(request):
    sign_id = request.data.get('id')
    
    entries = StampTable.objects.filter(key=sign_id).order_by('timestamp')
    
    count = 0
    cnt = 0
    cc = 0
    entry_list = []
    for i in range(4):
        entry_list.append({
            "tour_id": i,
            "location" : "ASDASDSDASADASD",
            "timestamp": timezone.now()
        })
        count += 2
    entry_list.append({
            "tour_id": i,
            "location" : "하하하하하하하하",
            "timestamp": timezone.now()
        })
    print(entry_list)
    return Response(entry_list, status=200)


GOOGLE_API_KEY = ""
df = pd.read_csv('yangdata.csv')
print(df)
@api_view(['POST'])
def LLM_QUEST(request):
    df = pd.read_csv('yangdata.csv')
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        system_instruction=""" 
            You are an AI travel guide that introduces tourist attractions and other locations in the Yangyang region of Korea.
            Your task is to recommend a one-day itinerary based on the user's preferences.
            The output should include place names, a brief description, and six itineraries for a one-day trip.
            The output text must not contain any Markdown marks or special symbols.
            The travel itinerary must include two visits to tourist attractions, one lodging, two visits to restaurants, and one visit to a cafe.
            When organizing a course, restaurant visits should be organized equally, taking lunch and dinner into account.
            When planning your course, you should never visit tourist attractions or restaurants all at once, but visit them evenly..
            For the travel course, you only need to print out one course consisting of a total of 6 locations.

        """
    )

    # 여행 코스 추천 요청
    start_time = time.time()

    # 사용자 취향에 대한 설명 (예: 해변, 자연, 휴식 등)
    user_preferences = "저는 해변을 좋아하고, 자연을 느낄 수 있는 곳을 선호해요. 먼저 점심을 먹고 시작을 하고싶어요. 숙소는 반드시 마지막에 방문하고 싶어요. 저녁에는 해산물 식사를 하고 싶어요."

    # 각 장소의 정보를 모델에 전달할 때 사용할 텍스트 포맷
    places_text = ""
    for _, row in df.iterrows():
        places_text += f"장소 이름: {row['place']}\n종류: {row['type']}\n설명: {row['text']}\n주소: {row['address']}\n위도: {row['lat']}\n경도: {row['lng']}\n\n"

    user_prompt = f"""
        안녕하세요! 저는 양양에서 추천 여행 코스를 찾고 있어요.
        제 취향은: {user_preferences}
        
        출력결과는 각 코스에 대해 코스n \n 장소의 이름 : \n 설명 : \n\n 으로 출력 주세요.
        장소의 이름과 설명은 엔터로 구분해 주세요.
        각 코스에 출력은 반드시 장소의 이름과 설명만 있어야 해.

        다음에 나열된 장소들의 정보를 참고하여, 여행 코스를 추천해 주세요.
        {places_text}
    """

    # 모델에게 여행 경로를 요청
    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=1.0)
    )

    print(response.text)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"실행 시간: {execution_time:.2f} 초")
    ans = list((response.text).split('\n'))
    lst = []
    dic = dict()
    print("여기까진만 ...")
    history.objects.filter(key=request.data.get('id')).delete()
    count = 1
    print("여기까진 옴..")
    for i in ans:
        if i[:3] == '장소의':
            dic['name'] = i[8::]
        elif i[:2] == '설명':
            dic['text'] = i[4::]
            print(dic['name'])
            print(dic['text'])
            langtitude = Tour_place.objects.get(place=dic['name']).lat
            longtitude = Tour_place.objects.get(place=dic['name']).lng
            iid = Tour_place.objects.get(place=dic['name']).tour_id
            if iid <= 19:
                dic['type'] = 0
            elif iid <= 39:
                dic['type'] = 1
            elif iid <= 59:
                dic['type'] = 2
            elif iid <= 79:
                dic['type'] = 3
            dic['langtitude'] = langtitude
            dic['longtitude'] = longtitude
            dic['address'] = Tour_place.objects.get(place=dic['name']).address
            dic['phone'] = Tour_place.objects.get(place=dic['name']).phone
            history.objects.create(key=request.data.get('id'), tour_id=iid, num = count, place = dic['name'], text = Tour_place.objects.get(place=dic['name']).text)
            lst.append(dic)
            dic = dict()
            count += 1
    for i in lst:
        print(i)
    return Response(lst, status=200)



@api_view(['POST'])
def history_view(request):
    id = request.data.get('id')
    filtered_history = history.objects.filter(key=request.data.get('id'))
    
    lst = []
    
    for his_entry in filtered_history:
        dic = dict()
        tour_id_ = his_entry.tour_id
        place_ = his_entry.place
        text_ = his_entry.text
        num_ = his_entry.num
        dic['location'] = place_
        dic['description'] - text_
        dic['tourId'] = tour_id_
        
        try:
            entry_stamp = StampTable.objects.get(key = id, tour_id = tour_id_)
            dic['isCollected'] = True
            dic['timestamp'] = entry_stamp.timestamp
            dic['imageIdx'] = entry_stamp.num
            
        except:
            dic['isCollected'] = False
            dic['timestamp'] = None
            dic['imageIdx'] = None
            
        
        lst.append(dic)
    return Response(lst, status=200)
            
        
        
        
        
        
        
    
    
    
    
    
    
def index(request):
    return HttpResponse("Communication start")