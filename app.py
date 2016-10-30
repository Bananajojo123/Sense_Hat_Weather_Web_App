from flask import Flask
from sense_hat import SenseHat
import os

sense = SenseHat()

app = Flask(__name__)


# get CPU temp
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t


# use moving average to smooth readings
def get_smooth(x):
    if not hasattr(get_smooth, "t"):
        get_smooth.t = [x, x, x]
    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x
    xs = (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3
    return xs


@app.route('/')
def index():
    t = sense.get_temperature()

    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    h = sense.get_humidity()
    p = sense.get_pressure()

    # Calculate the real temperature compesating CPU heating
    t = (t1 + t2) / 2
    t_corr = t - ((t_cpu - t) / 1.5)
    t_corr = get_smooth(t_corr)

    t = round(t, 1)
    t_corr = round(t_corr, 1)
    h = round(h, 1)
    p = round(p, 1)

    return "Temperatura: %s <br> Temperatura corregida: %s <br>Presion: %s <br>Humedad: %s" % (t, t_corr, p, h)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
