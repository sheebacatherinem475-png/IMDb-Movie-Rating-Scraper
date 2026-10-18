import urllib.request

url = "https://datasets.imdbws.com/title.ratings.tsv.gz"
output = "title.ratings.tsv.gz"

try:
    print("Downloading IMDb ratings dataset...")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        with open(output, "wb") as file:
            while True:
                data = response.read(1024 * 1024)
                if not data:
                    break
                file.write(data)
                print("Downloaded another MB...")

    print("Download completed:", output)

except Exception as error:
    print("Download failed:", error)
