from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Player, Team
import io
import base64
import matplotlib.pyplot as plt
new_leaderboard_entries = []

def player_list(request):
    query = request.GET.get('q', '')
    players = Player.objects.all()
    if query:
        players = players.filter(name__icontains=query)
    return render(request, "player_list.html", {"players": players, "query": query})

def player_detail(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'player_detail.html', {'player': player})

@login_required
# def leaderboard(request):
#     players = Player.objects.all().order_by('-goals')

#     ranked_players = []
#     prev_goals = None
#     rank = 0
#     for index, player in enumerate(players, start=1):
#         if prev_goals is None or player.goals < prev_goals:
#             rank = index
#         prev_goals = player.goals
#         ranked_players.append({"rank": rank, "player": player})
    
#     return render(request, "leaderboard.html", {"ranked_players": ranked_players})



@login_required
def leaderboard(request):
    global new_leaderboard_entries

    # If the form is submitted, get the new entry data and add it to the list
    if request.method == "POST":
        player_name = request.POST.get("player_name").strip()
        team_name = request.POST.get("team").strip()
        matches_played = request.POST.get("matches_played").strip()
        goals = request.POST.get("goals").strip()
        assists = request.POST.get("assists").strip()
        
        # Convert numeric fields safely
        try:
            matches_played = int(matches_played)
        except:
            matches_played = "N/A"
        try:
            goals = int(goals)
        except:
            goals = 0
        try:
            assists = int(assists)
        except:
            assists = "N/A"
        
        # Create new leaderboard entry as a dictionary
        new_entry = {
            "name": player_name,
            "team": team_name,
            "matches_played": matches_played,
            "goals": goals,
            "assists": assists,
        }
        new_leaderboard_entries.append(new_entry)
        # Optionally, you might want to redirect here to avoid duplicate POSTs:
        # from django.shortcuts import redirect
        # return redirect("leaderboard")

    # Define your static players data
    static_players = [
        {"name": "Lionel Messi", "team": "PSG", "matches_played": 30, "goals": 25, "assists": 31},
        {"name": "Neymar Jr", "team": "PSG", "matches_played": 25, "goals": 19, "assists": 15},
        {"name": "Cristiano Ronaldo", "team": "Barcelona", "matches_played": 32, "goals": 28, "assists": 12},
        {"name": "Kylian Mbappe", "team": "PSG", "matches_played": 29, "goals": 22, "assists": 18},
        {"name": "Bruno Fernandes", "team": "Manchester United", "matches_played": 31, "goals": 15, "assists": 20},
    ]
    
    # Merge the static data with new entries
    all_entries = static_players + new_leaderboard_entries

    # Sort the merged entries by goals in descending order
    all_entries.sort(key=lambda x: x["goals"] if isinstance(x["goals"], int) else 0, reverse=True)

    # Calculate ranking based on goals
    ranked_entries = []
    prev_goals = None
    rank = 0
    for index, entry in enumerate(all_entries, start=1):
        if prev_goals is None or entry["goals"] < prev_goals:
            rank = index
        prev_goals = entry["goals"]
        entry["rank"] = rank
        ranked_entries.append(entry)
    
    # Render the leaderboard template with the merged ranked data
    return render(request, "leaderboard.html", {"ranked_players": ranked_entries})




# def leaderboard(request):
#     # Define your static players data as dictionaries
#     static_players = [
#         {"name": "Lionel Messi", "team": "PSG", "matches_played": 30, "goals": 25, "assists": 31},
#         {"name": "Neymar Jr", "team": "PSG", "matches_played": 25, "goals": 19, "assists": 15},
#         {"name": "Cristiano Ronaldo", "team": "Barcelona", "matches_played": 32, "goals": 28, "assists": 12},
#         {"name": "Kylian Mbappe", "team": "PSG", "matches_played": 29, "goals": 22, "assists": 18},
#         {"name": "Bruno Fernandes", "team": "Manchester United", "matches_played": 31, "goals": 15, "assists": 20},
#     ]
    
#     # Get all newly registered teams from the database
#     new_teams = Team.objects.all()
#     # Get the set of team names that are already in the static players list
#     static_team_names = {player["team"] for player in static_players}
    
#     # For teams that are not in the static players, create placeholder entries
#     new_team_entries = []
#     for team in new_teams:
#         if team.name not in static_team_names:
#             new_team_entries.append({
#                 "name": "N/A",               # No player name available
#                 "team": team.name,
#                 "matches_played": "N/A",      # Or you could use 0
#                 "goals": 0,                   # Default to 0 goals
#                 "assists": "N/A",             # Or 0 if preferred
#             })
    
#     # Merge the two lists
#     all_entries = static_players + new_team_entries

#     # Sort by goals in descending order
#     all_entries.sort(key=lambda x: x["goals"] if x["goals"] is not None else 0, reverse=True)

#     # Calculate ranking based on goals
#     ranked_entries = []
#     prev_goals = None
#     rank = 0
#     for index, entry in enumerate(all_entries, start=1):
#         if prev_goals is None or entry["goals"] < prev_goals:
#             rank = index
#         prev_goals = entry["goals"]
#         entry["rank"] = rank
#         ranked_entries.append(entry)
    
#     # Pass the merged, ranked list to the template using the key "ranked_players"
#     return render(request, "leaderboard.html", {"ranked_players": ranked_entries})




@login_required
def advanced_stats(request):
    players = Player.objects.all()

    advanced_data = [
        {
            "player": player,
            "goals_per_match": round(player.goals / player.matches_played, 2) if player.matches_played else 0,
            "assists_per_match": round(player.assists / player.matches_played, 2) if player.matches_played else 0,
        }
        for player in players
    ]

    return render(request, "advanced_stats.html", {"advanced_data": advanced_data})



@login_required
def impact_leaderboard(request):
    players = Player.objects.all()

    impact_data = [
        {
            "player": player,
            "impact_score": round((2 * player.goals + player.assists) / player.matches_played, 2) if player.matches_played else 0
        }
        for player in players
    ]

    sorted_impact = sorted(impact_data, key=lambda x: x["impact_score"], reverse=True)
    ranked_impact = []
    prev_score = None
    rank = 0
    for index, item in enumerate(sorted_impact, start=1):
        if prev_score is None or item["impact_score"] < prev_score:
            rank = index
        prev_score = item["impact_score"]
        item["rank"] = rank
        ranked_impact.append(item)

    return render(request, "impact_leaderboard.html", {"ranked_impact": ranked_impact})



@login_required
def performance_chart_static(request):
    players = Player.objects.all()
    
    names = [p.name for p in players]
    goals = [p.goals for p in players]
    assists = [p.assists for p in players]

    fig, ax = plt.subplots(figsize=(10, 6))
    index = range(len(players))
    bar_width = 0.35

    ax.bar(index, goals, bar_width, alpha=0.8, color='r', label='Goals')
    ax.bar([i + bar_width for i in index], assists, bar_width, alpha=0.8, color='b', label='Assists')

    ax.set_xlabel('Players')
    ax.set_ylabel('Counts')
    ax.set_title('Player Performance (Goals vs. Assists)')
    ax.set_xticks([i + bar_width/2 for i in index])
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, "performance_chart.html", {"graphic": graphic})


@login_required

def team_synergy(request):
    team_synergy_data = []
    
    teams = Team.objects.all()
    for team in teams:
        players = Player.objects.filter(team=team)  # Assuming Player has a ForeignKey to Team
        player_count = players.count()
        synergy_score = calculate_team_synergy(players)  # Custom function to calculate synergy
        
        team_synergy_data.append({
            "team": team.name,
            "player_count": player_count,
            "synergy": synergy_score
        })

    return render(request, "team_synergy.html", {"team_synergy_data": team_synergy_data})

# Example function for synergy calculation
def calculate_team_synergy(players):
    if not players:
        return 0  # Default synergy score if no players
    return sum(player.skill_level for player in players) / len(players)  # Example metric


def dashboard(request):
    teams = Team.objects.all()
    return render(request, 'dashboard.html', {'teams': teams})


teams_data = [
    {"name": "PSG", "sport": "Kabbadi"},
    {"name": "PSG", "sport": "Football"},
    {"name": "Barcelona", "sport": "Badminton"},
    {"name": "PSG", "sport": "Badminton"},
    {"name": "Manchester United", "sport": "Cricket"},
]

players_data = [
    {"name": "Lionel Messi", "team": "PSG", "sport": "Kabbadi", "matches_played": 30, "goals": 25, "assists": 31},
    {"name": "Neymar Jr", "team": "PSG", "sport": "Football", "matches_played": 25, "goals": 19, "assists": 15},
    {"name": "Cristiano Ronaldo", "team": "Barcelona", "sport": "Badminton", "matches_played": 32, "goals": 28, "assists": 12},
    {"name": "Kylian Mbappe", "team": "PSG", "sport": "Badminton", "matches_played": 29, "goals": 22, "assists": 18},
    {"name": "Bruno Fernandes", "team": "Manchester United", "sport": "Cricket", "matches_played": 31, "goals": 15, "assists": 20},
]

# Organize teams by sport
teams_by_sport = {}
for team in teams_data:
    sport = team["sport"]
    if sport not in teams_by_sport:
        teams_by_sport[sport] = []
    teams_by_sport[sport].append(team["name"])


def dashboard(request):
    return render(request, 'dashboard.html', {
        'teams_by_sport': teams_by_sport,
        'players_data': players_data,  # ✅ Make sure this is passed correctly
    })


new_teams = []


def login_view(request):
    form = TeamRegistrationForm()  # Create an empty form

    if request.method == "POST":
        if "login_form" in request.POST:  # If login form is submitted
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")  # Redirect to dashboard after login
            else:
                return render(request, "login.html", {"error": "Invalid username or password", "form": form})

        elif "register_form" in request.POST:  # If registration form is submitted
            form = TeamRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")  # Redirect to dashboard after team registration

    return render(request, "login.html", {"form": form})




from stats.models import Team, Player

def dashboard_view(request):
    teams_by_sport = {}

    # Fetch teams grouped by sport
    for team in Team.objects.all():
        teams_by_sport.setdefault(team.sport, []).append(team.name)

    # Fetch all players
    players = Player.objects.all()

    return render(request, 'dashboard.html', {
        'teams_by_sport': teams_by_sport,
        'players': players
    })
from stats.models import Team, Player


# def register_team_view(request):
#     if request.method == "POST":
#         team_name = request.POST.get("team_name")
#         sport_name = request.POST.get("sport")

#         if team_name and sport_name:
#             Team.objects.create(name=team_name, sport=sport_name)
#             return JsonResponse({"success": True})  # Respond with success message

#     # Fetch registered teams for display
#     teams_by_sport = {}
#     for team in Team.objects.all():
#         teams_by_sport.setdefault(team.sport, []).append(team.name)

#     return render(request, "register_team.html", {"teams_by_sport": teams_by_sport})


# def delete_team(request, team_id):
#     # Only allow POST method for delete (you can add additional permission checks if needed)
#     if request.method == "POST":
#         team = get_object_or_404(Team, id=team_id)
#         team.delete()
#     return redirect("register_team")

def register_team_view(request):
    if request.method == "POST":
        team_name = request.POST.get("team_name")
        sport_name = request.POST.get("sport")
        if team_name and sport_name:
            Team.objects.create(name=team_name, sport=sport_name)
            return JsonResponse({"success": True})  # or redirect as needed

    teams_by_sport = {}
    for team in Team.objects.all():
        teams_by_sport.setdefault(team.sport, []).append(team)
    
    return render(request, "register_team.html", {"teams_by_sport": teams_by_sport})

from django.shortcuts import get_object_or_404, redirect

def delete_team(request, team_id):
    if request.method == "POST":
        team = get_object_or_404(Team, id=team_id)
        team.delete()
    return redirect("register_team")


import json
import joblib
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Load trained model
goals_predictor = joblib.load("stats/ml_models/goals_predictor.pkl")

def predict_page(request):
    """Render the Prediction Form Page"""
    return render(request, "stats/predict.html")  # Ensure this file exists

@csrf_exempt
def predict_performance(request):
    """Handle Prediction Requests"""
    if request.method == "GET":
        return render(request, "predict.html")  # Show page if accessed via GET

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            player_name = data.get("player_name", "Unknown Player")
            future_matches = int(data["future_matches"])

            # Make prediction
            predicted_goals = goals_predictor.predict(np.array([[future_matches]]))[0]

            return JsonResponse({
                "success": True,
                "player_name": player_name,
                "future_matches": future_matches,
                "predicted_goals": round(predicted_goals, 2)
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request"})
