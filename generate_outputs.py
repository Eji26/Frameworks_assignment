import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

def main():
    csv='Used_Car_Price_Prediction.csv'
    print('Loading', csv)
    df=pd.read_csv(csv)
    print('Loaded shape', df.shape)

    # Convert ad_created_on to datetime/year
    if 'ad_created_on' in df.columns:
        df['ad_created_on']=pd.to_datetime(df['ad_created_on'], errors='coerce')
        df['year']=df['ad_created_on'].dt.year

    # Text feature
    df['car_name']=df['car_name'].fillna('')
    df['name_word_count']=df['car_name'].apply(lambda x: len(str(x).split()))

    # Missing percentages
    missing_pct = df.isnull().mean().sort_values(ascending=False)
    print('Top missing columns:\n', missing_pct.head(10).to_string())

    # Drop columns with >60% missing
    to_drop = list(missing_pct[missing_pct > 0.6].index)
    if to_drop:
        print('Dropping columns:', to_drop)
        df = df.drop(columns=to_drop)

    # Fill numeric NaNs with median
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        med = df[c].median()
        if not np.isnan(med):
            df[c] = df[c].fillna(med)

    # Fill categorical NaNs with 'unknown'
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for c in cat_cols:
        df[c] = df[c].fillna('unknown')

    # Drop rows missing sale_price
    if 'sale_price' in df.columns:
        before = df.shape[0]
        df = df[~df['sale_price'].isnull()]
        after = df.shape[0]
        print(f'Dropped {before-after} rows missing sale_price')

    out = 'cleaned_used_car_data.csv'
    df.to_csv(out, index=False)
    print('Wrote', out, 'shape', df.shape)

    # Plot listings by year
    if 'year' in df.columns:
        yc = df['year'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8,4))
        yc.plot(kind='bar', ax=ax)
        ax.set_title('Listings by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Count')
        fig.savefig('publications_by_year.png', bbox_inches='tight')
        print('Wrote publications_by_year.png')

    # Top makes
    if 'make' in df.columns:
        top = df['make'].value_counts().head(20)
        fig2, ax2 = plt.subplots(figsize=(10,5))
        top.plot(kind='bar', ax=ax2)
        ax2.set_title('Top Makes')
        fig2.savefig('top_makes.png', bbox_inches='tight')
        print('Wrote top_makes.png')

    # Wordcloud from car_name
    text = ' '.join(df['car_name'].astype(str).tolist()).lower()
    words = [w.strip('.,()') for w in text.split() if w.isalpha()]
    if words:
        wc = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
        fig3, ax3 = plt.subplots(figsize=(12,6))
        ax3.imshow(wc, interpolation='bilinear')
        ax3.axis('off')
        fig3.savefig('car_name_wordcloud.png', bbox_inches='tight')
        print('Wrote car_name_wordcloud.png')

if __name__ == '__main__':
    main()
