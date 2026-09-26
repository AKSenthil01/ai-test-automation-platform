# HVAC Controller API Reference

This document defines all controller APIs that AI is allowed to use while generating pytest automation scripts.

---

# API

Name:
configure_controller

Module:
Controller

Description:
Initializes the HVAC controller and loads default configuration.

Parameters:
None

Returns:
None

Usage:
configure_controller()

Example:
configure_controller()

Related APIs:
reset_controller
restart_controller

------------------------------------------------------------

# API

Name:
reset_controller

Module:
Controller

Description:
Performs a software reset of the HVAC controller.

Parameters:
None

Returns:
None

Usage:
reset_controller()

Example:
reset_controller()

Related APIs:
configure_controller
restart_controller

------------------------------------------------------------

# API

Name:
restart_controller

Module:
Controller

Description:
Restarts the controller and reloads firmware.

Parameters:
None

Returns:
None

Usage:
restart_controller()

Example:
restart_controller()

------------------------------------------------------------

# API

Name:
start_compressor

Module:
Compressor

Description:
Starts the HVAC compressor.

Parameters:
None

Returns:
None

Usage:
start_compressor()

Example:
start_compressor()

------------------------------------------------------------

# API

Name:
stop_compressor

Module:
Compressor

Description:
Stops the HVAC compressor.

Parameters:
None

Returns:
None

Usage:
stop_compressor()

Example:
stop_compressor()

------------------------------------------------------------

# API

Name:
get_compressor_status

Module:
Compressor

Description:
Returns current compressor status.

Parameters:
None

Returns:
String

Possible Values:
RUNNING
STOPPED
FAULT

Usage:
status = get_compressor_status()

Example:
assert get_compressor_status() == "RUNNING"

------------------------------------------------------------

# API

Name:
enable_a2l_detection

Module:
A2L

Description:
Enables refrigerant leak detection.

Parameters:
None

Returns:
None

Usage:
enable_a2l_detection()

Example:
enable_a2l_detection()

------------------------------------------------------------

# API

Name:
disable_a2l_detection

Module:
A2L

Description:
Disables refrigerant leak detection.

Parameters:
None

Returns:
None

Usage:
disable_a2l_detection()

Example:
disable_a2l_detection()

------------------------------------------------------------

# API

Name:
simulate_refrigerant_leak

Module:
A2L

Description:
Simulates refrigerant leakage.

Parameters:
None

Returns:
None

Usage:
simulate_refrigerant_leak()

Example:
simulate_refrigerant_leak()

------------------------------------------------------------

# API

Name:
verify_a2l_alarm

Module:
A2L

Description:
Verifies that A2L leak alarm is active.

Parameters:
None

Returns:
Boolean

Usage:
verify_a2l_alarm()

Example:
assert verify_a2l_alarm()

------------------------------------------------------------

# API

Name:
read_alarm

Module:
Alarm

Description:
Reads currently active alarm.

Parameters:
None

Returns:
String

Usage:
alarm = read_alarm()

Example:
assert read_alarm() == "A2L Leak Alarm"

------------------------------------------------------------

# API

Name:
clear_alarm

Module:
Alarm

Description:
Clears active alarm.

Parameters:
None

Returns:
None

Usage:
clear_alarm()

Example:
clear_alarm()

------------------------------------------------------------

# API

Name:
verify_alarm

Module:
Alarm

Description:
Verifies specified alarm is active.

Parameters:
alarm_name

Returns:
Boolean

Usage:
verify_alarm("A2L Leak Alarm")

Example:
assert verify_alarm("A2L Leak Alarm")

------------------------------------------------------------

# API

Name:
read_temperature

Module:
Sensor

Description:
Reads temperature sensor.

Parameters:
None

Returns:
Float

Usage:
temp = read_temperature()

Example:
assert read_temperature() > 0

------------------------------------------------------------

# API

Name:
read_pressure

Module:
Sensor

Description:
Reads pressure sensor.

Parameters:
None

Returns:
Float

Usage:
pressure = read_pressure()

Example:
assert read_pressure() > 0

------------------------------------------------------------

# API

Name:
read_sensor

Module:
Sensor

Description:
Reads all sensor values.

Parameters:
None

Returns:
Dictionary

Usage:
values = read_sensor()

Example:
assert "temperature" in read_sensor()

------------------------------------------------------------

# API

Name:
simulate_sensor_failure

Module:
Sensor

Description:
Simulates sensor failure.

Parameters:
sensor_name

Returns:
None

Usage:
simulate_sensor_failure("temperature")

Example:
simulate_sensor_failure("temperature")

------------------------------------------------------------

# API

Name:
connect_modbus

Module:
Modbus

Description:
Connects to Modbus slave.

Parameters:
None

Returns:
Boolean

Usage:
connect_modbus()

Example:
assert connect_modbus()

------------------------------------------------------------

# API

Name:
disconnect_modbus

Module:
Modbus

Description:
Disconnects Modbus.

Parameters:
None

Returns:
None

Usage:
disconnect_modbus()

Example:
disconnect_modbus()

------------------------------------------------------------

# API

Name:
read_modbus_register

Module:
Modbus

Description:
Reads Modbus register.

Parameters:
address

Returns:
Integer

Usage:
value = read_modbus_register(100)

Example:
assert read_modbus_register(100) == 25

------------------------------------------------------------

# API

Name:
write_modbus_register

Module:
Modbus

Description:
Writes Modbus register.

Parameters:
address, value

Returns:
None

Usage:
write_modbus_register(100,25)

Example:
write_modbus_register(100,25)

------------------------------------------------------------

# API

Name:
connect_bacnet

Module:
BACnet

Description:
Connects to BACnet network.

Usage:
connect_bacnet()

Example:
assert connect_bacnet()

------------------------------------------------------------

# API

Name:
disconnect_bacnet

Module:
BACnet

Description:
Disconnects BACnet network.

Usage:
disconnect_bacnet()

Example:
disconnect_bacnet()

------------------------------------------------------------

# API

Name:
send_bacnet_message

Module:
BACnet

Description:
Sends BACnet packet.

Usage:
send_bacnet_message(packet)

Example:
send_bacnet_message(packet)

------------------------------------------------------------

# API

Name:
receive_bacnet_message

Module:
BACnet

Description:
Receives BACnet packet.

Usage:
receive_bacnet_message()

Example:
packet = receive_bacnet_message()

------------------------------------------------------------

# API

Name:
start_defrost

Module:
Defrost

Description:
Starts defrost cycle.

Usage:
start_defrost()

Example:
start_defrost()

------------------------------------------------------------

# API

Name:
verify_defrost_complete

Module:
Defrost

Description:
Verifies defrost completion.

Returns:
Boolean

Usage:
verify_defrost_complete()

Example:
assert verify_defrost_complete()

------------------------------------------------------------

# API

Name:
start_furnace

Module:
Furnace

Description:
Starts furnace.

Usage:
start_furnace()

Example:
start_furnace()

------------------------------------------------------------

# API

Name:
stop_furnace

Module:
Furnace

Description:
Stops furnace.

Usage:
stop_furnace()

Example:
stop_furnace()

------------------------------------------------------------

# API

Name:
verify_heat_cycle

Module:
Furnace

Description:
Verifies heat cycle.

Returns:
Boolean

Usage:
verify_heat_cycle()

Example:
assert verify_heat_cycle()

------------------------------------------------------------

# API

Name:
capture_logs

Module:
Utilities

Description:
Captures controller logs.

Usage:
capture_logs()

------------------------------------------------------------

# API

Name:
take_snapshot

Module:
Utilities

Description:
Captures controller state snapshot.

Usage:
take_snapshot()

------------------------------------------------------------

# API

Name:
generate_report

Module:
Utilities

Description:
Generates execution report.

Usage:
generate_report()

------------------------------------------------------------

# API

Name:
log_step

Module:
Utilities

Description:
Logs current execution step.

Parameters:
message

Usage:
log_step("Starting compressor")

Example:
log_step("Starting compressor")