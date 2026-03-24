 # Movie Recommender System
A content-based movie recommendation system. 

## The project uses the MovieLens dataset:
- movies.csv
- ratings.csv
- tags.csv

## Structure

```bash
.
├── app.py                  # Streamlit app
├── data                    # Dataset
│   ├── links.csv
│   ├── movies.csv
│   ├── ratings.csv
│   ├── README.txt
│   └── tags.csv
├── movie_recommender.ipynb # Analysis
├── pyproject.toml
├── README.md
├── recommender.py          # Recommender code
└── uv.lock
``` 
## Installation
* Clone repository and install dependencies using uv:

uv sync

## Usage
To start streamlit app on localhost:
run streamlit app.py


## Example
Input: 

"Toy Story"

Output: 

1. Toy Story 2 (1999)
Genres: Adventure|Animation|Children|Comedy|Fantasy

2. Toy Story 3 (2010)
Genres: Adventure|Animation|Children|Comedy|Fantasy|IMAX

3. Monsters, Inc. (2001)
Genres: Adventure|Animation|Children|Comedy|Fantasy

4. Bug's Life, A (1998)
Genres: Adventure|Animation|Children|Comedy

5. Finding Dory (2016)
Genres: Adventure|Animation|Comedy

### Adam Hedlund AIM25G