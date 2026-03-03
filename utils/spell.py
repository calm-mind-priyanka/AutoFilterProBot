from rapidfuzz import process

# Example static dictionary
MOVIE_NAMES = [
    "Avatar", "Inception", "Interstellar", "Avengers", "Joker"
]

def correct_spelling(query):
    match = process.extractOne(query, MOVIE_NAMES)
    if match and match[1] > 70:
        return match[0]
    return query
