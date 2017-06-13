from flask import Flask
from flask import render_template
from flask import request
from collections import OrderedDict
from logging.handlers import RotatingFileHandler
import logging
import os
import yaml

app = Flask(__name__)
templates_path = 'templates/'
config_file = 'template.yaml'

def ordered_yaml_load(yaml_path, Loader=yaml.Loader,
                    object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path) as stream:
        return yaml.load(stream, OrderedLoader)

data = ordered_yaml_load(config_file)

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
          html_str += '</div>'

        elif element == 'input':
          for tag in data[service][element]:
            if tag == 'button':
              html_str += '<div class="pure-controls">'
              html_str += '<button type="submit" class="pure-button pure-button-primary">' + data[service][element][tag]['name'] + '</button>'
              html_str += '</div>'
            elif tag == 'select':
              html_str += '<div class="pure-control-group">'
              html_str += '<label>' + data[service][element][tag]['name'] + '</label>'
              html_str += '<select class="pure-input-1-3">'
              for option in data[service][element][tag]['option']:
                html_str += '<option>' + str(option) + '</option>'
              html_str += '</select>'
              html_str += '</div>'

        else:
          pass

      html_str += '</fieldset>'
      html_str += '</form>'
      html_str += '<form class="pure-form pure-form-aligned">'
      html_str += '<fieldset>'
      html_str += '<legend>Output</legend>'

      for element in data[service]:
        
        if element == 'output':
          for tag in data[service][element]:
            if tag == 'textarea':
              html_str += '<div class="pure-control-group">'
              html_str += '<label>' + data[service][element][tag]['name'] + '</label>'
              html_str += '<textarea class="pure-input-1-2" style="height: 150px" readonly>{{result}}</textarea>'
              html_str += '</div>'
            else:
              pass

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
