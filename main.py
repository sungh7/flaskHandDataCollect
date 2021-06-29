from flask import Flask, render_template, request, url_for
from flask.wrappers import Request
from markupsafe import escape
from werkzeug.utils import secure_filename
import os, shutil, sqlite3, json, datetime

app = Flask(__name__)
app.secret_key = b'lajsiudofjqew!awf!@#@##$xzicv'
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
db_id_list = ['static/patient_id.txt', 'static/files_id.txt']
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBlob(id, patient_id, filepath, file_blob, video_type, upload_date):
    try:
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()
        sql_insert_blob_query = """ INSERT INTO files (
            id, patient_id, filepath, file_blob, video_type, upload_date) 
            VALUES (?, ?, ?, ?, ?, ?)"""
        blobData = convertToBinaryData(file_blob)
        data_tuple = (id, patient_id, filepath, blobData, video_type, upload_date)
        cursor.execute(sql_insert_blob_query, data_tuple)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def insertPatientData(patient_data):
    try: 
        conn = sqlite3.connect('static/database.db')
        cursor = conn.cursor()
        sql_insert_data_query = """ INSERT INTO patients (
            id, name, age, sex, disease, hand, finger_num, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
        data_tuple = (patient_data['id'], patient_data['name'], patient_data['age'], patient_data['sex'], patient_data['disease'], patient_data['hand'], patient_data['finger_num'], patient_data['description'])
        cursor.execute(sql_insert_data_query, data_tuple)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if conn:
            conn.close()

def countId(path):
    with open(path, 'r') as r:
        id = int(r.read())
    with open(path, 'w') as w:
        w.write(str(id+1))
        w.close()            
    return id 

def makeFolder(patient_id):
    try:
        os.mkdir('static/data/'+str(patient_id))
    except Error as e:
        print(e)
    return 'static/data/'+str(patient_id)

def makeJson(filepath, dic):
    with open(filepath+'/patient_data.json', 'w', encoding='UTF-8-sig') as f:
        json.dump(dic, f, ensure_ascii=False)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files[]")
        print(uploaded_files)
        if len(uploaded_files) <= 10:
            filepaths = []
            patient_id = countId(db_id_list[0])
            filepath = makeFolder(patient_id)
            now = str(datetime.datetime.now())

            for file in uploaded_files:
                filename = file.filename
                file.save(filepath+'/'+filename)
                filepaths.append(filepath+'/'+filename)
                file_id = countId(db_id_list[1])
                video_type=''
                insertBlob(file_id, patient_id, filepath, filepath+'/'+filename, video_type, now)
            patient_data = {
                "id" : patient_id,
                "name" : request.form['patientName'],
                "age" : request.form['patientAge'],
                "sex" : request.form['patientSex'],
                "disease" : request.form['diseaseName'],
                "hand" : request.form['diseaseHand'],
                "finger_num" : request.form['diseaseFinger'],
                "description" : request.form['description'],
                "files" : filepaths
            }
            insertPatientData(patient_data)
            makeJson(filepath, patient_data)   
            return render_template('upload_complete.html')   
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
