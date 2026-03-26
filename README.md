 # Movie Recommender System
A content-based movie recommendation system. 

## The project uses the MovieLens dataset:
- movies.csv
- ratings.csv
- tags.csv

## Structure

```bash
.
├── app.py                      # Streamlit app
├── data                        # Data (not included)
│   ├── links.csv
│   ├── movies.csv
│   ├── ratings.csv
│   ├── README.txt
│   └── tags.csv
├── images
│   └── app.png                 # Screenshot
├── movie_recommender.ipynb     # Analysis
├── pyproject.toml
├── README.md
├── recommender.py              # Code function
└── uv.lock
``` 
## Installation
* Clone repository and install dependencies using uv:

uv sync

## Usage
To start streamlit app on localhost:
streamlit run app.py


## Example
Input: 

"Toy Story"

## Output: 
![App Screenshot](/images/app.png)


### Adam Hedlund AIM25G