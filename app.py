
import gradio as gr
import joblib as jb
import pandas as pd


pipe = jb.load('heart1.pkl')






def predict(age,	sex,	cp,	trtbps,	chol,	fbs,	restecg,	thalachh,	exng,	oldpeak,	slp,	caa,	thall):
    if sex=="Male":
      sex=1
    else:
      sex=0

    if cp=="Typical Angina":
      cp=0
    elif cp=="Typical Angina":
      cp=1
    elif cp=="Atypical Angina":
      cp=2
    elif cp=="Non-Anginal pain":
      cp=3
    elif cp=="Asymptomatic":
      cp=4
    else:
      cp=0

    if fbs>120:
      fbs=1
    else:
      fbs=0

    if restecg=="Normal":
      restecg=0
    elif restecg=="ST-T wave abnormality":
      restecg=1
    elif restecg=="Definite left Ventricular hypertrophy":
      restecg=2
    else:
      restecg=0

    if slp=="Unsloping":
      slp=0
    elif restecg=="flat":
      slp=1
    elif restecg=="Downsloping":
      slp=2
    else:
      slp=0
    
    if exng=="Yes":
      exng=1
    else:
      exng=0
    
    if thall=="Null":
      thall=0
    elif thall=="Fixed defect":
      thall=1
    elif cp=="Normal":
      thall=2
    elif cp=="Reversable defect":
      thall=3
    else:
      thall=0

    
    x = pd.DataFrame([[age,	sex,	cp,	trtbps,	chol,	fbs,	restecg,	thalachh,	exng,	oldpeak,	slp,	caa,	thall]])
    x.columns = ["age",	"sex",	"cp",	"trtbps",	"chol",	"fbs",	"restecg",	"thalachh",	"exng",	"oldpeak",	"slp",	"caa",	"thall"]
    prediction = pipe.predict(x)

    ans = prediction[0]
    
    if ans>=1:
      ans = 100
    elif ans<=0:
      ans = 0
    else:
      ans = ans*100 

    if ans>50:
      final = str(int(ans)) + "%" +"\n>50% Diameter narrowing.\nMore chance of heart disease."
    else:
      final = str(int(ans)) + "%" + "\n< 50% Diameter narrowing.\nLess chance of heart disease."


    return final



app = gr.Interface(title="Heart Attack Predictor",fn=predict, 
        inputs=[
        gr.inputs.Number(label='Age'), 
        gr.inputs.Radio(["Male","Female"],label='Sex'),
        gr.inputs.Radio(["Typical Angina","Atypical Angina","Non-Anginal pain","Asymptomatic"],label='Chest Pain'),
        gr.inputs.Number(label='Resting blood pressure (in mm Hg)'),
        gr.inputs.Number(label='Cholestoral in mg/dl '),
        gr.inputs.Number(label='Fasting blood sugar'),
        gr.inputs.Radio(["Normal","ST-T wave abnormality","Definite left Ventricular hypertrophy"],label='Resting Rlectrocardiographic Results'),
        gr.inputs.Number(label='Maximum Heartrate achieved'),
        gr.inputs.Radio(["Yes","No"],label='Exercise induced Angina'),
        gr.inputs.Number(label='ST depression induced by exercise'),
        gr.inputs.Radio(["Unsloping","flat","Downsloping"],label='Slope of the peak exercise ST segment'),
        gr.inputs.Slider(minimum=0,maximum=3,step=1,label='Number of major vessels'),
        gr.inputs.Radio(["Null","Fixed defect","Normal","Reversable defect"],label='Thalassemia'), 
    ],
    outputs=gr.outputs.Textbox(label="Prediction")
)   



app.launch()

