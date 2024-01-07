import pytest

from smartswitch import *



# A fixture that adds the switch to the test group
@pytest.fixture(scope="function")
def switch_on_group(switch, group):
    # Remove device from the group if it was there already
    resp = group.remove_device(switch)
    print(resp)

    # Create a brand new group
    resp = group.add_device(switch)
    print(resp)
    assert resp['status'] == 'ok'

    yield switch

    # Cleanup group membership
    resp = group.remove_device(switch)
    print(resp)
    assert resp['status'] == 'ok'


# Test 1:
# - Create a test group (if not yet created)
# - Add endpoint to the group (if not yet created)
# - Send On/Off/Toggle (and later LevelCtrl) commands to the group
# - Verify the device handles these commands


def test_on_off(group, switch_on_group):
    group.switch('ON')
    switch_on_group.wait_device_state_change('ON')
    switch_on_group.wait_zigbee_state_change()  # Ignore the state change generated by z2m, wait for the one generated by the device
    assert switch_on_group.wait_zigbee_state_change() == 'ON'

    group.switch('OFF')
    switch_on_group.wait_device_state_change('OFF')
    switch_on_group.wait_zigbee_state_change()  # Ignore the state change generated by z2m, wait for the one generated by the device
    assert switch_on_group.wait_zigbee_state_change() == 'OFF'


def test_toggle(group, switch_on_group):
    group.switch('OFF')
    switch_on_group.wait_device_state_change('OFF')
    switch_on_group.wait_zigbee_state_change()  # Ignore the state change generated by z2m, wait for the one generated by the device
    assert switch_on_group.wait_zigbee_state_change() == 'OFF'

    group.switch('TOGGLE')
    switch_on_group.wait_device_state_change('ON')
    switch_on_group.wait_zigbee_state_change()  # Ignore the state change generated by z2m, wait for the one generated by the device
    assert switch_on_group.wait_zigbee_state_change() == 'ON'

    group.switch('TOGGLE')
    switch_on_group.wait_device_state_change('OFF')
    switch_on_group.wait_zigbee_state_change()  # Ignore the state change generated by z2m, wait for the one generated by the device
    assert switch_on_group.wait_zigbee_state_change() == 'OFF'
