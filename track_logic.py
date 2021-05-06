import calculator as calculate
import coordinates
import godot_communicator
import json

GODOT_IP = '127.0.0.1'
LISTENER_PORT = 4242
UPDATE_INTERVAL = 1 / 60
VELOCITY_MODIFIER = 70


class Car:
    def __init__(self, track, cpu_controlled):
        self.name = "cpuCar" if cpu_controlled else "playerCar"
        self.velocity = 0
        self.track = track
        self.x, self.y = coordinates.extract_x_and_y_values_lists(track)
        self.coordinateIndex = 0
        self.coordinate = {'x': self.x[self.coordinateIndex],
                           'y': self.y[self.coordinateIndex],
                           'coordinate_reached': True}
        self.position = 1
        self.CpuControlled = cpu_controlled
        self.derailed = False
        self.lap = 0
        self.best_lap = -1
        self.last_lap = -1
        self.progress = "0/3"

    def is_accelerating(self, data):
        if self.CpuControlled:
            return True if b'cpu_space' in data else False
        else: 
            return True if b'space' in data else False

    def check_for_reset(self, data):
        if data:
            if self.CpuControlled:
                self.derailed = False if b'cpu_reset' in data else True
            else: 
                self.derailed = False if b'reset' in data else True
                
    def is_derailed(self):
        i = self.coordinateIndex
        radius = calculate.radius(self.x[i], self.y[i], self.x[i - 1], self.y[i - 1], self.x[i - 2], self.y[i - 2])
        centripetal_force = calculate.centripetal_force(self.velocity, radius)
        return calculate.is_derailed(centripetal_force)

    def derail(self):
        print("DERAILED")
        self.velocity = 0
        self.coordinate = {'x': self.x[0], 'y': self.y[0], 'coordinate_reached': True}
        self.coordinateIndex = 0
        self.derailed = True
        return 'derailed'

    def update_velocity(self, new_data):
        #self.velocity = get_new_velocity(self.velocity, self.is_accelerating(new_data) if new_data else False)
        if new_data:
            self.velocity = calculate.velocity(self.velocity, VELOCITY_MODIFIER if self.is_accelerating(new_data) else 0)
        else:
            self.velocity = calculate.velocity(self.velocity, 0)

    def calculate_position(self):
        i = self.coordinateIndex
        next_coord = i + 1 if i + 1 < len(self.track) else 0
        self.coordinate = calculate.new_position(self.velocity,
                                                 self.coordinate['x'],
                                                 self.x[next_coord],
                                                 self.coordinate['y'],
                                                 self.y[next_coord],
                                                 UPDATE_INTERVAL)
        if self.coordinate['coordinate_reached']:
            self.coordinateIndex = next_coord
            if self.coordinateIndex == 0:
                self.lap_complete()
    
    def lap_complete(self):
        self.lap = self.lap+1
        print("Laps completed: " + str(self.lap))
        return 0

    def get_dictionary(self):
        dictionary = {
            "name": self.name,
            "velocity": self.velocity,
            "last_lap": self.last_lap,
            "best_lap": self.best_lap,
            "derailed": self.derailed,
            "coordinate": self.coordinate,
            "race_position": self.position,
            "progress": self.progress
        }
        return dictionary


def game_loop(cars):
    # set up communicator
    communicator = godot_communicator.Connection(GODOT_IP, LISTENER_PORT)
    communicator.start_sending(UPDATE_INTERVAL)

    while True:
        new_data = communicator.receive_data()

        message_dictionary = {}
        for car in cars:
            if car.derailed:
                if new_data:
                    car.check_for_reset(new_data)
            else:
                if car.is_derailed():
                    car.derail()
                else:
                    car.update_velocity(new_data)
                    if car.velocity > 0:
                        car.calculate_position()

            message_dictionary[car.name] = car.get_dictionary()

        json_message: str = json.dumps(message_dictionary)
        communicator.set_data(json_message)


if __name__ == "__main__":
    inner_track, outer_track = coordinates.load_tracks()
    playerCar = Car(outer_track, False)
    cpuCar = Car(inner_track, True)

    cars = [playerCar]
    # add CpuCar
    game_loop(cars)
    # run_simulation(outer_track)

