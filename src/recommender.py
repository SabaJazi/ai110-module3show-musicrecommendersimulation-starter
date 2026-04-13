from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Converts numeric columns to float/int for calculation.
    Required by src/main.py
    """
    songs = []
    numeric_fields = {
        'id': int,
        'energy': float,
        'tempo_bpm': int,
        'valence': float,
        'danceability': float,
        'acousticness': float,
    }
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric strings to their proper types
                for field, field_type in numeric_fields.items():
                    if field in row:
                        row[field] = field_type(row[field])
                songs.append(row)
        print(f"Loaded {len(songs)} songs from {csv_path}")
        return songs
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading songs: {e}")
        return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song based on user preferences.
    Returns (total_score, list_of_reasons).
    
    Scoring rules:
    - Genre match: +2.0 points
    - Mood match: +1.0 point
    - Energy closeness: weighted by 1.5
    - Acousticness preference: weighted by 1.0
    """
    score = 0.0
    reasons = []
    
    # Genre match: +2.0 points
    if song.get('genre') == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append(f"Genre match: {song['genre']} (+2.0)")
    
    # Mood match: +1.0 point
    if song.get('mood') == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append(f"Mood match: {song['mood']} (+1.0)")
    
    # Energy closeness (1.0 = exact match, 0.0 = maximum difference)
    target_energy = user_prefs.get('target_energy', 0.5)
    song_energy = float(song.get('energy', 0.5))
    energy_closeness = 1.0 - abs(song_energy - target_energy)
    energy_score = energy_closeness * 1.5
    score += energy_score
    reasons.append(f"Energy closeness ({song_energy:.2f} vs {target_energy:.2f}): {energy_closeness:.2f} (+{energy_score:.2f})")
    
    # Acousticness match to preference
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    song_acousticness = float(song.get('acousticness', 0.5))
    if likes_acoustic:
        acoustic_score = song_acousticness * 1.0
        reasons.append(f"Acoustic preference: {song_acousticness:.2f} (+{acoustic_score:.2f})")
    else:
        acoustic_score = (1.0 - song_acousticness) * 1.0
        reasons.append(f"Electronic preference: {acoustic_score:.2f} (+{acoustic_score:.2f})")
    score += acoustic_score
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    
    Returns list of (song_dict, score, explanation_string) tuples sorted by score descending.
    """
    # Score all songs and collect results
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k recommendations
    return scored_songs[:k]
