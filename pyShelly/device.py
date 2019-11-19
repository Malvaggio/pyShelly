# -*- coding: utf-8 -*-
# pylint: disable=broad-except, bare-except

from .const import LOGGER, SHELLY_TYPES

class Device(object):
    def __init__(self, block):
        self.block = block
        self.id = block.id
        self.type = block.type
        self.ip_addr = block.ip_addr
        self.cb_updated = []
        self.is_device = True
        self.is_sensor = False
        self.sub_name = None
        self.state_values = None
        self.sensor_values = None
        self.info_values = None
        self.state = None
        self.device_type = None
        self.device_sub_type = None #Used to make sensors unique

    def type_name(self):
        """Friendly type name"""
        try:
            name = SHELLY_TYPES[self.type]['name']
        except:
            name = self.type
        if self.sub_name is not None:
            name = name + " (" + self.sub_name + ")"
        return name

    def _send_command(self, url):
        self.block.http_get(url)

    def available(self):
        return self.block.available()

    def _update(self, new_state=None, new_state_values=None, new_values=None,
                info_values=None):
        LOGGER.debug(
            "Update id:%s state:%s stateValue:%s values:%s info_values:%s",
            self.id, new_state, new_state_values, new_values, info_values)
        need_update = False
        if new_state is not None:
            if self.state != new_state:
                self.state = new_state
                need_update = True
        if new_state_values is not None:
            if self.state_values != new_state_values:
                self.state_values = new_state_values
                need_update = True
        if new_values is not None:
            self.sensor_values = new_values
            need_update = True
        if info_values is not None:
            self.info_values = info_values
            need_update = True
        if need_update:
            self._raise_updated()

    def update_status_information(self,  _status):
        """Update the status information."""
        #pass
        #self._update(info_values={}})

    def _raise_updated(self):
        for callback in self.cb_updated:
            callback(self)

    def close(self):
        self.cb_updated = []

    def _reload_block(self):
        self.block.reload = True