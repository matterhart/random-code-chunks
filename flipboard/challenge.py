import urllib2
import json
import urlparse
from random import randint

## Globals##
base_url = 'https://challenge.flipboard.com/'
start_path = base_url + 'start'
step_path = base_url + 'step?'
check_path = base_url + 'check?'

curr_coordinate = {
	'x': 0,
	'y': 0
}
last_coordinate = {
	'x': 0,
	'y': 0
}
maze_id = ''
solution_string = ''

def start_maze():
	global maze_id

	# Query for maze start
	response = urllib2.urlopen(start_path)
	start_values = json.loads(response.read())

	# Parse maze string from response url
	url = response.geturl()
	url_query = urlparse.urlparse(url).query
	parsed_dict = urlparse.parse_qs(url_query)

	maze_id = parsed_dict['s'][0]

	print('\nStarting solution for maze: ' + maze_id + '\n')

	# Return the available moves from (0,0) for this maze
	return start_values

def pick_move(available_moves):
	# This function will either return the only available move
	# Or it will pick one at random that isn't the current coordinate
	# Nor the last coordinate we came from to avoid a loop
	if len(available_moves) == 1:
		return available_moves[0]
	else :
		while True:
			move = available_moves[randint(0, len(available_moves) - 1)]
			if move != curr_coordinate and move != last_coordinate:
				return move

def make_move(next_coordinate,curr_values):
	global curr_coordinate,last_coordinate,solution_string
	# If move is to deadend, return to previous point and log
	# Else continue on the path
	print(' 	Try Move To: (' + str(next_coordinate['x']) + ',' + str(next_coordinate['y']) + ')')

	url = step_path + 's=' + maze_id + '&x=' + str(next_coordinate['x']) + '&y=' + str(next_coordinate['y'])
	response = urllib2.urlopen(url)
	check_values = json.loads(response.read())

	if len(check_values['adjacent']) == 1:
		print(' 	DEADEND')
		solution_string += check_values['letter']
		last_coordinate = {
			'x': check_values['adjacent'][0]['x'],
			'y': check_values['adjacent'][0]['y']
		}
		return curr_values 
	else :
		last_coordinate = curr_coordinate
		curr_coordinate = next_coordinate
		return check_values

# Begin the fun here, getting our first point for a random maze
curr_values = start_maze()

while curr_values['end'] == False:
	# Loop until we hit a success
	print('At: (' + str(curr_coordinate['x']) + ',' + str(curr_coordinate['y']) + ') Letter:' + curr_values['letter'] + '\n')
	solution_string += curr_values['letter']
	next_coordinate = pick_move(curr_values['adjacent'])
	curr_values = make_move(next_coordinate,curr_values)

# Catch last point's letter for string path
solution_string += curr_values['letter']
print '\nMaze Id: '+maze_id
print 'Solution String: '+solution_string
print ''+check_path + 's=' + maze_id + '&guess=' + solution_string + '\n'