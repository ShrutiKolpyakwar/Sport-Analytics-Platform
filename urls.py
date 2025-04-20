from django.urls import path
from .views import dashboard,register_team_view,delete_team,predict_performance,predict_page, player_list, player_detail, leaderboard, advanced_stats, impact_leaderboard, performance_chart_static, team_synergy
from .views import predict_performance
urlpatterns = [
    path('', dashboard, name='dashboard'),  # This will be the landing page after login.
    path('players/', player_list, name='player-list'),
    path('players/<int:player_id>/', player_detail, name='player-detail'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('advanced/', advanced_stats, name='advanced-stats'),
    path('impact/', impact_leaderboard, name='impact-leaderboard'),
    path('chart-static/', performance_chart_static, name='performance-chart-static'),
    path('team-synergy/', team_synergy, name='team-synergy'),
    path('register-team/', register_team_view, name='register_team'),
    path("delete-team/<int:team_id>/", delete_team, name="delete_team"),
    path("predict/", predict_page, name="predict_page"),
    path("predict-goals/", predict_performance, name="predict_performance"),  

]
