# IMDb Movie Rating Scraper 🎬

A Python-based project that collects movie information and ratings from IMDb's publicly available datasets and displays the top-rated movies through a web application built with Flask. It also integrates The Movie Database (TMDB) API to display movie posters.

## 🚀 Features

- Displays the top 250 movies based on ratings and vote counts.
- Shows movie titles, release years, ratings, and vote counts.
- Provides a searchable movie gallery.
- Displays movie posters using the TMDB API.
- Processes movie datasets using Pandas.
- Exports movie information to CSV files.
- Offers a user-friendly web interface.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Web Framework:** Flask
- **API Integration:** TMDB API
- **HTTP Requests:** Requests
- **Frontend:** HTML, CSS
- **Data Storage:** CSV

## 📂 Project Structure

```text
IMDb-Movie-Rating-Scraper/
├── app.py
├── scraper.py
├── download_data.py
├── download_basics.py
├── imdb_page.html
├── imdb_top_250.csv
├── imdb_top_movies.csv
├── test_poster.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sheebacatherinem475-png/IMDb-Movie-Rating-Scraper.git
cd IMDb-Movie-Rating-Scraper
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the TMDB API key

Obtain an API key from [TMDB](https://www.themoviedb.org/settings/api).

Set it as an environment variable in PowerShell:

```powershell
$env:TMDB_API_KEY="YOUR_TMDB_API_KEY"
```

Replace the placeholder with your own key. Do not publish your API key on GitHub.

### 5. Run the application

```bash
python app.py
```

Open the following address in your browser:

`http://127.0.0.1:5000`

## 📊 Data Source

The project uses publicly available IMDb datasets for movie titles and ratings. Movie poster images are retrieved through the TMDB API when configured.

## 🎯 Project Objective

The objective of this project is to demonstrate data collection, data processing, API integration, and web development using Python. It transforms movie rating data into an interactive interface that makes it easier for users to explore highly rated films.

## 🔮 Future Enhancements

- Add movie genre filters.
- Improve search and sorting options.
- Add detailed movie information pages.
- Improve responsive design for mobile devices.
- Add pagination for browsing movies.

## ⚠️ Disclaimer

This project is intended for educational purposes.

This product uses the TMDB API but is not endorsed or certified by TMDB.

IMDb and TMDB are trademarks of their respective owners. This project is not affiliated with or endorsed by IMDb or TMDB.

## 👩‍💻 Author

**Project:** IMDb Movie Rating Scraper

**GitHub:** [sheebacatherinem475-png](https://github.com/sheebacatherinem475-png)
