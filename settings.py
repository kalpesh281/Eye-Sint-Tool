# from os import getenv, path
# from json import loads
# # D:\project
# home = getenv('HOME')
# usr_data = f'D:\project\output\output'
# # conf_path = f'{home}/.config/finalrecon'
# conf_path = f'D:\project\conf'
# path_to_script = path.dirname(path.realpath(__file__))
# src_conf_path = f'{path_to_script}/conf/'
# meta_file_path = f'{path_to_script}/metadata.json'
# keys_file_path = f'{conf_path}/keys.json'
# conf_file_path = f'{conf_path}/config.json'

# if path.exists(conf_path):
#     pass
# else:
#     from shutil import copytree
#     copytree(src_conf_path, conf_path, dirs_exist_ok=True)

# with open(conf_file_path, 'r') as config_file:
#     config_read = config_file.read()
#     config_json = loads(config_read)

#     ssl_port = config_json['ssl_cert']['ssl_port']

#     export_fmt = config_json['export']['format']
# D:\project\output
import os
from os import getenv, path
from json import loads

# Use os.path.join() to construct paths
home = getenv('HOME')
# usr_data = path.join('D:', 'project', 'output', 'output')
# conf_path = path.join('D:', 'project', 'conf')
# usr_data = r'D:\project\output'
# conf_path = r'D:\project\conf'

# Define the common parts of your paths
common_data_dir = 'output'
common_conf_dir = 'conf'

# Determine the base directory depending on the OS
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full paths
usr_data = os.path.join(base_dir, common_data_dir)
conf_path = os.path.join(base_dir, common_conf_dir)
path_to_script = path.dirname(path.realpath(__file__))
src_conf_path = path.join(path_to_script, 'conf')
meta_file_path = path.join(path_to_script, 'metadata.json')
keys_file_path = path.join(conf_path, 'keys.json')
conf_file_path = path.join(conf_path, 'config.json')

if path.exists(conf_path):
    pass
else:
    from shutil import copytree
    copytree(src_conf_path, conf_path, dirs_exist_ok=True)

with open(conf_file_path, 'r') as config_file:
    config_read = config_file.read()
    config_json = loads(config_read)

    ssl_port = config_json['ssl_cert']['ssl_port']

    export_fmt = config_json['export']['format']
