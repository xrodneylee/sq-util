from flask import Flask
from flask import render_template
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh')
@app.route('/ssh/<action>')
def ssh(action=None):
    private_key = 'Private Key'
    public_key = 'Public Key'

    if action:
      os.system("ssh-keygen -t rsa -b 4096 -f id_rsa -N ''")
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
    return render_template('gunpg.html')

if __name__ == '__main__':
    app.run(debug=True)
