# Used Car Data — Short Report

Summary
- Dataset: `Used_Car_Price_Prediction.csv` (listings snapshot).\n- I performed exploration, cleaning, and produced visualizations and a small Streamlit app.

Key steps performed
- Data loaded and inspected (shape, dtypes, missing values).\n- Converted `ad_created_on` to datetime and extracted `year`.\n- Created `name_word_count` from `car_name`.\n- Imputed numeric NaNs with column medians; filled categorical NaNs with `'unknown'`.\n- Dropped rows missing `sale_price`. Cleaned dataset saved as `cleaned_used_car_data.csv`.

Key statistics and findings
- Rows in cleaned data: see `cleaned_used_car_data.csv` for exact count.\n- Median `sale_price` (filtered sample in Streamlit) is shown in the app; across dataset the median is roughly the central tendency for prices.\n- Top makes: the dataset is dominated by mainstream manufacturers (e.g., Maruti, Hyundai, Honda) — see `top_makes.png`.\n- Time distribution: listings cluster in recent years; see `publications_by_year.png`.\n- Word-cloud of `car_name` reveals common models and tokens (e.g., `swift`, `i20`, `alto`) — see `car_name_wordcloud.png`.

Reflections and limitations
- The cleaning strategy is intentionally simple (median imputation, `'unknown'` placeholders). A production analysis should treat each column individually (e.g., investigate why `original_price` has missing values).\n- The dataset contains categorical variants and mixed tokens (e.g., `petrol & cng`) that may need standardized mapping.\n- The `ad_created_on` time range is short — the time-based analysis is limited to available years.\n- Word frequency was calculated from `car_name` only; titles/abstracts were not available in this dataset and were out of scope.

Next steps (recommended)
- Standardize categorical values (fuel types, make/model variants).\n- Engineer additional features: age = `year_mfr` difference, price per km, etc.\n- Add robust missing-value handling and outlier detection for `sale_price` and `kms_run`.\n- Expand Streamlit app with price distribution plots and filters by body type or transmission.

Files produced
- `cleaned_used_car_data.csv`\n- `publications_by_year.png`\n- `top_makes.png`\n- `car_name_wordcloud.png`\n- `analysis.ipynb` (source notebook)\n- `executed_analysis.ipynb` (notebook with outputs embedded)\n- `app.py` (Streamlit app)
