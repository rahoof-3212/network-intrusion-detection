import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="NETWORK INTRUSION DETECTION", page_icon="🛡️", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #0B1F3A 0%, #081729 50%, #0B1F3A 100%);
    color: #EAF6FF;
}

.header-title {
    font-size: 44px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0px;
}

.header-sub {
    font-size: 17px;
    color: #9FD8E8;
    margin-top: 0px;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,209,217,0.25);
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 20px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #00D1D9;
    margin-bottom: 12px;
}

div.stButton > button {
    background: linear-gradient(90deg, #00D1D9, #0B8FA6);
    color: #06202E;
    font-weight: 600;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    transition: 0.2s;
}
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 12px rgba(0,209,217,0.6);
}

div[data-testid="stNumberInput"] label {
    color: #BFE4FF !important;
    font-weight: 500;
}

.result-box {
    padding: 26px;
    border-radius: 14px;
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    margin-top: 20px;
}
.attack {
    background: linear-gradient(90deg, #7A0E23, #B3122E);
    color: white;
    box-shadow: 0 0 20px rgba(255,0,60,0.4);
}
.normal {
    background: linear-gradient(90deg, #0E7A4E, #12B36F);
    color: white;
    box-shadow: 0 0 20px rgba(0,255,140,0.3);
}
</style>
""", unsafe_allow_html=True)

# ---------- Load model ----------
model = joblib.load('intrusion_model.pkl')
selected_features = joblib.load('selected_features.pkl')
examples = joblib.load('examples.pkl')

# ---------- Header ----------
st.markdown('<p class="header-title">🛡️ NETWORK INTRUSION DETECTION</p>', unsafe_allow_html=True)
st.markdown('<p class="header-sub">Machine Learning powered classification of network traffic — Normal vs Attack</p>', unsafe_allow_html=True)

# ---------- Example loader ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Quick Load — Real Examples</p>', unsafe_allow_html=True)

for feature in selected_features:
    if feature not in st.session_state:
        st.session_state[feature] = 0.0

col1, col2 = st.columns(2)
with col1:
    if st.button("✅  Load Normal Example", use_container_width=True):
        for feature in selected_features:
            st.session_state[feature] = float(examples['normal'][feature])
with col2:
    if st.button("🚨  Load Attack Example", use_container_width=True):
        for feature in selected_features:
            st.session_state[feature] = float(examples['attack'][feature])
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Input fields ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Connection Details</p>', unsafe_allow_html=True)

cols = st.columns(3)
for i, feature in enumerate(selected_features):
    with cols[i % 3]:
        st.number_input(f"{feature}", key=feature)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Predict ----------
predict_clicked = st.button("🔍  PREDICT", use_container_width=True)

if predict_clicked:
    input_values = np.array([[st.session_state[feature] for feature in selected_features]])
    prediction = model.predict(input_values)[0]

    if prediction == 1:
        st.markdown('<div class="result-box attack">🚨 ATTACK DETECTED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box normal">✅ NORMAL TRAFFIC</div>', unsafe_allow_html=True)