#LATEST VERSION
import calculator as calculate
import coordinates
import godot_communicator

GODOT_IP = '127.0.0.1'
LISTENER_PORT = 4242
UPDATE_INTERVAL = 1 / 60
VELOCITY_MODIFIER = 70

class Car:
    def __init__(self, track, CpuControlled):
        self.velocity = 0
        self.track = track
        self.x, self.y = coordinates.extract_x_and_y_values_lists(track)
        self.currentCoordinate = 0
        self.position = {'x': self.x[self.currentCoordinate], 'y': self.y[self.currentCoordinate], 'coordinate_reached': True}
        self.CpuControlled = CpuControlled
        self.derailed = False
        self.lap = 0
        self.best_lap = -1
        self.last_lap = -1


    def is_accelerating(self, data):
        if(self.CpuControlled):
            return True if b'cpu_space' in data else False
        else: 
            return True if b'space' in data else False

    def check_for_reset(self, data):
        if data:
            if(self.CpuControlled):
                self.derailed = True if b'cpu_reset' in data else False
            else: 
                self.derailed = True if b'reset' in data else False
                
    def is_derailed(self):
        i = self.currentCoordinate
        radius = calculate.radius(self.x[i], self.y[i], self.x[i - 1], self.y[i - 1], self.x[i - 2], self.y[i - 2])
        centripetal_force = calculate.centripetal_force(self.velocity, radius)
        return calculate.is_derailed(centripetal_force)


    def get_status(self):
        status = ""

        if self.is_derailed():
            print("DERAILED")
            status = 'derailed'
            self.velocity = 0
            self.position = {'x': self.x[0], 'y': self.y[0], 'coordinate_reached': True}
            self.currentCoordinate = 0
            self.derailed = True
    
        else:
            status = str(self.position['x']) + ',' + str(self.position['y'])

        return status


    def update_velocity(self, new_data):
        self.velocity = get_new_velocity(self.velocity, self.is_accelerating(new_data) if new_data else False)


    def calculate_position(self):
        i = self.currentCoordinate
        next_coord = i + 1 if i + 1 < len(self.track) else 0
        self.position = calculate.new_position(self.velocity, self.position['x'], self.x[next_coord],
                                        self.position['y'], self.y[next_coord], UPDATE_INTERVAL)
        if self.position['coordinate_reached']:
            self.currentCoordinate = next_coord
            if self.currentCoordinate == 0:
                self.lap_complete()
    
    def lap_complete(self):
        self.lap = self.lap+1
        print("Laps completed: " + str(self.lap))
        
        return 0


    def get_json_msg(derail_status):
        Json_obj = {
            "name": self.name,
            "velocity": self.velocity,
            "last_lap": self.last_lap,
            "best_lap": self.best_lap,
            "derailed": derail_status,
            "coordinate": self.position,
            "race_position": self.position
        }


def game_loop(cars):
    # set up communicator
    communicator = godot_communicator.Connection(GODOT_IP, LISTENER_PORT)
    communicator.start_sending(UPDATE_INTERVAL)

    while(True):
        new_data = communicator.receive_data()
        
        for car in cars:
            if car.derailed:
                    if new_data:
                        car.check_for_reset(new_data)
                    return

            car.update_velocity(new_data)
            if car.velocity > 0:
                car.calculate_position()
                
            status = car.get_status()

        communicator.set_data(status)


def get_new_velocity(old_velocity, is_accelerating):
    return calculate.velocity(old_velocity, VELOCITY_MODIFIER if is_accelerating else 0)


def is_restarting(data):
    return True if b'restart' in data else False


if __name__ == "__main__":
    inner_track, outer_track = coordinates.load_tracks()
    playerCar = Car(outer_track, False)
    cpuCar = Car(inner_track, True)

    cars = [playerCar] #add CpuCar
    game_loop(cars)
    #run_simulation(outer_track)
