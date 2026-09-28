from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from .....app_core import Context
from .....network.hardware import ap_commands
from ....frame_widgets.shift_wheel_slider import ShiftWheelSlider
from ...base_form import BaseForm

# (title, min, max, default, field, decimals) - field is the name the value
# is posted under (see ap_commands.SUBMARINE_SLIDER_FIELDS/HVAC_SLIDER_FIELDS).
SUBMARINE_SLIDER_DEFS = [
    ("Sensor Noise Variance", 0.0, 20, 8.3, "sensor_noise_variance", 2),
    ("Kalman Expected Sensor Variance", 0.0, 20, 8.3, "kalman_expected_sensor_variance", 2),
    ("Rudder Error Threshold", 0.0, 10, 2.75, "rudder_error_threshold", 1),
    ("Speed Error Threshold", 0.0, 10, 2.0, "speed_error_threshold", 1),
]

HVAC_SLIDER_DEFS = [
    ("Sensor Noise Variance", 0.0, 1.0, 0.1, "sensor_noise_variance", 2),
    ("Kalman Expected Sensor Variance", 0.0, 1.0, 0.1, "hvac_kalman_expected_sensor_variance", 2),
    ("State Error Threshold", 0.0, 10.0, 5.0, "hvac_state_error_threshold", 1),
]

# QSlider only steps through integers - each slider's own float min/max is
# mapped onto this many integer positions (see _to_slider_pos/_from_slider_pos).
SLIDER_RESOLUTION = 1000


class SlidersForm(BaseForm):
    '''
    Submarine and HVAC filter-tuning sliders in one form, ported from
    DefenderV0's _build_slider_block/_post_slider_settings/
    _sync_submarine_sliders/_reset_slider_defaults and HVACView's
    equivalents. Whichever group matches context.buffer.defender_status.
    submarine_mode is shown - checked every animation tick, not a static
    settings toggle. Settings go out through the shared AP poller via
    context.buffer.defender_status (see ap_commands), and the sliders sync
    back from there.
    '''

    def __init__(self, master: QWidget, context: Context):
        super().__init__(master, context, process_noun="Sliders")

        # Retitled per mode like DefenderV0/HVACView's "SUBMARINE SETTINGS"/
        # "HVAC SETTINGS" sections - see refresh.
        self.add_header("Submarine Settings")

        self._syncing = False

        body = QWidget()
        body.setLayout(QVBoxLayout())
        body.layout().setContentsMargins(0, 0, 0, 0)
        self.grid_layout.addWidget(body, self.current_row, 0, 1, 3)
        self.current_row += 1

        self.submarine_frame, self.submarine_sliders, self.submarine_labels = self._build_group(
            body, SUBMARINE_SLIDER_DEFS, self._push_submarine)
        self.hvac_frame, self.hvac_sliders, self.hvac_labels = self._build_group(
            body, HVAC_SLIDER_DEFS, self._push_hvac)

        reset_button = QPushButton("Reset Filters")
        reset_button.setFont(self.style.get_font())
        self.wire_button(reset_button, self.reset_defaults)
        body.layout().addWidget(reset_button)

        self._submarine_mode = True
        self.hvac_frame.hide()

        # Both pages push their defaults on load (DefenderV0's
        # _post_slider_settings, HVACView's _push_hvac_controls).
        self._push_submarine()
        self._push_hvac()

        self.context.animation_manager.add_callback(f"DefenderSlidersForm_{id(self)}", self.refresh)

    def _to_slider_pos(self, value: float, lo: float, hi: float) -> int:
        if hi == lo:
            return 0
        return int(round((value - lo) / (hi - lo) * SLIDER_RESOLUTION))

    def _from_slider_pos(self, pos: int, lo: float, hi: float) -> float:
        return lo + (pos / SLIDER_RESOLUTION) * (hi - lo)

    def _build_group(self, parent: QWidget, defs, push_func):
        frame = QWidget()
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(0, 0, 0, 0)
        parent.layout().addWidget(frame)
        sliders = {}
        value_labels = {}

        for title, min_val, max_val, default, field, decimals in defs:
            header = QWidget()
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(self.style.igap, 0, self.style.igap, 0)
            frame.layout().addWidget(header)

            title_label = QLabel(title)
            title_label.setFont(self.style.get_font("small"))
            header_layout.addWidget(title_label)
            header_layout.addStretch()

            value_label = QLabel(f"{default:.{decimals}f}")
            value_label.setFont(self.style.get_font("small"))
            value_label.setStyleSheet("color: gray;")
            header_layout.addWidget(value_label)

            slider = ShiftWheelSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, SLIDER_RESOLUTION)
            slider.setValue(self._to_slider_pos(default, min_val, max_val))

            def slider_callback(pos, lbl=value_label, d=decimals, lo=min_val, hi=max_val):
                lbl.setText(f"{self._from_slider_pos(pos, lo, hi):.{d}f}")
                # Only POST when the USER moved the slider.
                if not self._syncing:
                    push_func()

            slider.valueChanged.connect(slider_callback)
            frame.layout().addWidget(slider)

            sliders[field] = slider
            value_labels[field] = value_label

        return frame, sliders, value_labels

    def _values(self, defs, sliders) -> dict:
        return {field: self._from_slider_pos(sliders[field].value(), lo, hi)
                for _, lo, hi, _, field, _ in defs}

    def _push_submarine(self):
        ap_commands.push_submarine_settings(self.context.buffer, self._values(SUBMARINE_SLIDER_DEFS, self.submarine_sliders))

    def _push_hvac(self):
        ap_commands.push_hvac_settings(self.context.buffer, self._values(HVAC_SLIDER_DEFS, self.hvac_sliders))

    def _set_group(self, defs, sliders, labels, values: dict):
        '''Moves sliders to `values` ({field: value}) without posting them.'''
        self._syncing = True
        try:
            for _, lo, hi, _, field, decimals in defs:
                value = values.get(field)
                if value is None:
                    continue
                value = float(value)
                sliders[field].setValue(self._to_slider_pos(value, lo, hi))
                labels[field].setText(f"{value:.{decimals}f}")
        finally:
            self._syncing = False

    def reset_defaults(self):
        '''"Reset to Defaults" from DefenderV0/HVACView - for whichever mode's sliders are showing.'''
        if self._submarine_mode:
            defaults = {field: default for _, _, _, default, field, _ in SUBMARINE_SLIDER_DEFS}
            self._set_group(SUBMARINE_SLIDER_DEFS, self.submarine_sliders, self.submarine_labels, defaults)
            self._push_submarine()
        else:
            defaults = {field: default for _, _, _, default, field, _ in HVAC_SLIDER_DEFS}
            self._set_group(HVAC_SLIDER_DEFS, self.hvac_sliders, self.hvac_labels, defaults)
            self._push_hvac()

    def refresh(self):
        submarine_mode = ap_commands.submarine_mode(self.context.buffer)

        if submarine_mode != self._submarine_mode:
            self._submarine_mode = submarine_mode
            self.header.setText("Submarine Settings" if submarine_mode else "HVAC Settings")
            if submarine_mode:
                self.hvac_frame.hide()
                self.submarine_frame.show()
            else:
                self.submarine_frame.hide()
                self.hvac_frame.show()

        # Both groups sync every tick whichever one is showing, like the
        # original page (HVACView synced its sliders even while hidden) - so
        # the moment the AP switches modes, the newly shown group already
        # holds the AP's current values instead of whatever it last showed.
        self._sync_submarine()
        self._sync_hvac()

    def _sync_submarine(self):
        # Never yank a slider out from under the user mid-drag, and wait
        # until the client/server have picked up the last post.
        if any(slider.isSliderDown() for slider in self.submarine_sliders.values()):
            return
        if not ap_commands.submarine_settings_synced(self.context.buffer):
            return
        status = self.context.buffer.defender_status
        values = {field: status.get(field) for field in ap_commands.SUBMARINE_SLIDER_FIELDS}
        self._set_group(SUBMARINE_SLIDER_DEFS, self.submarine_sliders, self.submarine_labels, values)

    def _sync_hvac(self):
        if any(slider.isSliderDown() for slider in self.hvac_sliders.values()):
            return
        status = self.context.buffer.defender_status
        values = {field: status.expected(reported) for field, reported in ap_commands.HVAC_SLIDER_FIELDS.items()}
        self._set_group(HVAC_SLIDER_DEFS, self.hvac_sliders, self.hvac_labels, values)
