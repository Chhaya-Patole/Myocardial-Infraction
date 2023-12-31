import pickle
import pandas as pd
from sklearn import preprocessing
import streamlit as st

MODEL_PATH = "MI_model.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

if __name__ == "__main__":
    st.title("Myocardial Infarction Prediction with ML")
# user input
    AGE = st.sidebar.number_input("Insert the Age")
    SEX=st.selectbox("Gender", ["0:Female", "1:Male"], index=0)
    INF_ANAM=st.selectbox("Quantity of myocardial infarctions",["0:Zero", "1: One", "2:Two", "3: Three or more"], index=0)
    STENOK_AN=st.selectbox("Exertional angina pectoris",  ["0: never"," 1: During the last year", "2: one year ago", "3: two years ago", "4: three years ago", "5: 4-5 years ago"], index=0)
    FK_STENOK=st.selectbox("Functional class (FC) of angina pectoris in the last year",  ["0: there is no angina pectoris", "1: I FC", "2: II FC", "3: III FC", "4: IV FC"], index=0)
    IBS_POST=st.selectbox("Coronary heart disease (CHD) in recent weeks, days before admission to hospital",
            ["0: none", "1: exertional angina pectoris", "2: unstable angina pectoris"],
            index=0)
    GB = st.selectbox("Presence of an essential hypertension", ["0: there is no essential hypertension","1: Stage 1", "2: Stage 2", "3: Stage 3"], index=0)
    nr=st.selectbox(
            "No Reflow Phenomenon",
            [
                "0:Premature atrial contractions in the anamnesis",
                "1:Premature ventricular contractions in the anamnesis",
                "2:Paroxysms of atrial fibrillation in the anamnesis)",
                "3:A persistent form of atrial fibrillation in the anamnesis",
                "4:Ventricular fibrillation in the anamnesis"
                "5:Ventricular paroxysmal tachycardia in the anamnesis"
                "6:Observing of arrhythmia in the anamnesis"
            ],
            index=0,
        ),
    endocr_02=st.selectbox("Obesity in the anamnesis", ["0:No", "1:Yes"], index=0)
    zab_leg_02=st.selectbox("Obstructive chronic bronchitis in the anamnesis", ["0:No", "1:Yes"], index=0)
    lat_im=st.selectbox("Presence of a lateral myocardial infarction (left ventricular) (ECG changes in leads V5: V6 , I, AVL)", ["0: there is no infarct in this location"," 1: QRS has no changes", "2: QRS is like QR-complex", "3: QRS is like Qr-complex", "4: QRS is like QS-complex"], index=0)
    inf_im=st.selectbox("Presence of an inferior myocardial infarction (left ventricular) (ECG changes in leads III, AVF, II)", ["0: there is no infarct in this location"," 1: QRS has no changes", "2: QRS is like QR-complex", "3: QRS is like Qr-complex", "4: QRS is like QS-complex"], index=0)
    post_im=st.selectbox("Presence of a posterior myocardial infarction (left ventricular) (ECG changes in V7: V9, reciprocity changes in leads V1 – V3)",
            ["0: there is no infarct in this location"," 1: QRS has no changes", "2: QRS is like QR-complex", "3: QRS is like Qr-complex", "4: QRS is like QS-complex"], index=0)
    IM_PG_P=st.selectbox(
            "Presence of a right ventricular myocardial infarction", ["0:No", "1:Yes"], index=0)
    ritm_ecg_p_01=st.selectbox(
            "ECG rhythm at the time of admission to hospital: sinus (with a heart rate 60-90)",
            ["0:No", "1:Yes"],index=0,)
    ritm_ecg_p_02=st.selectbox("ECG rhythm at the time of admission to hospital: atrial fibrillation", ["0:No", "1:Yes"], index=0)
    n_r_ecg_p_02=st.selectbox(
            "Frequent premature atrial contractions on ECG at the time of admission to hospital",
            ["0:No", "1:Yes"],index=0)
    n_r_ecg_p_08=st.selectbox(
            "Paroxysms of supraventricular tachycardia on ECG at the time of admission to hospital",
            ["0:No", "1:Yes"],index=0)
    GIPO_K=st.selectbox(
            "Hypokalemia ( < 4 mmol/L)", ["0:No", "1:Yes"], index=0)
    
    TIME_B_S=st.selectbox(
            "Time elapsed from the beginning of the attack of CHD to the hospital",["1: less than 2 hours," "2: 2-4 hours", "3: 4-6 hours", "4: 6-8 hours"," 5: 8-12 hours", "6: 12-24 hours", "7: more than 1 days"," 8: more than 2 days", "9: more than 3 days"],index=0,)
    NOT_NA_1_n=st.selectbox(
            "Use of NSAIDs in the ICU in the first hours of the hospital period",[" 0: no"," 1: once"," 2: twice"," 3: three times", "4: four or more times"],index=0,)
    RAZRIV=st.selectbox(
            "Myocardial rupture",["0:No", "1:Yes"],index=0,)

    df=pd.DataFrame(columns=['SEX', 'INF_ANAM', 'STENOK_AN', 'FK_STENOK', 'IBS_POST', 'GB', 'nr_02', 'nr_07', 'endocr_02', 'zab_leg_02', 'lat_im', 'inf_im', 'post_im', 'IM_PG_P', 'ritm_ecg_p_01', 'ritm_ecg_p_02', 'n_r_ecg_p_02', 'n_r_ecg_p_08', 'GIPO_K', 'TIME_B_S', 'NOT_NA_1_n', 'RAZRIV'])


    # Missing Value Imputation
    df_f = df.apply(lambda x: x.fillna(x.mode().iloc[0]))


    # separate numeric and categorical columns
    numeric=df_f[['AGE','S_AD_ORIT', 'D_AD_ORIT', 'K_BLOOD','NA_BLOOD','ALT_BLOOD','AST_BLOOD','L_BLOOD','ROE']]
    categorical_columns=[]
    for i in df_f:
        if i not in numeric:
            categorical_columns.append(i)
        
    categorical_data = df_f[categorical_columns]
             
    # Normalise the data
    column_name=numeric.columns
    scaler=preprocessing.MinMaxScaler()
    numeric_norm=scaler.fit_transform(numeric)
    numeric_norm=pd.DataFrame(numeric_norm,columns=column_name)

     # Code for Prediction
    Outcome = ''

    # Creating a button for Prediction
    if st.button("Prediction"):
        X = [SEX, INF_ANAM, STENOK_AN, FK_STENOK, IBS_POST, GB, nr, endocr_02, zab_leg_02, lat_im, inf_im,
             post_im, IM_PG_P, ritm_ecg_p_01, ritm_ecg_p_02, n_r_ecg_p_02, n_r_ecg_p_08, GIPO_K, TIME_B_S, NOT_NA_1_n, RAZRIV]

        MI_prediction = model.predict([X])

        if MI_prediction == 0:
            Outcome = "Unknown Cause (Alive)"
        elif MI_prediction == 1:
            Outcome = "Cardiogenic Shock"
        elif MI_prediction == 2:
            Outcome = "Pulmonary Edema"
        elif MI_prediction == 3:
            Outcome = "Myocardial Rupture"
        elif MI_prediction == 4:
            Outcome = "Progress of Congestive Heart Failure"
        elif MI_prediction == 5:
            Outcome = "Thromboembolism"
        elif MI_prediction == 6:
            Outcome = "Asystole"
        elif MI_prediction == 7:
            Outcome = "Ventricular Fibrillation"

    st.success(Outcome)



