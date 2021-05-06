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

var ExampleJSON: String = '{"playerCar": {"name": "playerCar", '\
+ '"race_position": 1, "velocity": 12, "last_lap": "undefined", "best_lap": '\
+ '"undefined", "derailed": false, "coordinate": "1,1"}, "cpuCar": {"name": '\
+ '"cpuCar", "race_position": 2, "velocity": 13, "last_lap": "undefined", '\
+ '"best_lap": "undefined", "derailed": false, "coordinate": "2,2"}}'

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
	var progress
	
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
			
			#var dictionary: Dictionary = JSON.parse(ExampleJSON).result
			#data = JSON.parse(data).result
			
			#update_car_classes(data)
			#update_info_grid()
			
			#if is_derailed(data):
				#show_derailed()
			#else:
				#drive_cars()
			
			if data == "derailed":
				#If cart is derailed, game stops
				$Derailed.visible = true
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
	$GridContainer/PositionPlayerCar.text = cars[0].race_position
	$GridContainer/PositionCpuCar.text = cars[1].race_position
	$GridContainer/VelocityPlayerCar.text = cars[0].velocity
	$GridContainer/VelocityCpuCar.text = cars[1].velocity
	$GridContainer/LastLapPlayerCar.text = cars[0].last_lap
	$GridContainer/LastLapCpuCar.text = cars[1].last_lap
	$GridContainer/BestLapPlayerCar.text = cars[0].best_lap
	$GridContainer/BestLapCpuCar.text = cars[1].best_lap
	$GridContainer/ProgressPlayerCar.text = cars[0].progress
	$GridContainer/ProgressCpuCar.text = cars[1].progress


func show_derailed():
	$Derailed.visible = true
	reset_timer()


func drive_cars():
	for car in cars:
		var position_array = split_coordinate_string(car.coordinate)
		var x = position_array[0]
		var y = position_array[1]
		update_navigation_path(get_node(car.name).position, Vector2(x, y))


func split_coordinate_string(string):
	return string.rsplit(",", true, 6)


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
	# setup UDP communication
	communicator = Communication.new(SERVER_IP, PORT)
	communicator.start_communication()
	print("A new thread for communication is created ", communicator.socket)
	
	# initialize two car classes
	cars = [Car.new("playerCar", 0, 0), Car.new("cpuCar", 0, 1)]


func _on_Port_text_entered(new_text):
	pass # Replace with function body.


func _ready():
	thread = Thread.new()
	# Third argument is optional userdata, it can be any variable.
	# Thread is used to asynchronously check incoming data
	thread.start(self, "thread_check_incoming", "sogeti")

