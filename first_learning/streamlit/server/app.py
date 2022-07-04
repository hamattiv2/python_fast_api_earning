import streamlit as st
import pandas as pd
import numpy as np

st.title('Sample App')




age = st.sidebar.slider('How old are you?', 0, 110, 25)
st.write("I'm ", age, 'years old')

col1, col2 = st.columns(2)
p = col1.slider('Pick Num in left', 0, 110, 25)
st.write("I'm ", p, 'years old')


col2.write('Write Col')