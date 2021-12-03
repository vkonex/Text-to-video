from flask import Flask, render_template, Response, request, redirect, url_for , jsonify
from flask_cors import CORS
import subprocess
import uuid
import os
import aws_upload
from gtts import gTTS, tts
import gtts
from requests import post
from random import choice
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import time
from datetime import datetime
import inference


app = Flask(__name__,static_folder='static')
# cors = CORS(app,resources={r"/*":{"origins":"*"}})

@app.route('/api')
def my_form():
    
    return render_template('index.html')

@app.route('/api/text_to_audio', methods=['POST','GET'])
def text2speech():
    text = request.form['text']
    processed_text = text.lower()    
    tts = gtts.gTTS(processed_text)
    tts.save("files/audio_input/text_to_audio.wav")
    dir = 'static'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    return jsonify({'status':'success','message':'converted successfully'})

@app.route('/api/merge', methods=['POST','GET'])
def lipsync():
    #move or rename file
    ################## 
    template_id = request.form['template_id']
    # 'video_templates/{template_id}.mp4' -> 'files/video_input/3.mp4
    ###################
    file_name = f"{uuid.uuid4().hex}_lip_sync.mp4"
    start_time = datetime.now()
    subprocess.call(f'python3 inference.py --checkpoint_path "checkpoints/wav2lip.pth" --face "files/video_input/{template_id}.mp4" --audio "files/audio_input/text_to_audio.wav" --outfile "static/{file_name}"',shell=True)
    end_time = datetime.now()
    diff = end_time-start_time
    print(diff.seconds)
    ### save the newly created file -> static/{file_name} -> to amazon s3
    aws_upload.upload_file(f"static/{file_name}",'lipsyncvkonex')
    
    return jsonify({'status':'success','message':'converted successfully','filename':file_name,'time':diff.seconds})
 
if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)