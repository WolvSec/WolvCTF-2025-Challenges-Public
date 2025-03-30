from flask import Flask, request, send_from_directory, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from apscheduler.schedulers.background import BackgroundScheduler
from ocr import ocr_db
import os
import uuid
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = load_model('model.h5')

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def clear_uploads_folder():
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error while clearing the uploads folder: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=clear_uploads_folder, trigger='interval', minutes=5)  # Run every 5 minutes, clear the images
scheduler.start()

@app.route('/')
def index():
    return send_from_directory('static', 'void.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {'success': False}, 400
    
    file = request.files['file']
    if file.filename == '':
        return {'success': False}, 400
    
    fname = str(uuid.uuid4()) + '_' + file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    file.save(file_path)
    trashtype = safety_check(file_path, model)
    if trashtype == 'paper' or trashtype == 'cardboard': 
        d = ocr_db(file_path)
        # Return JSON so the frontend can handle the redirect
        return {
            'success': True,
            'filename': fname,
            'type': trashtype,
            'data': d
        }
    else:
        return {
            'success': False,
            'filename': fname,
            'type': trashtype,
            'data': "abc"
        }

@app.route('/result')
def result():
    filename = request.args.get('filename')
    trashtype = request.args.get('trashtype')
    data = request.args.get('data')
    # Render the result page with the given data
    return render_template('result.html', filename=filename, trashtype=trashtype, data=data)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def safety_check(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array.reshape(1, 224, 224, 3) 

    predictions = model.predict(img_array)
    predicted_class = predictions.argmax()

    classes = ['metal', 'glass', 'paper', 'trash', 'cardboard', 'plastic']
    return classes[predicted_class]
    # pizza boxes or napkins only




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
