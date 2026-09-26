# HVAC Pytest Examples

This document contains executable pytest examples.

The AI should learn coding style, fixture usage, assertions and cleanup from these examples.

===========================================================
Example 1
Verify Compressor Startup
===========================================================

```python
def test_start_compressor():

    configure_controller()

    start_compressor()

    assert get_compressor_status()=="RUNNING"

    stop_compressor()

    reset_controller()
```

------------------------------------------------------------

Example 2
Verify Compressor Stop

```python
def test_stop_compressor():

    configure_controller()

    start_compressor()

    stop_compressor()

    assert get_compressor_status()=="STOPPED"

    reset_controller()
```

------------------------------------------------------------

Example 3
Verify A2L Leak Alarm

```python
def test_a2l_alarm():

    configure_controller()

    enable_a2l_detection()

    simulate_refrigerant_leak()

    assert verify_a2l_alarm()

    clear_alarm()

    reset_controller()
```

------------------------------------------------------------

Example 4
Verify Alarm Clear

```python
def test_clear_alarm():

    configure_controller()

    enable_a2l_detection()

    simulate_refrigerant_leak()

    assert verify_a2l_alarm()

    clear_alarm()

    assert read_alarm()=="NO_ALARM"

    reset_controller()
```

------------------------------------------------------------

Example 5
Verify Modbus Connection

```python
def test_modbus():

    configure_controller()

    assert connect_modbus()

    value=read_modbus_register(100)

    assert value is not None

    disconnect_modbus()

    reset_controller()
```

------------------------------------------------------------

Example 6
Verify BACnet Communication

```python
def test_bacnet():

    configure_controller()

    assert connect_bacnet()

    send_bacnet_message()

    message=receive_bacnet_message()

    assert message is not None

    disconnect_bacnet()

    reset_controller()
```

------------------------------------------------------------

Example 7
Verify Temperature Sensor

```python
def test_temperature():

    configure_controller()

    temperature=read_temperature()

    assert temperature>-50

    reset_controller()
```

------------------------------------------------------------

Example 8
Verify Defrost

```python
def test_defrost():

    configure_controller()

    start_defrost()

    assert verify_defrost_complete()

    reset_controller()
```

------------------------------------------------------------

Example 9
Verify Furnace

```python
def test_furnace():

    configure_controller()

    start_furnace()

    assert verify_heat_cycle()

    stop_furnace()

    reset_controller()
```

------------------------------------------------------------

Example 10
Verify Controller Restart

```python
def test_restart():

    configure_controller()

    restart_controller()

    assert get_compressor_status()=="STOPPED"

    reset_controller()
```