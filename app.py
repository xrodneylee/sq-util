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
      html_str = '{% extends "index.html" %}\n'
      html_str += '{% block content %}\n'
      html_str += '<h1>' + service + '</h1>\n'
      html_str += '<div class="console">\n'
      html_str += '<form class="pure-form pure-form-aligned" action="/' + service + '" method="post">\n'
      html_str += '<fieldset>\n'
      html_str += '<legend>Input</legend>\n'

      for element in data[service]:
        
        if element == 'description':
          html_str += '<div class="pure-control-group">\n'
          html_str += '<label>' + element + '</label>\n'
          html_str += '<span>' + data[service][element] + '</span>\n'
          html_str += '</div>\n'

        elif element == 'input':
          for field in data[service][element]:
            if data[service][element][field]['tag'] == 'button':
              html_str += '<div class="pure-controls">\n'
              html_str += '<input name="action" class="pure-input-1-3" value="' + data[service][element][field]['action'] + '" hidden>\n'
              html_str += '<button type="submit" class="pure-button pure-button-primary">' + data[service][element][field]['name'] + '</button>\n'
              html_str += '</div>\n'
            elif data[service][element][field]['tag'] == 'select':
              html_str += '<div class="pure-control-group">\n'
              html_str += '<label>' + data[service][element][field]['name'] + '</label>\n'
              html_str += '<select name="' + data[service][element][field]['variable'] + '" class="pure-input-1-3">\n'
              for option in data[service][element][field]['option']:
                html_str += '<option value="' + str(option) + '">' + str(option) + '</option>\n'
              html_str += '</select>\n'
              html_str += '</div>\n'
            elif data[service][element][field]['tag'] == 'input':
              html_str += '<div class="pure-control-group">\n'
              html_str += '<label>' + data[service][element][field]['name'] + '</label>\n'
              html_str += '<input name="' + data[service][element][field]['name'] + '" class="pure-input-1-3" type="' + data[service][element][field]['type'] + '">\n'
              html_str += '</div>\n'

        else:
          pass

      html_str += '</fieldset>\n'
      html_str += '</form>\n'
      html_str += '<form class="pure-form pure-form-aligned">\n'
      html_str += '<fieldset>\n'
      html_str += '<legend>Output</legend>\n'

      for element in data[service]:
        
        if element == 'output':
          for field in data[service][element]:
            if data[service][element][field]['tag'] == 'textarea':
              html_str += '<div class="pure-control-group">\n'
              html_str += '<label>' + data[service][element][field]['name'] + '</label>\n'
              html_str += '<textarea class="pure-input-1-2" style="height: 150px" readonly>{{result}}</textarea>\n'
              html_str += '</div>\n'
            else:
              pass

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
    if request.method == 'POST':
      action=request.form.get('action')
      result = ''
      for key in request.form:
        if key != 'action':
          app.logger.info(key + '=' + request.form.get(key))
          action = str(action).replace('$'+key, request.form.get(key))
      os.system(action)
      for file in data[service]['output']['result']['content']:
        f = open(file, 'r')
        result += f.read() + '\n\n\n\n\n'
      f.close()
      for file in data[service]['output']['result']['content']:
        os.remove(file)      
      return render_template(service + '.html', menu=data, result=result)
    elif service:
      return render_template(service + '.html', menu=data)
    return render_template('index.html', menu=data)

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
