import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import io

sns.set()


@st.cache_data
def load_data(path='Used_Car_Price_Prediction.csv'):
    df = pd.read_csv(path)
    df['car_name'] = df['car_name'].fillna('')
    # attempt to parse date and extract year
    if 'ad_created_on' in df.columns:
        df['ad_created_on'] = pd.to_datetime(df['ad_created_on'], errors='coerce')
        df['year'] = df['ad_created_on'].dt.year
    return df


@st.cache_data
def get_wordcloud_text(series):
    text = ' '.join(series.astype(str).tolist()).lower()
    words = [w.strip('.,()') for w in text.split() if w.isalpha()]
    return ' '.join(words)


df = load_data()

st.set_page_config(layout='wide')
st.title('Used Car Data Explorer')
st.write('Interactive exploration of used-car listings (basic cleaning applied)')

# Sidebar filters
st.sidebar.header('Filters')
with st.sidebar.expander('Time & Make'):
    min_year = int(df['year'].min()) if 'year' in df.columns else 2000
    max_year = int(df['year'].max()) if 'year' in df.columns else 2025
    year_range = st.slider('Select year range', min_year, max_year, (min_year, max_year))
    make_options = ['All'] + sorted(df['make'].dropna().unique().tolist())
    make_choice = st.selectbox('Make', make_options)

with st.sidebar.expander('Location & Fuel'):
    city_options = ['All'] + sorted(df['city'].dropna().unique().tolist())
    city_choice = st.selectbox('City', city_options)
    fuel_options = ['All'] + sorted(df['fuel_type'].dropna().unique().tolist())
    fuel_choice = st.selectbox('Fuel', fuel_options)

# Apply filters
df_filtered = df.copy()
if 'year' in df.columns:
    df_filtered = df_filtered[df_filtered['year'].between(year_range[0], year_range[1])]
if make_choice != 'All':
    df_filtered = df_filtered[df_filtered['make'] == make_choice]
if city_choice != 'All':
    df_filtered = df_filtered[df_filtered['city'] == city_choice]
if fuel_choice != 'All':
    df_filtered = df_filtered[df_filtered['fuel_type'] == fuel_choice]

st.markdown(f"**Showing** {len(df_filtered):,} rows — filters applied")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric('Listings (filtered)', f"{len(df_filtered):,}")
if 'sale_price' in df_filtered.columns:
    col2.metric('Median Price', f"₹{int(df_filtered['sale_price'].median()):,}")
else:
    col2.metric('Median Price', 'N/A')
if 'kms_run' in df_filtered.columns:
    col3.metric('Median KMs', f"{int(df_filtered['kms_run'].median()):,}")
else:
    col3.metric('Median KMs', 'N/A')
col4.metric('Unique Makes', df_filtered['make'].nunique())

# Main charts
left, right = st.columns([2,1])
with left:
    st.subheader('Listings by Year')
    if 'year' in df_filtered.columns:
        fig, ax = plt.subplots(figsize=(8,4))
        counts = df_filtered['year'].value_counts().sort_index()
        counts.plot(kind='bar', ax=ax, color='C0')
        ax.set_xlabel('Year')
        ax.set_ylabel('Count')
        st.pyplot(fig)
    else:
        st.write('Year column not found')

    st.subheader('Top Makes (filtered)')
    if 'make' in df_filtered.columns:
        top = df_filtered['make'].value_counts().head(10)
        fig2, ax2 = plt.subplots(figsize=(8,3))
        top.plot(kind='barh', ax=ax2, color='C2')
        ax2.invert_yaxis()
        ax2.set_xlabel('Count')
        st.pyplot(fig2)
    else:
        st.write('Make column not found')

with right:
    st.subheader('Word Cloud — Car Names')
    wc_text = get_wordcloud_text(df_filtered['car_name'])
    if wc_text.strip():
        wc = WordCloud(width=600, height=300, background_color='white').generate(wc_text)
        fig_wc, ax_wc = plt.subplots(figsize=(6,3))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)
    else:
        st.write('No text to build word cloud')

    st.subheader('Counts by Source')
    if 'source' in df_filtered.columns:
        src = df_filtered['source'].value_counts().head(10)
        st.bar_chart(src)
    else:
        st.write('No source column')

# Data sample and download
st.subheader('Data sample')
st.dataframe(df_filtered.head(100))

def convert_df_to_csv(df_in: pd.DataFrame) -> bytes:
    return df_in.to_csv(index=False).encode('utf-8')

csv_bytes = convert_df_to_csv(df_filtered)
st.download_button('Download filtered CSV', data=csv_bytes, file_name='filtered_used_cars.csv', mime='text/csv')

