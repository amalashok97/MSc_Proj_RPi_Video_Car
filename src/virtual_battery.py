#!/usr/bin/python
###
#Virtual battery class
###


import threading
import time
import os

class VirtualBattery:

	
	def __init__(self, max_capacity=100, base_step=1, discharge_interval=60):
		self.max_capacity = max_capacity
		self.base_step = base_step
		self.current_capacity = self.max_capacity
		self.discharge_interval = discharge_interval
		self.drain_timer = threading.Thread(target=self._drain)


	def _drain(self, discharge_step=None):
		if discharge_step is None:
			discharge_step = self.base_step
		while self.current_capacity >= discharge_step:
			self.current_capacity -= discharge_step
			time.sleep(self.discharge_interval)
		self.current_capacity = 0
		os.system("sudo shutdown -h now")

	
	def battery_percentage(self):
		return int(self.current_capacity/float(self.max_capacity)*100)

	def start_drain(self):
		self._stop_charge()
		self.drain_timer.start()

	def _stop_drain(self):
		if self.drain_timer.isAlive():
			self.drain_timer.join()
	
	def stop_activity(self):
		self._stop_charge()
		self._stop_drain()
