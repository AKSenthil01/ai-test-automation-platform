# Assertions

Requirement

Verify compressor startup

Assertion

assert get_compressor_status()=="RUNNING"

------------------------------------------------

Requirement

Verify compressor stop

Assertion

assert get_compressor_status()=="STOPPED"

------------------------------------------------

Requirement

Verify A2L alarm

Assertion

assert verify_a2l_alarm()

------------------------------------------------

Requirement

Verify alarm cleared

Assertion

assert read_alarm()=="NO_ALARM"

------------------------------------------------

Requirement

Verify Modbus connection

Assertion

assert connect_modbus()

------------------------------------------------

Requirement

Verify BACnet communication

Assertion

assert connect_bacnet()

------------------------------------------------

Requirement

Verify temperature sensor

Assertion

assert read_temperature()>-50

------------------------------------------------

Requirement

Verify defrost

Assertion

assert verify_defrost_complete()

------------------------------------------------

Requirement

Verify furnace

Assertion

assert verify_heat_cycle()