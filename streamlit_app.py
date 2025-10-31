
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import os

st.set_page_config(page_title="Pigeon Breeding App", layout="wide")
st.title("Pigeon Breeding App — Compatibility Selector")

st.sidebar.header("Data")
uploaded = st.sidebar.file_uploader("Upload CSV (columns: id,gender,color,weight,head,feather,power,health,image_path)", type=['csv'])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    st.sidebar.info("No CSV uploaded — using sample data included in the app.")
    df = pd.read_csv('data.csv')

# default mapping for categorical traits
value_map = {
    'color': {'white':10,'gray':8,'black':6,'brown':7},
    'head': {'long':10,'medium':7,'short':5},
    'feather': {'smooth':10,'medium':7,'rough':4}
}

st.sidebar.header("Target traits")
col_target = st.sidebar.selectbox("Target color", ['white','gray','black','brown'], index=0)
weight_target = st.sidebar.number_input("Target weight (grams)", value=400)
head_target = st.sidebar.selectbox("Target head shape", ['long','medium','short'], index=0)
feather_target = st.sidebar.selectbox("Target feather pattern", ['smooth','medium','rough'], index=0)
power_target = st.sidebar.slider("Target power (1-10)", 1, 10, 9)
health_target = st.sidebar.slider("Target health (1-10)", 1, 10, 9)

st.sidebar.header("Trait weights (sum ≈ 1)")
w_color = st.sidebar.number_input('Color weight', 0.0, 1.0, 0.3)
w_weight = st.sidebar.number_input('Weight weight', 0.0, 1.0, 0.2)
w_head = st.sidebar.number_input('Head shape weight', 0.0, 1.0, 0.1)
w_feather = st.sidebar.number_input('Feather pattern weight', 0.0, 1.0, 0.1)
w_power = st.sidebar.number_input('Power weight', 0.0, 1.0, 0.2)
w_health = st.sidebar.number_input('Health weight', 0.0, 1.0, 0.1)

# map categorical to numeric
def map_row(r):
    return {
        'color_v': value_map['color'].get(r['color'].lower(),7),
        'head_v': value_map['head'].get(r['head'].lower(),7),
        'feather_v': value_map['feather'].get(r['feather'].lower(),7)
    }

mapped = df.apply(map_row, axis=1, result_type='expand')
df = pd.concat([df, mapped], axis=1)

males = df[df['gender']=='male']
females = df[df['gender']=='female']

pairs = []
for _, m in males.iterrows():
    for _, f in females.iterrows():
        diff_color = abs(m['color_v'] - f['color_v'])
        diff_head = abs(m['head_v'] - f['head_v'])
        diff_feather = abs(m['feather_v'] - f['feather_v'])
        diff_weight = abs(m['weight'] - f['weight']) / max(1, weight_target) * 10  # scale 0-10
        diff_power = abs(m['power'] - f['power'])
        diff_health = abs(m['health'] - f['health'])

        weighted_sum = (diff_color * w_color + diff_head * w_head + diff_feather * w_feather +
                        diff_weight * w_weight + diff_power * w_power + diff_health * w_health)

        compatibility = max(0, round(100 - weighted_sum*1, 2))

        pairs.append({
            'male_id': m['id'], 'female_id': f['id'],
            'compatibility': compatibility,
            'diff_color': diff_color,
            'diff_head': diff_head,
            'diff_feather': diff_feather,
            'diff_weight': round(diff_weight,2),
            'diff_power': diff_power,
            'diff_health': diff_health,
            'male_img': m.get('image_path',''),
            'female_img': f.get('image_path','')
        })

pairs_df = pd.DataFrame(pairs).sort_values(by='compatibility', ascending=False)

st.header('Top matches')
st.dataframe(pairs_df[['male_id','female_id','compatibility']].head(20))

if not pairs_df.empty:
    top = pairs_df.iloc[0]
    st.subheader(f"Best pair: {top['male_id']} × {top['female_id']} — Compatibility {top['compatibility']}")
    col1, col2, col3, col4 = st.columns([1,2,2,1])
    try:
        if top['male_img'] and os.path.exists(top['male_img']):
            col1.image(Image.open(top['male_img']), caption=top['male_id'], use_column_width=True)
        else:
            col1.write(top['male_id'])
        if top['female_img'] and os.path.exists(top['female_img']):
            col4.image(Image.open(top['female_img']), caption=top['female_id'], use_column_width=True)
        else:
            col4.write(top['female_id'])
    except Exception as e:
        st.write('Image error:', e)

st.write('Total birds:', len(df), ' — total pairs calculated:', len(pairs_df))
