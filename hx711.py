from utime import sleep_us, time
from machine import Pin
from micropython import const

class HX711Exception(Exception):
    pass

class InvalidMode(HX711Exception):
    pass

class DeviceIsNotReady(HX711Exception):
    pass

class HX711:
    """
    Micropython driver for Avia Semiconductor's HX711
    24-Bit Analog-to-Digital Converter.
    """

    CHANNEL_A_128 = const(1)
    CHANNEL_A_64 = const(3)
    CHANNEL_B_32 = const(2)

    DATA_BITS = const(24)
    MAX_VALUE = const(0x7fffff)
    MIN_VALUE = const(0x800000)
    READY_TIMEOUT_SEC = const(5)
    SLEEP_DELAY_USEC = const(80)

    def __init__(self, d_out: int, pd_sck: int, channel: int = CHANNEL_A_128):
        # Initialize pins
        self.d_out_pin = Pin(d_out, Pin.IN)
        self.pd_sck_pin = Pin(pd_sck, Pin.OUT, value=0)
        self.channel = channel
        self.offset = 0
        self.scale = 1

    def __repr__(self):
        return f"HX711 on channel {self.channel}, gain={self.channel[1]}"

    def _convert_from_twos_complement(self, value: int) -> int:
        """
        Converts a given integer from two's complement format.
        """
        if value & (1 << (self.DATA_BITS - 1)):
            value -= 1 << self.DATA_BITS
        return value

    def _set_channel(self):
        """
        Set the input channel and gain selection.
        """
        for _ in range(self._channel):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

    def _wait(self):
        """
        Wait until the HX711 is ready or raise an exception.
        """
        t0 = time()
        while not self.is_ready():
            if time() - t0 > self.READY_TIMEOUT_SEC:
                raise DeviceIsNotReady()

    @property
    def channel(self) -> tuple:
        """
        Get the current input channel as a tuple (Channel, Gain).
        """
        if self._channel == self.CHANNEL_A_128:
            return 'A', 128
        if self._channel == self.CHANNEL_A_64:
            return 'A', 64
        if self._channel == self.CHANNEL_B_32:
            return 'B', 32

    @channel.setter
    def channel(self, value):
        """
        Set the input channel and gain.
        """
        if value not in (self.CHANNEL_A_128, self.CHANNEL_A_64, self.CHANNEL_B_32):
            raise InvalidMode('Gain must be one of CHANNEL_A_128, CHANNEL_A_64, CHANNEL_B_32')
        self._channel = value

        if not self.is_ready():
            self._wait()

        for _ in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)

        self._set_channel()

    def is_ready(self) -> bool:
        """
        Check if HX711 is ready to read data.
        """
        return self.d_out_pin.value() == 0

    def power_off(self):
        """
        Put the HX711 into power-down mode.
        """
        self.pd_sck_pin.value(0)
        self.pd_sck_pin.value(1)
        sleep_us(self.SLEEP_DELAY_USEC)

    def power_on(self):
        """
        Reset and wake up the HX711.
        """
        self.pd_sck_pin.value(0)
        self.channel = self._channel

    def read(self, raw=False) -> int:
        """
        Read the current value from the HX711.
        """
        if not self.is_ready():
            self._wait()

        raw_data = 0
        for _ in range(self.DATA_BITS):
            self.pd_sck_pin.value(1)
            self.pd_sck_pin.value(0)
            raw_data = (raw_data << 1) | self.d_out_pin.value()
        self._set_channel()

        if raw:
            return raw_data
        else:
            return self._convert_from_twos_complement(raw_data)

    def tare(self, times=10):
        """
        Tare the scale by setting the offset to the current reading.
        """
        self.offset = sum(self.read() for _ in range(times)) / times

    def set_scale(self, scale: float):
        """
        Set the calibration scale factor.
        """
        self.scale = scale

    def get_units(self, times=10) -> float:
        """
        Get the weight in user-defined units (grams, kilograms, etc.).
        """
        value = sum(self.read() for _ in range(times)) / times
        return (value - self.offset) / self.scale