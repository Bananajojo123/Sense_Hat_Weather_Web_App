from flask import Flask
from sense_hat import SenseHat

sense = SenseHat()

app = Flask(__name__)


@app.route('/')
def index():
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    t = round(t, 1)
    p = round(p, 1)
    h = round(h, 1)

    return "Temperatura: %s <br>Presion: %s <br>Humedad: %s" % (t, p, h)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
