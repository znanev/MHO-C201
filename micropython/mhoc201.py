from micropython import const
from machine import idle
from ht16e07 import HT16E07

DIGIT_TO_SEGMENTS = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
]

TOP_SEGMENTS = {
    'hundreds': [62],
    'tens': [85, 86, 92, 87, 82, 76, 58, 60, 72, 84, 83],
    'ones': [88, 89, 91, 90, 77, 75, 70, 71, 78, 79, 80],
    'tenths': [69, 73, 74, 68, 66, 54, 50, 52, 56, 67, 64]
}

BOTTOM_SEGMENTS = {
    'tens': [41, 43, 39, 35, 31, 4, 0, 3, 37, 48, 33],
    'ones': [25, 29, 21, 17, 7, 6, 1, 2, 5, 23, 19],
}

FACE_MOUTH_BOTTOM = const(9)
FACE_MOUTH_MIDDLE = const(10)
FACE_MOUTH_TOP = const(11)

FACE_EYES_BOTTOM = const(12)
FACE_EYES_TOP = const(13)

FACE_DROPS_LEFT_2 = const(8)
FACE_DROPS_RIGHT_3 = const(14)
FACE_ANGRY_SUN = const(15)

CFE_BOTTOM = const(81)
CFE_MIDDLE = const(93)
PERCENT_FACESIDES_DEGREE_DECIMAL_CFE_TOPLEFT = const(94)
BATTERY_X = const(95)
BACKGROUND = const(96)

FACES = {
    'all': [
        FACE_MOUTH_BOTTOM,
        FACE_MOUTH_MIDDLE,
        FACE_MOUTH_TOP,
        FACE_DROPS_LEFT_2,
        FACE_DROPS_RIGHT_3,
        FACE_EYES_BOTTOM,
        FACE_EYES_TOP,
        FACE_ANGRY_SUN,
    ],
    'happy': [
        FACE_EYES_TOP,
        FACE_MOUTH_MIDDLE,
        FACE_MOUTH_BOTTOM,
    ],
    'neutral': [
        FACE_EYES_TOP,
        FACE_EYES_BOTTOM,
        FACE_MOUTH_MIDDLE,
    ],
    'sad': [
        FACE_EYES_TOP,
        FACE_EYES_BOTTOM,
        FACE_MOUTH_TOP,
    ],
    'angry': [
        FACE_EYES_BOTTOM,
        FACE_MOUTH_TOP,
        FACE_ANGRY_SUN,
    ],
}


class MHOC201Display(HT16E07):
    # LUT values based on logic analyzer captures
    # The lookup table (LUT) values control the timing and voltages for
    # refreshing the display. These values are likely specific to the
    # epaper panel used in the MHO-C201.
    # See HT16E07 datasheet for more details about the meaning of the values.

    # LUT*_FULL_CLEAR values are used turn off-on-off all the segments
    LUTV_FULL_CLEAR = [
        0x47, 0x47, 0x01,
        0x87, 0x87, 0x01,
        0x47, 0x47, 0x01,
        0x87, 0x87, 0x01,
        0x81, 0x81, 0x01,
    ]

    LUT_KK_FULL_CLEAR = [
        0x87, 0x87, 0x01,
        0x87, 0x87, 0x01,
        0x47, 0x47, 0x01,
        0x47, 0x47, 0x01,
        0x81, 0x81, 0x01,
    ]

    LUT_KW_FULL_CLEAR = [
        0x47, 0x47, 0x01,
        0x47, 0x47, 0x01,
        0x87, 0x87, 0x01,
        0x87, 0x87, 0x01,
        0x81, 0x81, 0x01,
    ]

    LUTV_UPDATE_WHITE = [
        0x47, 0x47, 0x01,
        0x4C, 0xC2, 0x01,
        0x42, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    LUT_KK_UPDATE_WHITE = [
        0x47, 0x47, 0x01,
        0x4C, 0xC2, 0x01,
        0x42, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    LUT_KW_UPDATE_WHITE = [
        0x87, 0x87, 0x01,
        0x8C, 0xC2, 0x01,
        0x82, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    # LUT*_UPDATE_BLACK are used when updating display to turn on segments
    LUTV_UPDATE_BLACK = [
        0x90, 0x90, 0x01,
        0x90, 0x90, 0x01,
        0x82, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    LUT_KK_UPDATE_BLACK = [
        0x50, 0x50, 0x01,
        0x50, 0x50, 0x01,
        0x82, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    LUT_KW_UPDATE_BLACK = [
        0x90, 0x90, 0x01,
        0x90, 0x90, 0x01,
        0x82, 0x82, 0x01,
        0x00, 0x00, 0x00,
        0x00, 0x00, 0x00,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_values = bytearray([0xff] * 13)

    def on_with_default_settings(self):
        """Turns on charge pump and sets default panel and power settings"""
        self.on()
        self.reset()
        # Panel and power settings based on logic analyzer captures
        # See HT16E07 datasheet for value descriptions
        self.send(self.PANEL_SETTING_PSR, [0x0f])
        self.send(self.POWER_SETTING_PWR, [0x0f, 0x0f])

        self.send(self.CHARGE_PUMP_ON_CPON)
        self.wait_until_not_busy()

    def off_with_default_settings(self):
        """Turns off charge pump"""
        self.wait_until_not_busy()
        # 0x03 = Segment, bg, and com voltages set to ground
        self.send(self.CHARGE_PUMP_OFF_CPOF, [0x03])
        self.off()
        self.reset()

    def wait_until_not_busy(self):
        """Waits until display is ready (until BUSY_N is high)"""
        while self.is_busy:
            idle()

    def send_luts(self, lutv, lut_kk, lut_kw):
        self.send(self.LUTV, lutv)
        self.send(self.LUT_KK, lut_kk)
        self.send(self.LUT_KW, lut_kw)

    def send_display_data(self, values):
        self.send(self.DATA_START_TRANSMISSION_DTM, values)
        self.send(self.DATA_STOP_DSP)
        self.send(self.DISPLAY_REFRESH_DRF)
        self.wait_until_not_busy()

    def full_clear(self):
        """Sends an update sequence that turns on then off all the segments.

        This should be called occasionally to remove any ghosting.
        """
        self.on_with_default_settings()

        # SF = 2Mhz, NF = 2MHz, Framerate = 20hz
        self.send(self.FRAME_RATE_CONTROL_FRC, [0x01])
        self.send_luts(self.LUTV_FULL_CLEAR,
                       self.LUT_KK_FULL_CLEAR,
                       self.LUT_KW_FULL_CLEAR)

        self.send_display_data([0xff] * 13)

        self.off_with_default_settings()

    def update_white(self, values):
        """Sets segments white/off"""
        self.on_with_default_settings()

        # SF = 2Mhz, NF = 2MHz, Framerate = 67hz
        self.send(self.FRAME_RATE_CONTROL_FRC, [0x05])
        self.send_luts(self.LUTV_UPDATE_WHITE,
                       self.LUT_KK_UPDATE_WHITE,
                       self.LUT_KW_UPDATE_WHITE)

        self.send_display_data(values)

        self.off_with_default_settings()

    def update_black(self, values):
        """Sets segments black/on"""
        self.on_with_default_settings()

        # SF = 2Mhz, NF = 2MHz, Framerate = 67hz
        self.send(self.FRAME_RATE_CONTROL_FRC, [0x05])
        self.send_luts(self.LUTV_UPDATE_BLACK,
                       self.LUT_KK_UPDATE_BLACK,
                       self.LUT_KW_UPDATE_BLACK)

        self.send_display_data(values)

        self.off_with_default_settings()

    def clear(self):
        for i, _ in enumerate(self.next_values):
            self.next_values[i] = 0xff
        self.update_white(self.next_values)

    def fill(self):
        for i, _ in enumerate(self.next_values):
            self.next_values[i] = 0x00
        self.update_black(self.next_values)

    def set_segment(self, segment_id, value):
        self.next_values[segment_id // 8] = (
            self.next_values[segment_id // 8] & ~(1 << (7 - segment_id % 8)) |
            (value << (7 - segment_id % 8))
        )

    def _set_digit(self, segments, value, zeropad):
        if value is not None:
            for i, val in enumerate(DIGIT_TO_SEGMENTS[value]):
                self.set_segment(segments[i], val)
        elif zeropad:
            # Set segments to show '0'
            for i, val in enumerate(DIGIT_TO_SEGMENTS[0]):
                self.set_segment(segments[i], val)
        else:
            # Turn off all segments
            for seg in segments:
                self.set_segment(seg, 1)

    def _set_number(self, segments, value, zeropad, flush):
        if value is None:
            for segment_ids in segments.values():
                for segment_id in segment_ids:
                    self.set_segment(segment_id, 1)
        else:
            value_str = str(round(value))

            tens_value = int(value_str[-2]) if len(value_str) > 1 else None
            self._set_digit(segments['tens'], tens_value, zeropad)

            ones_value = int(value_str[-1]) if value_str else None
            self._set_digit(segments['ones'], ones_value, zeropad)

        if flush:
            self.flush()

    def set_top_number(self, value, zeropad=False, flush=False):
        self.set_segment(TOP_SEGMENTS['hundreds'][0],
                         0 if value and value > 99 else 1)
        self._set_number(TOP_SEGMENTS, value, zeropad, flush)

    def set_bottom_number(self, value, zeropad=False, flush=False):
        self._set_number(BOTTOM_SEGMENTS, value, zeropad, flush)

    def set_face(self, face_name, flush=False):
        if face_name is not None and face_name not in FACES:
            raise ValueError('Invalid face_name: {!r}. Valid values are: {}'
                             .format(face_name, [None] + list(FACES.keys())))

        # Hide all face segments
        for seg in FACES['all']:
            self.set_segment(seg, 1)
        self.set_segment(PERCENT_FACESIDES_DEGREE_DECIMAL_CFE_TOPLEFT, 1)

        # Show segments
        if face_name is not None:
            for seg in FACES[face_name]:
                self.set_segment(seg, 0)
            # Show the side of the face.
            # This also shows percent and other segments :(
            self.set_segment(PERCENT_FACESIDES_DEGREE_DECIMAL_CFE_TOPLEFT, 0)

        if flush:
            self.flush()

    def flush(self):
        self.update_white(self.next_values)
        self.update_black(self.next_values)
