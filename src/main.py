"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "likes_acoustic": False,
    },
    "Adversarial - High Energy Sad Acoustic": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "likes_acoustic": True,
    },
    "Adversarial - Chill Max Energy": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 1.0,
        "likes_acoustic": True,
    },
    "Adversarial - Missing Genre": {
        "favorite_genre": "nonexistent_genre",
        "favorite_mood": "happy",
        "target_energy": 0.70,
        "likes_acoustic": False,
    },
    # "Adversarial - Missing Mood": {
    #     "favorite_genre": "rock",
    #     "favorite_mood": "nonexistent_mood",
    #     "target_energy": 0.80,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - Neutral Energy Midpoint": {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "happy",
    #     "target_energy": 0.50,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - EDM But Acoustic": {
    #     "favorite_genre": "edm",
    #     "favorite_mood": "intense",
    #     "target_energy": 0.90,
    #     "likes_acoustic": True,
    # },
    # "Adversarial - Folk But Electronic": {
    #     "favorite_genre": "folk",
    #     "favorite_mood": "calm",
    #     "target_energy": 0.20,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - Energy Too High": {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "happy",
    #     "target_energy": 1.50,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - Energy Too Low": {
    #     "favorite_genre": "rock",
    #     "favorite_mood": "sad",
    #     "target_energy": -0.30,
    #     "likes_acoustic": True,
    # },
    # "Adversarial - Minimal Signal": {
    #     "favorite_genre": "",
    #     "favorite_mood": "",
    #     "target_energy": 0.90,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - Pop Chill Conflict": {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "chill",
    #     "target_energy": 0.90,
    #     "likes_acoustic": False,
    # },
    # "Adversarial - Tie Heavy Rock": {
    #     "favorite_genre": "rock",
    #     "favorite_mood": "intense",
    #     "target_energy": 0.90,
    #     "likes_acoustic": False,
    # },
}


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Pick one profile to run in the CLI.
    # active_profile_name = "High-Energy Pop"
    active_profile_name = "Adversarial - Missing Genre"

    user_prefs = USER_PROFILES[active_profile_name]

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Format and display results
    print("\n" + "="*80)
    print("🎵 MUSIC RECOMMENDER RESULTS")
    print("="*80)
    print(f"Profile: {active_profile_name}")
    print(f"\nUser Preferences:")
    print(f"  • Genre: {user_prefs['favorite_genre']}")
    print(f"  • Mood: {user_prefs['favorite_mood']}")
    print(f"  • Target Energy: {user_prefs['target_energy']}")
    print(f"  • Likes Acoustic: {user_prefs['likes_acoustic']}")
    print("\n" + "-"*80)
    print(f"Top {len(recommendations)} Recommendations:\n")

    for rank, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        
        print(f"{rank}. {song['title']}")
        print(f"   Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.2f}/5.5")
        
        # Parse and format reasons
        reasons = explanation.split(" | ")
        print(f"   Why:")
        for reason in reasons:
            print(f"      ✓ {reason}")
        print()

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
