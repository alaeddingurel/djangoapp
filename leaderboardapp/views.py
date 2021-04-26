from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, request
from django.views.decorators import csrf
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.parsers import JSONParser
from rest_framework.relations import ManyRelatedField
from rest_framework.serializers import Serializer
from rest_framework.utils import serializer_helpers
from .models import Submission, User
from .serializers import SubmissionSerializer, UserSerializer
from django.db import transaction




from django.views.decorators.csrf import csrf_exempt
import uuid
from random import randrange

@transaction.atomic
def rank_score():
    for idx, i in enumerate(User.objects.order_by('-points')):
        # Checking this in order to improve response time
        if i.rank != idx+1:
            i.rank = idx+1
            i.save()

@transaction.atomic
def rank_leaderboard():
    for idx, i in enumerate(User.objects.order_by('-points')[0:100]):
        # Checking this in order to improve response time
        if i.rank != idx+1:
            i.rank = idx+1
            i.save()


@csrf_exempt
def leaderboard(request):

    if request.method == 'GET':
        scores = User.objects.order_by('-points')
        serializer = UserSerializer(scores, many=True)

        #CHANGING SERIALIZED DATA
        #rank_leaderboard()
        
        serialized_data = serializer.data
        for idx, i in enumerate(serialized_data):
            i['rank'] = idx+1 

        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'message': 'Request method must be GET'})

@csrf_exempt
def leaderboard_country(request, country_code):

    if request.method == 'GET':
        #rank_score()
        scores = User.objects.filter(iso_code=country_code).order_by('-points')[0:100]
        serializer = UserSerializer(scores, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'message': 'Request method must be GET'})

@csrf_exempt
def submit_score(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubmissionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            try:
                user_submit = User.objects.get(user_id=data['user_id'])
            except:
                return JsonResponse({'message': 'user does not exist'})

            if data['score_worth'] > user_submit.points:
                user_submit.points = data['score_worth']
                user_submit.save()
            
            #rank_score()
            submission = Submission.objects.filter(user_id=serializer.data['user_id']).order_by('-id')[0]
            serializer = SubmissionSerializer(submission)
            

            return JsonResponse(serializer.data, safe=False , status=201)
        return JsonResponse(serializer.errors)
    else:
        return JsonResponse({'message': 'Request method must be POST'})

@csrf_exempt
def add_user(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors)
    else:
        return JsonResponse({'message': 'Request method must be POST'})


@csrf_exempt
def user_profile(request, user_uuid):

    if request.method == 'GET':
        profile = User.objects.get(user_id=user_uuid)
        serializer = UserSerializer(profile)
        print(serializer)
        print(User.objects.filter(points__gt=serializer.data["points"]).count()+1)

        # Initializing with other variables in order to change value.
        serialized_data = serializer.data
        serialized_data["rank"] = User.objects.filter(points__gt=serialized_data["points"]).count()+1

        return JsonResponse(serialized_data, safe=False)
    else:
        return JsonResponse({'message': 'Request method must be GET'})


@csrf_exempt
def construct_database(request):
    data = JSONParser().parse(request)

    iso_code_list = ["TR", "UK"]
    instance_list = []
    if request.method == 'POST':
        for item in iso_code_list:
            for i in range(data['user_number']):
                a = User(user_id=uuid.uuid4(), display_name='user_id_'+str(i), iso_code=item, points=randrange(10000), rank=randrange(1000))
                instance_list.append(a)
    User.objects.bulk_create(instance_list)
    return HttpResponse({'message': 'okay'})


@csrf_exempt
def delete_data(request):

    if request.method == 'GET':
        User.objects.all().delete()
        Submission.objects.all().delete()
        return JsonResponse({'message': 'Data Deleted'})
# Create your views here.
