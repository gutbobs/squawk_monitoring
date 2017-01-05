# squawk_monitoring
A Raspberry Pi and a TV tuner as an SDR can be combined to monitor ADS-B signals from aircraft (as per here: http://www.instructables.com/id/Cheap-easy-Orange-Pi-SDR-for-Flightradar24-Feed/) this code in this repo will allow the Pi to alert you when ever an aircraft 'squawks' an emergency code

No additional python modules are required as everything you need is already available, however my own home network does have an SMTP server already configured, hence the basic config in the send_email module

