import serial


class WheelController:
    def __init__(self, fd=None):
        self.serial = serial.Serial(fd) if fd is not None else serial.Serial()

    def set_wheel_velocity(self, left_side: float = 0, right_side: float = 0):
        """Send rotational velocity command to the wheel controller.

        The wheel command format is sent to the wheel controller
        in the following format

            set_vel {left_side} {right_side}\\n

        Parameters
        ----------
        left_side
            The angular velocity for the left side wheels
        right_side
            The angular velocity for the right side wheels
        """
        self.serial.write(f'set_vel {left_side} {right_side}\n'.encode())
        pass

    def poll_wheel_velocities(self) -> tuple[float, float]:
        """Request most recent wheel velocities from wheel controller.

        The data request is sent to the controller in the following
            format over serial

            read_vel\\n

        The controller is expected to send back the data in the
            following format

            current_vel {left_side} {right_side}\\n

        Returns
        -------
        tuple[left_side, right_side]
            The angular velocity of the left side wheels and right side wheels.


        The controller is expected to return the values as angular velocity.
        """
        self.serial.write('read_vel\n'.encode())

        while True:
            line = self.serial.readline()
            parts = line.split(' ')
            if parts[0] == 'current_vel':
                try:
                    left_side = float(parts[1])
                    right_side = float(parts[2])
                    return left_side, right_side
                except ValueError as e:
                    print(f'Failed to read current velocity:\n  `{line}`')
                    raise e
