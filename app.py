from flask import Flask
from flask import render_template
from flask import request
from logging.handlers import RotatingFileHandler
import logging
import os
import yaml

app = Flask(__name__)
templates_path = 'templates/'
config_file = 'template.yaml'

@app.before_first_request
def init_html():
    stream = open(config_file, 'r')
    data = yaml.safe_load(stream)
    for service in data:
      app.logger.info('init html=' + service)
      html_str = '{% extends "index.html" %}\n'
      html_str += '{% block content %}\n'
      html_str += '<h1>' + service + '</h1>\n'
      html_str += '<div class="console">\n'
      html_str += '<form class="pure-form pure-form-aligned" action="/' + service + '" method="post">\n'
      html_str += '<fieldset>\n'
      html_str += '<legend>Input</legend>\n'

      for element in data[service]:
        html_str += '<div class="pure-control-group">\n'
        html_str += '<label>' + element + '</label>'
        html_str += '<span>' + element + '</span>'
        # if element == 'description':
        #   html_str += ''


      html_str += '</fieldset>\n'
      html_str += '</form>\n'
      html_str += '<form class="pure-form pure-form-aligned">'
      html_str += '<fieldset>\n'
      html_str += '<legend>Output</legend>\n'



      html_str += '</fieldset>\n'
      html_str += '</form>\n'
      html_str += '</div>\n'
      html_str += '{% endblock content %}'
      file = open(templates_path + service + '.html', 'w', encoding='UTF-8')
      file.write(html_str)

    file.close()

@app.route('/')
@app.route('/<service>')
@app.route('/<service>', methods=['POST'])
def index(service=None):
    app.logger.info('request url=' + str(service))
    if service:
      return render_template(service + '.html')
    return render_template('index.html')

# @app.route('/ssh')
# @app.route('/ssh', methods=['POST'])
# def ssh():
#     private_key = 'Private Key'
#     public_key = 'Public Key'
#     cmd = request.form.get('cmd')
#     keysize = request.form.get('keysize')

#     if request.method == 'POST':
#       os.system(cmd + keysize)
#       f = open('id_rsa', 'r')
#       private_key = f.read()
#       f = open('id_rsa.pub', 'r')
#       public_key = f.read()
#       f.close()
#       os.remove('id_rsa')
#       os.remove('id_rsa.pub')
      
#     return render_template('ssh.html', private_key=private_key, public_key=public_key)

# @app.route('/gunpg')
# def gunpg():
#     app.logger.info(request)
#     return render_template('gunpg.html')

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
