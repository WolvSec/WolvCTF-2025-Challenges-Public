from flask import Flask, request, jsonify, render_template
from answer import get_accuracy, predict
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    accuracy = get_accuracy(file_path)
    os.remove(file_path)

    if accuracy > 77.3: # may need to adjust threshold
        return render_template('p1_ifafbsy4yb.html')

    res = {"accuracy" : accuracy}
    res["success"] = "fail"
    return jsonify(res)


@app.route('/comment_gIknS4kq1ht3Ab1TS', methods=['POST'])
def upload_comment():
    comment = request.form.get('comment')
    if not comment:
        return jsonify({"error": "No comment"}), 400
    pred = predict(comment)
    if pred < 0.50 and pred != -1:
        return render_template('p2_gGlNVzhbAMm7s5Ox8zzIyWJYdnb1Q9YO.html')
    res = {"prediction" : pred}
    res["success"] = "fail"
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
