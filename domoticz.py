import base64
import urllib.request as urllib

class Domoticz:
    def __init__(self, config):
        self.config = config

    def dzRequest(self, url):
        if self.config['debug'] == True:
            print(url)

        request = urllib.Request(url)
        base64string = base64.encodestring(('%s:%s' % (self.config['dzUsername'], self.config['dzPassword'])).encode()).decode().replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib.urlopen(request)
        return response.read()

    # Sensor Type: Electric Instant+Counter
    # Set it to computed (after creating) to automatically calculate the kWh.
    def setPower(self, idx, power=0, kWh=0):
        self.dzRequest(
            "http://" + self.config['dzServer'] +
            "/json.htm?type=command&param=udevice&idx=%d" % idx +
            ("&nvalue=0&svalue=%d;%d" % (power, kWh)) +
            "&passcode=" + self.config['dzPasscode']
        )

    # Sensor Type: Any sensor that accepts a float value
    def setValue(self, idx, value):
        self.dzRequest(
            "http://" + self.config['dzServer'] +
            "/json.htm?type=command&param=udevice&idx=%d" % idx +
            ("&nvalue=0&svalue=%f" % value) +
            "&passcode=" + self.config['dzPasscode']
        )

    # Sensor Type: Switch
    def setSwitch(self, idx, state):
        switch_cmd = 'On' if state else 'Off'

        self.dzRequest(
            "http://" + self.config['dzServer'] +
            "/json.htm?type=command&param=switchlight&idx=%d" % idx +
            ("&switchcmd=%s" % switch_cmd) +
            "&passcode=" + self.config['dzPasscode']
        )
