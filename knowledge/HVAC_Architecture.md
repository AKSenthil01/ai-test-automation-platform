# HVAC System

Subsystems

- Controller
- BACnet
- Modbus
- Sensor
- Compressor
- Defrost
- Heat Furnace
- A2L Leak Detection
- Alarm Manager

Relationships

BACnet controls Controller communication.

Sensor values affect Defrost.

Controller controls Compressor.

A2L Leak Detection can stop Compressor.

Alarm Manager records all critical faults.