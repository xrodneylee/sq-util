from flask import Flask
from flask import render_template
from flask import request
import logging
from logging.handlers import RotatingFileHandler
import os
import yaml
app = Flask(__name__)

@app.before_first_request
def init_html():
    file = open('qq.html', 'a', encoding='UTF-8')
    file.write('test')
    file.close()
    app.logger.info('Hello world again!')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh')
@app.route('/ssh', methods=['POST'])
def ssh():
    private_key = 'Private Key'
    public_key = 'Public Key'
    cmd = request.form.get('cmd')
    keysize = request.form.get('keysize')

    if request.method == 'POST':
      os.system(cmd + keysize)
      f = open('id_rsa', 'r')
      private_key = f.read()
      f = open('id_rsa.pub', 'r')
      public_key = f.read()
      f.close()
      os.remove('id_rsa')
      os.remove('id_rsa.pub')
      
    return render_template('ssh.html', private_key=private_key, public_key=public_key)

@app.route('/gunpg')
def gunpg():
    html = 'index'
    stream = open('config.yaml', 'r')
    data = yaml.load(stream)
    app.logger.info(data)
    return render_template('ssh.html', private_key=data)

if __name__ == '__main__':
    app.run(debug=True)
