from dataclasses import dataclass, field


@dataclass
class RefrigerationController:
    """Small deterministic simulator for interview/demo automation."""

    refrigerant_concentration: str = "below safe limit"
    compressor_on: bool = False
    evaporator_fan_on: bool = False
    condenser_fan_on: bool = False
    alarm_active: bool = False
    safe_mode: bool = False
    alarm_mode: bool = False
    discharge_temperature: str = "within limit"
    suction_pressure: str = "within safe range"
    sensor_input_valid: bool = True
    event_log: list[str] = field(default_factory=list)

    def set_leak_condition(self):
        self.refrigerant_concentration = "above 25% of LFL"
        self.compressor_on = False
        self.evaporator_fan_on = True
        self.alarm_active = True
        self.event_log.append("refrigerant leak detected")

    def clear_leak_condition(self):
        self.refrigerant_concentration = "below safe limit"

    def manual_reset(self):
        if self.refrigerant_concentration == "below safe limit":
            self.alarm_active = False

    def set_high_discharge_temperature(self):
        self.discharge_temperature = "above limit"
        self.compressor_on = False
        self.event_log.append("high discharge temperature protection")

    def set_low_suction_pressure(self):
        self.suction_pressure = "low"
        self.compressor_on = False
        self.event_log.append("low suction pressure protection")

    def invalidate_sensor(self):
        self.sensor_input_valid = False
        self.safe_mode = True
        self.event_log.append("invalid sensor input")

    def activate_alarm_mode(self):
        self.alarm_mode = True
        self.alarm_active = True

    def modbus_registers(self):
        return {
            30001: "evaporator temperature",
            30002: "suction pressure",
            30003: "discharge temperature",
            30004: 1 if self.compressor_on else 0,
            30006: 1 if self.alarm_active else 0,
            30007: 1 if self.refrigerant_concentration == "above 25% of LFL" else 0,
            30008: 1 if self.evaporator_fan_on or self.condenser_fan_on else 0,
        }
