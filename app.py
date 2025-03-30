import os, shutil
from zipfile import ZipFile
from io import BytesIO
from flask import Flask, render_template, request, session, send_file
from backend import pipeline
from flask_session import Session
from flask_mail import Mail, Message
app = Flask(__name__, template_folder='./frontend', static_folder="./static")
app.secret_key='jsdbghjkailerfgjhlihugbr'
ALLOWEDEXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', '.xlsx', '.zip'}
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './backend/ticket_documents'
app.config["SESSION_PERMANENT"] = False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'robert.pasca00@e-uvt.ro'
app.config['MAIL_PASSWORD'] = 'zuci nnor fzvi jsww'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
Session(app)


@app.route('/landing')
def landing():
    return render_template('landing.html') 

@app.route('/')
def load_content():
    user_id = session.get('user_id')
    if user_id:
        if pipeline.is_client(user_id,'_id'):
            return render_template('index.html')
        else: 
            return render_template('panel.html', tickets=pipeline.retrive_tickets(session['user_id'],session['type'])) 
    else:
       return  render_template('landing.html')



@app.route('/index')
def load_index():
    return render_template('index.html')

@app.route('/services')
def load_services():
    return render_template('services.html')

@app.route('/depositary')
def load_depositary():
    return render_template('depositary.html', auditors=pipeline.get_auditors())

@app.route('/cash')
def load_cash():
    return render_template('cash.html', auditors=pipeline.get_auditors())

@app.route('/leads')
def load_leads():
    return render_template('leads.html', auditors=pipeline.get_auditors())

@app.route('/fs')
def load_fs():
    return render_template('fs.html', auditors=pipeline.get_auditors())

@app.route('/kcw')
def load_kcw():
    return render_template('kcw.html', auditors=pipeline.get_auditors())

@app.route('/sr')
def load_sr():
    return render_template('sr.html', auditors=pipeline.get_auditors())

@app.route('/minutes')
def load_minutes():
    return render_template('minutes.html', auditors=pipeline.get_auditors())

@app.route('/swaps')
def load_swaps():
    return render_template('swaps.html', auditors=pipeline.get_auditors())

@app.route('/custom')
def load_custom():
    return render_template('custom.html', auditors=pipeline.get_auditors())

@app.route('/information')
def load_information():
    return render_template('information.html')

@app.route('/panel')
def load_panel():
    return render_template('panel.html', tickets=pipeline.retrive_tickets(session['user_id'],session['type']))

@app.route('/landing')
def load_landing():
    return render_template('landing.html')

@app.route('/signin')
def load_signin():
    return render_template('signin.html')

@app.route('/signup')
def load_signup():
    return render_template('signup.html')


@app.context_processor
def utility_fullname():
    def get_auditor_fullname(id):
       return pipeline.get_auditor_fullname(id)
    return dict(auditor_fullname=get_auditor_fullname)


def create_ticket_folder(name):
    path = str(app.config['UPLOAD_FOLDER']) + '/' + str(session['user_id'])
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + '/' + name
    if not os.path.exists(path):
        os.makedirs(path)           
        os.makedirs(path + '/' + 'input')  
        os.makedirs(path + '/' + 'output')
    path = path + '/' + 'input'
    print(path)
    return path

@app.route('/delete_ticket/<id>/<name>', methods=['GET'])
def delete_ticket(id, name):
    pipeline.delete_ticket(id)
    path = str(app.config['UPLOAD_FOLDER']) + '/' + str(session['user_id']) 
    shutil.rmtree(os.path.join(path, name))
    return app.redirect('/panel')  

@app.route('/auditor_download/<id>/<name>', methods=['GET'])
def auditor_download(id, name):
    path = str(app.config['UPLOAD_FOLDER']) + '/' + str(id) + '/' + name + '/' + 'input'
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
     for filename in os.listdir(path):
       file = os.path.join(path, filename)
       if os.path.isfile(file):
          zf.write(file, os.path.basename(file))
    stream.seek(0)              
    return send_file(stream, as_attachment=True, download_name='archive.zip')

@app.route('/client_download/<name>', methods=['GET'])
def client_download(name):
    path = str(app.config['UPLOAD_FOLDER']) + '/' + str(session['user_id']) + '/' + name + '/' + 'output'
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
     for filename in os.listdir(path):
       file = os.path.join(path, filename)
       if os.path.isfile(file):
          zf.write(file, os.path.basename(file))
    stream.seek(0)              
    return send_file(stream, as_attachment=True, download_name='archive.zip')

@app.route('/auditor_upload/<id>/<name>', methods=['POST'])
def auditor_upload(id, name):
    path = str(app.config['UPLOAD_FOLDER']) + '/' + str(id) + '/' + name + '/' + 'output'
    files = request.files.getlist("files")
    for file in files:
        file.save(os.path.join(path, file.filename))       
    return app.redirect('/panel')

@app.route('/upload_minutes', methods=['POST'])
def upload_minutes():
    path = create_ticket_folder(request.form.get("name"))
    BM = request.files['BM']
    response = pipeline.push_minutes(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),BM.filename)
    if response:
       BM.save(os.path.join(path, BM.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'minutes')
    return app.redirect('/')


@app.route('/upload_custom', methods=['POST'])
def upload_custom():
    path = create_ticket_folder(request.form.get("name"))
    custom = request.files['custom']
    response = pipeline.push_custom(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),custom.filename) 
    if response:
       custom.save(os.path.join(path, custom.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'custom')
    return app.redirect('/')
    

@app.route('/upload_cash', methods=['POST'])
def upload_cash():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    portofolio = request.files['portofolio']
    materiality = request.files['materiality']
    bank_confirmation = request.files['bank_confirmation']
    fx = request.files['fx']
    response = pipeline.push_cash(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename, portofolio.filename, materiality.filename, bank_confirmation.filename, fx.filename)  
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       portofolio.save(os.path.join(path, portofolio.filename))
       materiality.save(os.path.join(path, materiality.filename))
       bank_confirmation.save(os.path.join(path, bank_confirmation.filename))
       fx.save(os.path.join(path, fx.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'cash')
    return app.redirect('/')

@app.route('/upload_depositary', methods=['POST'])
def upload_depositary():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    portofolio = request.files['portofolio']
    materiality = request.files['materiality']
    bank_confirmation = request.files['bank_confirmation']
    response = pipeline.push_depositary(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename, portofolio.filename, materiality.filename, bank_confirmation.filename)  
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       portofolio.save(os.path.join(path, portofolio.filename))
       materiality.save(os.path.join(path, materiality.filename))
       bank_confirmation.save(os.path.join(path, bank_confirmation.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'depositary')
    return app.redirect('/')


@app.route('/upload_fs', methods=['POST'])
def upload_fs():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    response = pipeline.push_fs(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename)   
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'finacial statement')
    return app.redirect('/')

@app.route('/upload_kcw', methods=['POST'])
def upload_kcw():
    path = create_ticket_folder(request.form.get("name"))
    engagement_letter = request.files['engagement_letter']
    san = request.files['san']
    response = pipeline.push_kcw(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),engagement_letter.filename, san.filename)   
    if response:
       engagement_letter.save(os.path.join(path, engagement_letter.filename))
       san.save(os.path.join(path, san.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'kcw')
    return app.redirect('/')


@app.route('/upload_leads', methods=['POST'])
def upload_leads():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    portofolio = request.files['portofolio']
    materiality = request.files['materiality']
    bank_confirmation = request.files['bank_confirmation']
    fx = request.files['fx']
    mapping = request.files['mapping']
    response = pipeline.push_leads(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename, portofolio.filename, materiality.filename, bank_confirmation.filename, fx.filename, mapping.filename)  
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       portofolio.save(os.path.join(path, portofolio.filename))
       materiality.save(os.path.join(path, materiality.filename))
       bank_confirmation.save(os.path.join(path, bank_confirmation.filename))
       fx.save(os.path.join(path, fx.filename))
       mapping.save(os.path.join(path, mapping.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'leads')
    return app.redirect('/')

@app.route('/upload_sr', methods=['POST'])
def upload_sr():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    prospectus = request.files['prospectus']
    materiality = request.files['materiality']
    response = pipeline.push_sr(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename, prospectus.filename, materiality.filename)   
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       prospectus.save(os.path.join(path, prospectus.filename))
       materiality.save(os.path.join(path, materiality.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'separate report')
    return app.redirect('/')

@app.route('/upload_swaps', methods=['POST'])
def upload_swaps():
    path = create_ticket_folder(request.form.get("name"))
    financial_statement = request.files['financial_statement']
    portofolio = request.files['portofolio']
    materiality = request.files['materiality']
    bank_confirmation = request.files['bank_confirmation']
    response = pipeline.push_swaps(request.form.get('name'),session['user_id'],request.form.get('hours'),request.form.get('independante'),request.form.get('auditor'),financial_statement.filename, portofolio.filename, materiality.filename, bank_confirmation.filename)  
    if response:
       financial_statement.save(os.path.join(path, financial_statement.filename))
       portofolio.save(os.path.join(path, portofolio.filename))
       materiality.save(os.path.join(path, materiality.filename))
       bank_confirmation.save(os.path.join(path, bank_confirmation.filename))
       send_mail(pipeline.get_auditor_mail(request.form.get('auditor')), pipeline.get_auditor_name(request.form.get('auditor')), 'swaps')
    return app.redirect('/')

@app.route('/update_ticket_state', methods=['POST'])
def update_ticket_state():
    pipeline.update_ticket_state(request.form.get('id'), request.form.get('state')) 
    return app.redirect('/')

@app.route('/signuser', methods=['POST'])
def signuser():
    response = pipeline.sign_user(request.form.get('username'),request.form.get('password'))
    if response:
        session['user_id'] = response['_id']
        session['type'] = response['type']
        return app.redirect('/')
    else:
        return render_template('noaccount.html')

@app.route('/signout', methods=['GET', 'POST'])
def unsignuser():
    user_id = session.get('user_id')
    if user_id:
       session.pop('user_id', None)
    return app.redirect('/')

@app.route('/createuser', methods=['POST'])
def createuser():
    response = pipeline.create_user(request.form.get("username"),request.form.get("password"),request.form.get("email"),request.form.get("fullname"))
    if response:
        session['user_id'] = response
        if not os.path.exists(str(app.config['UPLOAD_FOLDER']) + '/' + str(session['user_id'])):
           os.makedirs(str(app.config['UPLOAD_FOLDER']) + '/' + str(session['user_id']))
    return app.redirect('/')

def send_mail(email, name, procedure):
    msg = Message(subject='New ticket!', sender='robert.pasca00@e-uvt.ro', recipients=[email])
    msg.body = "Hello " + name + ", a new " + procedure + " ticket has just been assigned to you!"
    mail.send(msg)
    return "Message sent!"

if __name__ == "__main__":
    app.run()