from autoloader import AutoLoader
from response import Response

if __name__ == '__main__':
	commands = AutoLoader.load_commands()
	response = {
			"command": "stereo_control",
			"keywords": ["change"],
			"full_text": "turn on the tv and the living room lights"
	}
	for key in commands.keys():
		commands[key].execute(Response(response))
		print(commands[key].examples())
