from flask import Flask
from flask import render_template
from flask import request
import os
import yaml
app = Flask(__name__)

templates_path = 'templates/'

@app.before_first_request
def init_html():
    stream = open('template.yaml', 'r')
    data = yaml.safe_load(stream)
    for service in data:
      html_str = '{% extends "index.html" %}\n'
      html_str += '{% block content %}\n'
      html_str += '<h1>' + service + '</h1>'
      html_str += '{% endblock content %}'
      file = open(templates_path + service + '.html', 'w', encoding='UTF-8')
      file.write(html_str)
      app.logger.info(service)
      app.logger.info(data[service])
      app.logger.info(html_str)

    file.close()

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

if __name__ == '__main__':
    app.run(debug=True)
