import urllib.request

url = "https://datasets.imdbws.com/title.basics.tsv.gz"
output = "title.basics.tsv.gz"

try:
    print("Downloading IMDb movie details...")
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
