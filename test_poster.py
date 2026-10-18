
import requests

API_KEY = "37ae03dcc63e6d6b5f0b47cd29393dde"

url = "https://api.themoviedb.org/3/search/movie"

response = requests.get(
    url,
    params={
        "api_key": API_KEY,
        "query": "The Shawshank Redemption",
        "year": 1994
    },
    timeout=15
)

print("Status:", response.status_code)

if response.ok:
    results = response.json().get("results", [])

    if results and results[0].get("poster_path"):
        path = results[0]["poster_path"]
        print("Poster URL:")
        print("https://image.tmdb.org/t/p/w500" + path)
    else:
        print("No poster path returned.")
else:
    print(response.text[:500])
