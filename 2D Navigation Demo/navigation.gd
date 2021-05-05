extends Navigation2D

var path = []
var communicator
var thread
var start_tick
var close_game
var cars

var SERVER_IP ="127.0.0.1"
var PORT = 4242
var CHARACTER_SPEED = 100000

var exampleJSON: String = '{"eBooks":[{"language":"Pascal","edition":"third"}'\
+ ',{"language":"Python","edition":"four"},{"language":"SQL","edition":"second"}]}'
var realExampleJSON: String = '{"playerCar": {"name": "playerCar", "velocity":'\
+ ' 15, "derailed": false, "coordinate": "1,1", "race_position": 1}, "cpuCar": '\
+ '{"name": "cpuCar", "velocity": 15, "derailed": true, "coordinate": "2,2", '\
+ '"race_position": 2}}'

class Communication:
	var server_ip
	var port
	var socket
	
	func _init(server_ip = "127.0.0.1", port=4242):
		self.server_ip = server_ip
		self.port = port
	
	func start_communication():
		self.socket = PacketPeerUDP.new()
		self.socket.set_dest_address(self.server_ip, self.port)
		self.socket.put_packet("Started socket. Port 4242".to_ascii())


class Car:
	var name
	var velocity
	var derailed
	var coordinate
	var race_position
	var best_lap
	var last_lap
	
	func _init(name="Car", velocity=0, race_position=0):
		self.name = name
		self.velocity = velocity
		self.race_position = race_position


func _physics_process(delta):
	# delta is 1/60th second
	# walk distance gives pixels / frame
	var walk_distance = CHARACTER_SPEED * delta
	move_along_path(walk_distance)
	
	send_throttle_on_space()
	
	update_timer()


func thread_check_incoming(userdata):
	while true:
		if close_game:
			return # close thread upon closing of game
		var data = get_data()
		if data:
			print(data)
			
			var dictionary: Dictionary = JSON.parse(realExampleJSON).result
			# print(dictionary["eBooks"][0]["edition"])
			# var dictionary: Dictionary = JSON.parse(data).result
			# var dictionary
			update_car_classes(dictionary)
			update_info_grid()
			print(is_derailed(dictionary))
			
			
			if data == "derailed":
				#If cart is derailed, game stops
				$Derailed.visible = true
				print("derailed!")
				reset_timer()
			else:
				var position_array = data.rsplit(",", true, 6)
				var x = position_array[0]
				var y = position_array[1]
				if position_array.size() == 7:
					$GridContainer/PositionCar1.text = position_array[2]
					$GridContainer/SpeedCar1.text = position_array[3]
					$GridContainer/LastLapCar1.text = position_array[4]
					$GridContainer/BestLapCar1.text = position_array[5]
					$GridContainer/ProgressCar1.text = position_array[6]
				update_navigation_path($cpuCar.position, Vector2(x, y))


func _input(event):
	# events are defined in: Project > Project Settings > Input Map tab
	if event.is_action_pressed("r"):
		$Derailed.visible = false
		reset_timer()
		communicator.socket.put_packet("reset".to_ascii())
	
	if event.is_action_pressed("esc"):
		communicator.socket.close()
		close_game = true # ensures thread to close
		get_tree().quit()


func send_throttle_on_space():
	if Input.is_key_pressed(KEY_SPACE):
		if not start_tick:
			# only start timer if not yet started
			start_timer()
		communicator.socket.put_packet("space".to_ascii())


func get_data():
	return communicator.socket.get_packet().get_string_from_ascii()


func update_car_classes(data):
	print(cars[0].velocity)
	print(cars[1].velocity)
	# car classes should be updated with data in JSON format
	for car in cars:
		for variable in car.get_property_list():
			if variable.usage == 8192 && variable.name in data[car.name]:
				# All properties are given, but only properties with usage 8192
				# are variables of the class.
				# Variable is only updated if it present in JSON message
				car[variable.name] = data[car.name][variable.name]


func update_info_grid():
	# pushes the information from car classes into the grid container
		pass


func is_derailed(data):
	for car in cars:
		if data[car.name]['derailed'] == true:
			return true
	return false


func start_timer():
	start_tick = OS.get_ticks_msec()


func update_timer():
	if start_tick: # only start showing the time if the timer started
		var current_time = OS.get_ticks_msec() - start_tick
		$Control/Legend2/PanelContainer/Timerlabel.text = ms_To_mm_ss_msmsms(current_time)


func reset_timer():
	start_tick = 0


func ms_To_mm_ss_msmsms(time):
	var digits = []
	var minutes = "%02d" % [time / 60000]
	digits.append(minutes)
	var seconds = "%02d" % [time / 1000]
	digits.append(seconds)
	var milliseconds = "%03d" % [int(ceil(time)) % 1000]
	digits.append(milliseconds)
	var formatted = String()
	var colon = ":"
	for digit in digits:
		formatted += digit + colon
	if not formatted.empty():
		formatted = formatted.rstrip(colon)
	return formatted


func move_along_path(distance): # Distance is pixels required to be traversed in this frame
	var last_point = $cpuCar.position
	while path.size(): # Path is an array of points that led us to the current position
		var distance_between_points = last_point.distance_to(path[0])
		# The position to move to falls between two points.
		if distance <= distance_between_points:
			$cpuCar.position = last_point.linear_interpolate(path[0], distance / distance_between_points)
			return
		# The position is past the end of the segment.
		distance -= distance_between_points
		last_point = path[0]
		path.remove(0)
	# The character reached the end of the path.
	$cpuCar.position = last_point
	set_physics_process(false)


func update_navigation_path(start_position, end_position):
	# get_simple_path returns a PoolVector2Array of points that lead you
	# from the start_position to the end_position.
	path = get_simple_path(start_position, end_position, true)
	# The first point is always the start_position.
	# We don't need it in this example as it corresponds to the character's position.
	path.remove(0)
	set_physics_process(true)


func _init():
	communicator = Communication.new(SERVER_IP, PORT)
	communicator.start_communication()
	print("A new thread for communication is created ", communicator.socket)
	
	cars = [Car.new("playerCar", 0, 0), Car.new("cpuCar", 0, 1)]
	#print(cars[0].get_property_list())
	#for item in cars[0].get_property_list():
		#if item.usage == 8192:
			#print(item.name)


func _on_Port_text_entered(new_text):
	pass # Replace with function body.


func _ready():
	thread = Thread.new()
	# Third argument is optional userdata, it can be any variable.
	# Thread is used to asynchronously check incoming data
	thread.start(self, "thread_check_incoming", "sogeti")

