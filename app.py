from flask import Flask
from flask import render_template
# from flask import request
from logging.handlers import RotatingFileHandler
import logging
# import os
import yaml
# import yamlordereddictloader

app = Flask(__name__)
templates_path = 'templates/'
config_file = 'template.yaml'
stream = open(config_file, 'r')#, Loader=yamlordereddictloader.Loader
data = yaml.safe_load(stream)

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.before_first_request
def init_html():
    for service in data:
      app.logger.info('init html=' + service)
      html_str = '{% extends "index.html" %}'
      html_str += '{% block content %}'
      html_str += '<h1>' + service + '</h1>'
      html_str += '<div class="console">'
      html_str += '<form class="pure-form pure-form-aligned" action="/' + service + '" method="post">'
      html_str += '<fieldset>'
      html_str += '<legend>Input</legend>'

      for element in data[service]:
        

        if element == 'description':
          html_str += '<div class="pure-control-group">'
          html_str += '<label>' + element + '</label>'
          html_str += '<span>' + data[service][element] + '</span>'

        elif element == 'input':
          for fields in data[service][element]:
            if fields == 'button':
              html_str += '<div class="pure-controls">'
              html_str += '<button type="submit" class="pure-button pure-button-primary">' + data[service][element][fields]['name'] + '</button>'
              html_str += '</div>'
            else:
              html_str += '<div class="pure-control-group">'
              html_str += '<label>' + fields + '</label>'
              for field in data[service][element][fields]:
                if field == 'tag':
                  html_str += '<select class="pure-input-1-3">'
                elif field == 'option':
                  for option in data[service][element][fields][field]:
                    html_str += '<option>' + str(option) + '</option>'
                  html_str += '</select>'
            

        elif element == 'output':
          pass
        else:
          app.logger.info(element + ' is wrong configuration!')

        html_str += '</div>'

      html_str += '</fieldset>'
      html_str += '</form>'
      html_str += '<form class="pure-form pure-form-aligned">'
      html_str += '<fieldset>'
      html_str += '<legend>Output</legend>'



      html_str += '</fieldset>'
      html_str += '</form>'
      html_str += '</div>'
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
      return render_template(service + '.html', menu=data)
    return render_template('index.html', menu=data)

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
