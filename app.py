from flask import Flask
from flask import render_template
import os
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ssh')
def ssh():
    return render_template('ssh.html')

@app.route('/gunpg')
def gunpg():
    return render_template('gunpg.html')

@app.route('/test', methods=['GET'])
def test():
	os.system("ssh-keygen -t rsa -b 4096 -f temp.rsa -N ''")
	return render_template('ssh.html', private_key='qq', public_key='qq')

if __name__ == '__main__':
    app.run(debug=True)
