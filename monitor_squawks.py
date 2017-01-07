#!/usr/bin/env python3
import pyinotify
import json
import os
import time

import send_email

class MyEventHandler(pyinotify.ProcessEvent):
	def process_IN_CLOSE_WRITE(self, event):
		input_file = "/run/dump1090-mutability/aircraft.json"
		with open(input_file) as json_data:
			aircraft_data = json.load(json_data)

		interesting_squawk_codes = {"7700":"Emergency",
									"7600":"Radio Failure",
									"7500":"Hijack",
									"7777":"Military Intercept",
									}
		
		for aircraft in aircraft_data['aircraft']:
			hex_code = aircraft['hex']
			
			if "squawk" in aircraft: squawk = aircraft['squawk']
			else: squawk = None
			
			if "flight" in aircraft: flight = aircraft['flight']
			else: flight = "Unknown"
			
			if "lat" in aircraft: lat = aircraft['lat']
			else: lat = None
			
			if "lon" in aircraft: lon = aircraft['lon']
			else: lon = None
			
			if "altitude" in aircraft: altitude = aircraft['altitude']
			else: altitude = None
			
			send_alert = False
			if squawk in interesting_squawk_codes:
				print ("Emergency on aircraft: {} flight: {}".format(hex_code,flight) )
				subject = "Emergency on flight: {}".format(flight)
				body = []
				body.append("There has been an emergency on flight: {}".format(flight))
				body.append("The hex code is: {}".format(hex_code) )	
				body.append("The aircraft is squawking code: {}:{}".format(squawk,
					interesting_squawk_codes[squawk]))
				bodytext="\n".join(body)
				to = "gutbobs@gmail.com"

				# check to see if we've already sent an alert for this aircraft in the last 10 minutes
				tmp_folder = '/tmp/aircraft_alerts'
				if not os.path.exists(tmp_folder): os.makedirs(tmp_folder)
				alerts_file_name = os.path.join(tmp_folder,"alerts")

				now = time.time()

				if not os.path.exists(alerts_file_name): 
					alerts_json = {}
					with open(alerts_file_name,"w") as outfile:
						json.dump(alerts_json, outfile)
					time.sleep(1)


				with open(alerts_file_name) as aircraft_file:
					alert_data = json.load(aircraft_file)

				if hex_code not in alert_data:
					send_alert = True
					alert_data[hex_code]={squawk:[now]}
				else:
					last_alert = float(alert_data[hex_code][squawk][-1])
					# is last alert within the last hour? if so don't raise a new alert
					# if the last alert is older than 24 hours, consider it a new alert and allow one to be raised
					if last_alert > (now - 3600): 
						send_alert = False
						alert_data[hex_code][squawk].append(now)

					if last_alert < (now - 86400):
						send_alert = True
						alert_data[hex_code][squawk].append(now)




				print (alert_data)		


				with open(alerts_file_name,"w") as outfile:
					json.dump(alert_data, outfile)

				if send_alert:
					send_email.send_email(to,subject,bodytext)

				

def main():
	# watch manager
	wm = pyinotify.WatchManager()
	wm.add_watch('/run/dump1090-mutability/',pyinotify.ALL_EVENTS, rec=True)

	# event handler
	eh = MyEventHandler()

	# Notifier
	notifier = pyinotify.Notifier(wm,eh)
	notifier.loop()

if __name__ == "__main__":
	main()
