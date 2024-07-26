from flask import Flask,render_template,url_for,request
import joblib,os
import pandas as pd
import sqlite3

model_1=joblib.load('./models/linear_model.lb')
model_2=joblib.load('./models/decisiontree.lb')
model_3=joblib.load('./models/randomforest.lb')

app=Flask(__name__)
data_insert_query="""
insert into project(Age,region,Children,Health,sex,smoker,bmi)
values(?,?,?,?,?,?,?)
"""
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=="POST":
        age=request.form['Age']
        region=request.form['region']
        children=request.form['Children']
        health=request.form['Health']
        sex=request.form['sex']
        smoker=request.form['smoker']
        bmindex=request.form['bmi']

        region_northeast=0
        region_northwest=0
        region_southeast=0
        region_southwest=0
        
        if region=='northeast':
            region_northeast=1
        elif region=='northwest':
            region_northwest=1
        elif region=='southeast':
            region_southeast=1
        else:
            region_southwest=1
        
        #ls2=[age,region,children,health,sex,smoker,bmindex]
        
        ls={'age':[age],'sex':[sex],'bmi':[bmindex],'children':[children],'smoker':[smoker],'health':[health],'region_northeast':[region_northeast],'region_northwest':[region_northwest],'region_southeast':[region_southeast],'region_southwest':[region_southwest]}
        df=pd.DataFrame(ls)
        lin_predict=model_1.predict(df)
        dtr_predict=model_2.predict(df)
        rfr_predict=model_3.predict(df)

        prediction={'Linear regression: ':lin_predict[0],'Decision Tree: ':dtr_predict[0],'Random Forest':rfr_predict[0]}
        conn=sqlite3.connect('insurance.db')

        cur=conn.cursor()

        Data=(age,region,children,health,sex,smoker,bmindex)
        cur.execute(data_insert_query,Data)
        conn.commit()
        cur.close()
        conn.close()
        return render_template('final.html',output=lin_predict[0])

if __name__=="__main__":
    app.run(debug=True)
