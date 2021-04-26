from django.urls import path
from .views import add_user, construct_database, delete_data, leaderboard, leaderboard_country, submit_score, user_profile


urlpatterns = [
path('leaderboard/', leaderboard),
path('leaderboard/<str:country_code>', leaderboard_country),
path('user/create/', add_user),
path('user/profile/<uuid:user_uuid>', user_profile),
path('construct/', construct_database),
path('submit/score/', submit_score),
path('delete/', delete_data),


]