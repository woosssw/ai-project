from flask import *

import sys
sys.path.append('./model')
from main import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['ORIGINAL_PHOTOS_DEST'] = 'ori_images'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/ori_images/<filename>')
def get_ori_file(filename):
    return send_from_directory(app.config['ORIGINAL_PHOTOS_DEST'], filename)

@app.route('/') 
def main(): 
    return render_template("index.html") 
  
@app.route('/upload', methods=['POST']) 
def upload(): 
    if request.method == 'POST': 
        # Get the list of files from webpage 
        files = request.files.getlist("file") 
  
        # Iterate for each file in the files List, and Save them 
        for file in files: 
            file.save('./uploads/'+file.filename)
        upload_image_name = files[0].filename
        upload_image_path = f'./uploads/{upload_image_name}'
        result = infer(upload_image_path)
        filename_1, filename_2, filename_3, filename_4, filename_5 = result[0][0], result[1][0], result[2][0], result[3][0], result[4][0]
        filename_6, filename_7, filename_8, filename_9, filename_10 = result[5][0], result[6][0], result[7][0], result[8][0], result[9][0]
        sim_1_res, sim_2_res, sim_3_res, sim_4_res, sim_5_res = result[0][1], result[1][1], result[2][1], result[3][1], result[4][1]
        sim_6_res, sim_7_res, sim_8_res, sim_9_res, sim_10_res = result[5][1], result[6][1], result[7][1], result[8][1], result[9][1]
        sim_1, sim_2, sim_3, sim_4, sim_5 = f'{sim_1_res:.1f}%', f'{sim_2_res:.1f}%', f'{sim_3_res:.1f}%', f'{sim_4_res:.1f}%', f'{sim_5_res:.1f}%'
        sim_6, sim_7, sim_8, sim_9, sim_10 = f'{sim_6_res:.1f}%', f'{sim_7_res:.1f}%', f'{sim_8_res:.1f}%', f'{sim_9_res:.1f}%', f'{sim_10_res:.1f}%'
        file_url_0 = url_for('upload_file', filename=upload_image_name)
        file_url_1 = url_for('get_ori_file', filename=filename_1)
        file_url_2 = url_for('get_ori_file', filename=filename_2)
        file_url_3 = url_for('get_ori_file', filename=filename_3)
        file_url_4 = url_for('get_ori_file', filename=filename_4)
        file_url_5 = url_for('get_ori_file', filename=filename_5)
        file_url_6 = url_for('get_ori_file', filename=filename_6)
        file_url_7 = url_for('get_ori_file', filename=filename_7)
        file_url_8 = url_for('get_ori_file', filename=filename_8)
        file_url_9 = url_for('get_ori_file', filename=filename_9)
        file_url_10 = url_for('get_ori_file', filename=filename_10)
        try:
            thres = int(request.form['number'])
        except:
            thres = 0

    return render_template('index.html', file_url_0=file_url_0, file_url_1=file_url_1, 
                           file_url_2=file_url_2, file_url_3=file_url_3, file_url_4=file_url_4,
                           file_url_5=file_url_5, file_url_6=file_url_6, file_url_7=file_url_7,
                           file_url_8=file_url_8, file_url_9=file_url_9, file_url_10=file_url_10,
                           sim_1=sim_1, sim_2=sim_2, sim_3=sim_3, sim_4=sim_4, sim_5=sim_5,
                           sim_6=sim_6, sim_7=sim_7, sim_8=sim_8, sim_9=sim_9, sim_10=sim_10,
                           sim_1_res=sim_1_res, sim_2_res=sim_2_res, sim_3_res=sim_3_res, sim_4_res=sim_4_res, sim_5_res=sim_5_res,
                           sim_6_res=sim_6_res, sim_7_res=sim_7_res, sim_8_res=sim_8_res, sim_9_res=sim_9_res, sim_10_res=sim_10_res,
                           thres=thres)
  
if __name__ == '__main__': 
    app.run(debug=True) 