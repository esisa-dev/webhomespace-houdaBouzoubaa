import logging
from datetime import datetime
import hashlib
import os
from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for,
    flash,
)
from flask import send_file
from business.userManagement import User

logger = logging.getLogger('HomeSpace')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('logger.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app=Flask(__name__)

def generate_key(user):
    return hashlib.md5(str(user).encode('utf-8')).hexdigest()
app.secret_key='1234'

@app.route('/')
def index():
    return render_template('authenticate.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user=request.form['user']
    passwd=request.form['password']
    #print(passwd)
    #print(user)
    
    if User().userExist(user, passwd):
        dirs = User().ls(user)
        response=app.make_response(render_template('index.html',dirs=dirs))
        session['acces']=user
        response.set_cookie('access_time',str(datetime.now()))
        flash('logged in')
        logger.info(f'{user} logged in')
        return response
    else:
        flash('Invalid password or user')
        logger.info('Invalid password or user')
        return render_template('authenticate.html',error_auth='user not fount or password incorrect')

@app.route('/home', methods=['POST'])
def home():
    if 'acces' in session :
        user = session['acces']
        button = request.form['button']
        if button == 'Files':
            return render_template('index.html', dirs = User().ls(user), nb ='Nombre de fichiers dans ce repertoire : '+ str(User().files(user))) 
        if button == 'Dirs':
            return render_template('index.html', dirs = User().ls(user), nb ='Nombre de repertoires dans ce repertoire : '+ str(User().dirs(user))) 
        if button == 'Space':
            return render_template('index.html', dirs = User().ls(user), nb ='l espace total de ce repertoire: '+ str(User().size(user))) 
        if button == 'Search':
            return render_template('index.html', dirs = User().search(user, request.form['file']))
        if button == 'Load':
            User().zip(user)
            flash('Load')
            logger.info(f'{user} loaded his home directory')
            '''else :
                session['acces'] += '/'+button
                user = session['acces']
                if os.path.isfile(user):
            #if user[-3:] == '.py':
                return render_template('index.html', file = User().cat(user),user = user)
            else:
                return render_template('index.html', dirs = User().ls(user))'''
        else :
            session['acces'] += '/'+button
            user = session['acces']
            #if os.path.exists(user):
            if  os.path.isfile(user):
                return render_template('index.html', file = User().cat(user))
            else:
                return render_template('index.html', dirs = User().ls(user))
            #else:
                #return render_template('index.html', file = 'file does not exist')
                
    else :
        return redirect('/')

@app.route('/logout')
def logout():
    user = session['acces']
    flash('logged in')
    logger.info(f'{user} logged out')
    return render_template('authenticate.html')

if __name__=='__main__':
    app.run(host="0.0.0.0",port=9090,debug=True)