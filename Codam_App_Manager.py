#!/usr/bin/env python3
import urllib.request
from pathlib import Path
import json
import sys
import os
import tarfile
import shutil

config_loc = str(Path.home()) + '/Library/Application Support/Codam_app/'
path = config_loc + 'download.cfg'
ins_path = config_loc + 'installs.cfg'

def write_json(j_file):
	with open(path, 'w') as f:
		json.dump(j_file, f)
		f.close()

def write_installs(j_file):
	with open(ins_path, 'w') as f:
		json.dump(j_file, f)
		f.close()

def read_installs():
	try:
		with open(ins_path, 'r') as f:
			j_file = json.load(f)
			f.close()
	except:
		j_file = {}
		j_file['installs'] = []
	return j_file

def create_json():
	print("Installing The Manager")
	of = open(path, 'w')
	data = {}
	data['installs'] = []
	with urllib.request.urlopen("https://api.github.com/repos/nloomans/Codam.app/releases/latest") as url:
		release = json.loads(url.read().decode())
	for asset in release['assets']:
		data['installs'].append({
			'name' : asset['name'].split('.')[0],
			'download' : asset['browser_download_url']
		})
	data['version'] = release['tag_name']
	write_json(data)
	print("Manager Installed")
	return data

def update_elem(j_file, asset):
	found = False
	for inst in j_file['installs']:
		if inst['name'] == asset['name']:
			found = True
			inst['download'] = asset['browser_download_url']
	if not found:
		j_file['installs'].append({
			'name' : asset['name'].split('.')[0],
			'download' : asset['browser_download_url']
		})

def update_json(j_file):
	print("Updating Manager")
	with urllib.request.urlopen("https://api.github.com/repos/nloomans/Codam.app/releases/latest") as url:
		release = json.loads(url.read().decode())
	if (j_file['version'] != release['tag_name']):
		for asset in release['assets']:
			update_elem(j_file, asset)
		j_file['version'] = release['tag_name']
	write_json(j_file)
	print("Manager Updated")

def check_starts():
	if not os.path.exists(config_loc):
		os.makedirs(config_loc)
	try:
		with open(path, 'r') as f:
			j_file = json.load(f)
			f.close()
		update_json(j_file)
	except:
		j_file = create_json()
	return j_file

def check_install(prog):
	try:
		with open(path, 'r') as f:
			j_file = json.load(f)
			f.close()
		for asset in j_file['installs']:
			if prog == asset['name']:
				return True
		return False
	except:
		return False

def add_install_to_config(name, loc):
	j_file = read_installs()
	j_file['installs'].append({
		'name' : name,
		'loc' : loc
	})
	write_installs(j_file)

def install_prog(prog):
	install_loc = str(Path.home()) + '/Applications/'
	if len(sys.argv) == 4:
		install_loc = sys.argv[3]
		if not install_loc.endswith('/'):
			install_loc += '/'
	if not check_install(prog):
		print("Downloading Program")
		urllib.request.urlretrieve(prog['download'], str(Path.home()) + '/goinfre/' + prog['name'] + 'tar.gz')
		print("Program Downloaded")
		print("Installing Program")
		tar = tarfile.open(str(Path.home()) + '/goinfre/' + prog['name'] + 'tar.gz', 'r:')
		tar.extractall(install_loc)
		tar.close()
		os.remove(str(Path.home()) + '/goinfre/' + prog['name'] + 'tar.gz')
		add_install_to_config(prog['name'], install_loc + prog['name'])
		print("Program Installed")

def install(ins, j_file):
	found = False
	for prog in j_file['installs']:
		if prog['name'] == ins:
			found = True
			install_prog(prog)	
	if not found:
		print("App Not Found")

def print_usage():
	print("Usage:")
	print("   " + sys.argv[0] + " install <program name> [Absolute Install Location]")
	print("   " + sys.argv[0] + " remove <program name>")
	print("   " + sys.argv[0] + " list")
	print("   " + sys.argv[0] + " update")

def list_installs(j_file):
	for pro in j_file['installs']:
		print('Name: ' + pro['name'])

def remove_program(loc):
	found = False
	j_file = read_installs()
	for prog in j_file['installs']:
		if prog['name'] == loc:
			found = True
			shutil.rmtree(prog['loc'] + '.app')
			for i in range(len(j_file['installs'])):
				if j_file['installs'][i]['name'] == prog['name']:
					del j_file['installs'][i]
					write_installs(j_file)
					break
				
	if not found:
		print("Program Not Found")

if __name__ == "__main__":
	if len(sys.argv) != 3 and len(sys.argv) != 2:
		print_usage()
		exit()
	j_file = check_starts()
	if len(sys.argv) == 2 and sys.argv[1] == 'list':
		list_installs(j_file)
	elif len(sys.argv) == 2 and sys.argv[1] != 'update':
		print_usage()
		exit()
	if sys.argv[1] == 'install':
		install(sys.argv[2], j_file)
		exit()
	elif sys.argv[1] == 'remove':
		remove_program(sys.argv[2])
		exit()

