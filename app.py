import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title('US Top 50 Playlist')


# =========================
# Load the analyzed data
# =========================
@st.cache_data
def load_data():

    df_streamlit = pd.read_csv('analyzed_data.csv')

    # -------------------------
    # Convert date column
    # -------------------------
    df_streamlit['date'] = pd.to_datetime(
        df_streamlit['date'],
        format='mixed',
        errors='coerce'
    )

    # -------------------------
    # Convert release_date
    # -------------------------
    # Convert everything to string first
    df_streamlit['release_date'] = (
        df_streamlit['release_date']
        .astype(str)
        .str.strip()
    )

    # Find values containing only a year, e.g. "2012"
    year_only = df_streamlit['release_date'].str.fullmatch(r'\d{4}')

    # Convert year-only values to January 1 of that year
    df_streamlit.loc[year_only, 'release_date'] = (
        df_streamlit.loc[year_only, 'release_date'] + '-01-01'
    )

    # Convert to datetime
    df_streamlit['release_date'] = pd.to_datetime(
        df_streamlit['release_date'],
        format='mixed',
        errors='coerce'
    )

    return df_streamlit


df_streamlit = load_data()


# =========================
# Raw Data Preview
# =========================
st.subheader('Raw Data Preview')
st.write(df_streamlit.head())


# =========================
# Data Overview
# =========================
st.subheader('Data Overview')

st.write(f"Total entries: {len(df_streamlit)}")

st.write(
    f"Number of unique artists: "
    f"{df_streamlit['artist'].nunique()}"
)

# =========================
# Top Artists Analysis
# =========================
st.subheader('Top Artists by Number of Songs')

# Number of artists to display
num_artists = st.slider(
    'Select number of top artists',
    min_value=5,
    max_value=20,
    value=10
)

top_artists = (
    df_streamlit['artist']
    .value_counts()
    .head(num_artists)
)

# Display chart
fig_artists, ax_artists = plt.subplots(figsize=(12, 7))

sns.barplot(
    x=top_artists.values,
    y=top_artists.index,
    ax=ax_artists
)

ax_artists.set_title(
    f'Top {num_artists} Artists by Number of Songs'
)
ax_artists.set_xlabel('Number of Songs')
ax_artists.set_ylabel('Artist')

# Add values to bars
for i, value in enumerate(top_artists.values):
    ax_artists.text(
        value,
        i,
        f' {value}',
        va='center'
    )

st.pyplot(fig_artists)

# Display data table
st.write('### Top Artists Data')
st.dataframe(
    top_artists.reset_index().rename(
        columns={
            'artist': 'Artist',
            'count': 'Number of Songs'
        }
    ),
    use_container_width=True
)
# =========================
# Popularity Distribution
# =========================
st.subheader('Distribution of Song Popularity')

fig_pop, ax_pop = plt.subplots(figsize=(10, 6))

sns.histplot(
    df_streamlit['popularity'],
    bins=30,
    kde=True,
    ax=ax_pop
)

ax_pop.set_title('Distribution of Song Popularity')
ax_pop.set_xlabel('Popularity')
ax_pop.set_ylabel('Frequency')

st.pyplot(fig_pop)


# =========================
# Correlation Matrix
# =========================
st.subheader('Correlation Matrix of Numerical Features')

numeric_df_streamlit = df_streamlit.select_dtypes(
    include=['number']
)

fig_corr, ax_corr = plt.subplots(figsize=(10, 8))

sns.heatmap(
    numeric_df_streamlit.corr(),
    annot=True,
    cmap='coolwarm',
    fmt=".2f",
    ax=ax_corr
)

ax_corr.set_title(
    'Correlation Matrix of Numerical Features'
)

st.pyplot(fig_corr)


# =========================
# Top 10 Artists
# =========================
st.subheader('Top 10 Artists by Number of Songs')

top_artists = (
    df_streamlit['artist']
    .value_counts()
    .head(10)
)

st.bar_chart(top_artists)


# =========================
# Album Type Distribution
# =========================
st.subheader('Album Type Distribution')

album_type_dist = (
    df_streamlit['album_type']
    .value_counts()
)

st.bar_chart(album_type_dist)


# =========================
# Explicit Song Distribution
# =========================
st.subheader('Explicit Song Distribution')

is_explicit_dist = (
    df_streamlit['is_explicit']
    .value_counts()
)

st.bar_chart(is_explicit_dist)


# =========================
# Success Message
# =========================
st.success(
    'Streamlit app generated successfully!'
)