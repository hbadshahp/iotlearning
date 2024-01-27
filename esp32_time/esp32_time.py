import ntptime
ntptime.settime() # this queris the time from an NTP server
# time.localtime()
UTC_OFFSET = 5.5*60*60
actual_time = time.localtime(time.time() + int(UTC_OFFSET))
actual_time