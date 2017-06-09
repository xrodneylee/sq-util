from flask import Flask
from flask import render_template
from flask import request
import os
import yaml
app = Flask(__name__)


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

    return render_template('ssh.html', private_key=data)

if __name__ == '__main__':
    app.run(debug=True)
