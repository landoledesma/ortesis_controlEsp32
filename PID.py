
class PID():

    def __init__(self, kp, ki, kd, _type='PID'):
        self._type  = _type 
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.last_error = 0
        self.prev_int = 0


    def update(self, error, dt, _type):
        if _type == 'P':
            self.output = self.proportional(error)
        elif _type == 'PD':
            self.output = self.proportional(error) + self.derivative(error, dt)
        elif _type == 'PI':
            self.output = self.proportional(error) + self.integral(error, dt)
        elif _type == 'PID':    
            self.output = self.proportional(error) + self.integral(error, dt) + self.derivative(error, dt)  
        else:
             return print("INVALID TYPE OF CONTROL")

        self.last_error = error
        return self.output


    def proportional(self, error):
        return self.kp*error 


    def integral(self, error, dt):
        return self.ki * (self.prev_int + ((error + self.last_error)/2 * dt))


    def derivative(self, error, dt):
        return self.kd * ((error - self.last_error)/dt)

    