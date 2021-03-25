extends Navigation2D

export(float) var character_speed = 30000.0
var path = []
var socket
var destination
var position_array
var x = 0
var y = 0
var thread
#var server_ip = "192.168.2.42"
var server_ip ="127.0.0.1"
var port = 4242

onready var dynamicTrack2DLine = $DynamicTrackLayer/Line2D

class communication:
	var _server_ip
	var _port
	var _destination_ip
	
	func __init__(server_ip = "127.0.0.1", port=4242, destination_ip="127.0.0.1"):
		self._server_ip = server_ip
		self._port = port
		self._destination_ip = destination_ip

class car:
	var _fuel
	var _color
	var _position_track
	var _speed
	
	func __init__(fuel=0, color='RED', position_track=0, speed=300):
		self._fuel = fuel
		self._color = color
		self._position_track = position_track
		self._speed = speed

func _process(delta):
	var walk_distance = character_speed * delta
	move_along_path(walk_distance)
	var data:String = (socket.get_packet().get_string_from_ascii())

	if data:
		position_array = data.rsplit(",", true, 1)
		x = position_array[0]
		y = position_array[1]
		position = Vector2(x, y)
		_update_navigation_path($Character.position, position) 
		print(position)

func _exit_tree():
	thread.wait_to_finish()

func _thread_function(userdata):
	print("A new thread for communication is created", userdata)
	while true:
		var data:String = (socket.get_packet().get_string_from_ascii())
		if data:
			position_array = data.rsplit(",", true, 6)
			x = position_array[0]
			y = position_array[1]
			if position_array.size() == 7:
				$GridContainer/PositionCar1.text = position_array[2]
				$GridContainer/SpeedCar1.text = position_array[3]
				$GridContainer/LastLapCar1.text = position_array[4]
				$GridContainer/BestLapCar1.text = position_array[5]
				$GridContainer/ProgressCar1.text = position_array[6]

			_update_navigation_path($Character.position, Vector2(x, y)) 
			dynamicTrack2DLine.add_point(Vector2(x, y))
			print(Vector2(x, y))
	

#https://docs.godotengine.org/en/latest/classes/class_packedbytearray.html#class-packedbytearray

# The 'click' event is a custom input action defined in
# Project > Project Settings > Input Map tab.
func _input(event):
	if not event.is_action_pressed("click"):
		return
	#_update_navigation_path($Character.position, get_local_mouse_position())  # destination


func move_along_path(distance):
	var last_point = $Character.position
	while path.size():
		var distance_between_points = last_point.distance_to(path[0])
		# The position to move to falls between two points.
		if distance <= distance_between_points:
			$Character.position = last_point.linear_interpolate(path[0], distance / distance_between_points)
			return
		# The position is past the end of the segment.
		distance -= distance_between_points
		last_point = path[0]
		path.remove(0)
	# The character reached the end of the path.
	$Character.position = last_point
	set_process(false)


func _update_navigation_path(start_position, end_position):
	# get_simple_path is part of the Navigation2D class.
	# It returns a PoolVector2Array of points that lead you
	# from the start_position to the end_position.
	path = get_simple_path(start_position, end_position, true)
	# The first point is always the start_position.
	# We don't need it in this example as it corresponds to the character's position.
	path.remove(0)
	set_process(true)


func _init():
	socket = PacketPeerUDP.new()	
	socket.set_dest_address(server_ip, port)
	socket.put_packet("Hello I am from Sogeti".to_ascii())
	socket.put_packet("What are you doing".to_ascii())


func _on_Button_pressed():
	print("Button Pressed")
	pass # Replace with function body.


func _on_ServerIP_text_entered(new_text):
	print(new_text)	
	pass # Replace with function body.


func _on_Port_text_entered(new_text):
	print(new_text)
	pass # Replace with function body.
	
	
	
	
func _ready():
	thread = Thread.new()
	# Third argument is optional userdata, it can be any variable.
	thread.start(self, "_thread_function", "Sogeti")
