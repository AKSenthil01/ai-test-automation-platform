# Fixture Examples

------------------------------------------------

Requirement

Controller setup

Fixture

```python
@pytest.fixture
def controller():

    configure_controller()

    yield

    reset_controller()
```

------------------------------------------------

Requirement

Compressor running

Fixture

```python
@pytest.fixture
def compressor():

    start_compressor()

    yield

    stop_compressor()
```

------------------------------------------------

Requirement

Modbus

Fixture

```python
@pytest.fixture
def modbus():

    connect_modbus()

    yield

    disconnect_modbus()
```

------------------------------------------------

Requirement

BACnet

Fixture

```python
@pytest.fixture
def bacnet():

    connect_bacnet()

    yield

    disconnect_bacnet()
```