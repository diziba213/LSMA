import streamlit as st
import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# 앱 제목
st.title("Iris Species Prediction App")

# 데이터셋 불러오기
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 훈련 및 테스트 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 모델 훈련
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 사용자 입력 받기 (Streamlit 위젯)
st.sidebar.header("User Input Parameters")
def user_input_features():
    sepal_length = st.sidebar.slider('Sepal length', float(X[:, 0].min()), float(X[:, 0].max()), float(X[:, 0].mean()))
    sepal_width = st.sidebar.slider('Sepal width', float(X[:, 1].min()), float(X[:, 1].max()), float(X[:, 1].mean()))
    petal_length = st.sidebar.slider('Petal length', float(X[:, 2].min()), float(X[:, 2].max()), float(X[:, 2].mean()))
    petal_width = st.sidebar.slider('Petal width', float(X[:, 3].min()), float(X[:, 3].max()), float(X[:, 3].mean()))
    
    data = {'Sepal length': sepal_length,
            'Sepal width': sepal_width,
            'Petal length': petal_length,
            'Petal width': petal_width}
    
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

# 사용자가 입력한 파라미터 표시
st.subheader('User Input Parameters')
st.write(df)

# 예측하기
prediction = model.predict(df)
prediction_proba = model.predict_proba(df)

# 예측 결과 출력
st.subheader('Prediction')
st.write(f"Predicted Species: **{iris.target_names[prediction][0]}**")

st.subheader('Prediction Probability')
st.write(pd.DataFrame(prediction_proba, columns=iris.target_names))
