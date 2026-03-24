import streamlit as st
from recommender import build_recommender, recommend

st.set_page_config(page_title="Filmrekommendationer", page_icon="🎬")


@st.cache_resource
def load_model():
    return build_recommender()


movies, tfidf_matrix, knn, indices = load_model()

st.title("🎬 Filmrekommendationer")
st.write("Skriv in en film som du gillar!")

movie_input = st.text_input("Skriv en film", placeholder="Toy Story")

if st.button("Rekommendera"):
    if not movie_input.strip():
        st.warning("Skriv in en film först.")
    else:
        matched_title, result = recommend(movie_input, movies, tfidf_matrix, knn, indices)

        if matched_title is None:
            st.error(result)
        else:
            recommendations = result

            st.subheader(f"Rekommendationer baserat på: {matched_title}")

            for i, row in recommendations.iterrows():
                st.markdown(
                    f"**{i+1}. {row['title']}**  \n"
                    f"Genres: {row['genres']}  \n"
                )
                st.divider()