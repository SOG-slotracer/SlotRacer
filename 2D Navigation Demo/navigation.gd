extends Navigation2D

export(float) var character_speed = 100000.0 #Pixels / second
var path = []
var socket
var communicator
var thread
var server_ip ="127.0.0.1"
var port = 4242
var start_tick
var close_game


class Communication:
	var _server_ip
	var _port
	var socket
	
	func _init(server_ip = "127.0.0.1", port=4242):
		self._server_ip = server_ip
		self._port = port
	
	func start_communication():
		self.socket = PacketPeerUDP.new()
		self.socket.set_dest_address(self._server_ip, self._port)
		self.socket.put_packet("Started socket. Port 4242".to_ascii())


class car:
	var _fuel
	var _color
	var _position_track
	var _speed

	func _init(fuel=0, color='RED', position_track=0, speed=300):
		self._fuel = fuel
		self._color = color
		self._position_track = position_track
		self._speed = speed


func _physics_process(delta): # delta is 60Hz in _physics_process
	var walk_distance = character_speed * delta # this gives pixels/frame
	move_along_path(walk_distance)
	
	if Input.is_key_pressed(KEY_SPACE):
		if not start_tick:
			start_timer()
		communicator.socket.put_packet("space".to_ascii())
	
	update_timer()


func _exit_tree():
	thread.wait_to_finish()


func _thread_function(userdata):
	print("A new thread for communication is created ", communicator.socket)
	while true:
		if close_game:
			return
		var data:String = (communicator.socket.get_packet().get_string_from_ascii())
		if data:
			print(data)
			
			# var dictionary: Dictionary = JSON.parse(data).result
			# print(dictionary)
			# update_car_classes(dictionary)
			
			if data == "derailed":
				#If cart is derailed, game stops
				$Derailed.visible = true
				print("derailed!")
				start_tick = 0
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
				_update_navigation_path($Car2.position, Vector2(x, y))


func _input(event):
	# The 'click' event is a custom input action defined in
	# Project > Project Settings > Input Map tab.
	if event.is_action_pressed("r"):
		$Derailed.visible = false
		start_tick = 0
		communicator.socket.put_packet("reset".to_ascii())
	
	if event.is_action_pressed("esc"):
		communicator.socket.close()
		close_game = true # ensures thread to close
		get_tree().quit()


func update_car_classes(data):
	return data


func start_timer():
	start_tick = OS.get_ticks_msec()


func update_timer():
	if start_tick:
		var current_time = OS.get_ticks_msec() - start_tick
		current_time = format_time(current_time)
		$Control/Legend2/PanelContainer/Timerlabel.text = current_time


func format_time(time):
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


func move_along_path(distance): #Distance is pixels required to be traversed in this frame
	var last_point = $Car2.position
	while path.size(): #Path is an array of points that led us to the current position
		var distance_between_points = last_point.distance_to(path[0])
		# The position to move to falls between two points.
		if distance <= distance_between_points:
			$Car2.position = last_point.linear_interpolate(path[0], distance / distance_between_points)
			return
		# The position is past the end of the segment.
		distance -= distance_between_points
		last_point = path[0]
		path.remove(0)
	# The character reached the end of the path.
	$Car2.position = last_point
	set_physics_process(false)


func _update_navigation_path(start_position, end_position):
	# get_simple_path is part of the Navigation2D class.
	# It returns a PoolVector2Array of points that lead you
	# from the start_position to the end_position.
	path = get_simple_path(start_position, end_position, true)
	# The first point is always the start_position.
	# We don't need it in this example as it corresponds to the character's position.
	path.remove(0)
	set_physics_process(true)


func _init():
	communicator = Communication.new("127.0.0.1",4242)
	communicator.start_communication()
	return
	# socket = PacketPeerUDP.new()
	# socket.set_dest_address(server_ip, port)
	# socket.put_packet("Started socket. Port 4242".to_ascii())


func _on_Button_pressed():
	pass # Replace with function body.


func _on_Port_text_entered(new_text):
	pass # Replace with function body.


func _ready():
	thread = Thread.new()
	# Third argument is optional userdata, it can be any variable.
	thread.start(self, "_thread_function", "sogeti")

