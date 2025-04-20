import os

# Player statistics data
data = [
    {"Name": "Cristiano Ronaldo", "Team": "B", "Matches_Played": 32, "Goals": 70, "Assists": 21},
    {"Name": "Kylian Mbappe	", "Team": "A", "Matches_Played": 29, "Goals": 65, "Assists": 18},
    {"Name": "Bruno Fernandes", "Team": "ML", "Matches_Played": 31, "Goals": 36, "Assists": 2},
    {"Name": "Lionel Messi", "Team": "PSG", "Matches_Played": 30, "Goals": 25, "Assists": 31},
    {"Name": "Neymar", "Team": "DL", "Matches_Played": 25, "Goals": 19, "Assists": 15},
]

def print_sports_data():
    print("Player Statistics:")
    print("------------------------")
    for row in data:
        print(f"Name: {row['Name']}")
        print(f"Team: {row['Team']}")
        print(f"Matches Played: {row['Matches_Played']}")
        print(f"Goals: {row['Goals']}")
        print(f"Assists: {row['Assists']}")
        print("------------------------")

if __name__ == "__main__":
    print_sports_data()
