import sublime, sublime_plugin
import threading
import time
import datetime

class Pomodoro(threading.Thread):
	
	MAX_SECONDS = 25 * 60

	is_running = False

	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		Pomodoro.is_running = True
		start_time = datetime.datetime.now()
		d = datetime.datetime.now() - start_time
		
		while (Pomodoro.is_running and d.seconds < Pomodoro.MAX_SECONDS):
				minutes = 24 - (d.seconds / 60)
				seconds = (60 - d.seconds) % 60
				if seconds == 0:
					minutes = minutes + 1
				sublime.set_timeout(
					lambda: sublime.status_message('Pomodoro Time: [{0:02d}:{1:02d}]'.format(minutes , seconds)) , 100)
				time.sleep(1)
				d = datetime.datetime.now() - start_time
		
		if Pomodoro.is_running:
				sublime.set_timeout(
					lambda: sublime.status_message('Pomodoro finished!') , 0)
				sublime.set_timeout(
					lambda: sublime.error_message('Pomodoro finished!') , 0)


		Pomodoro.is_running = False
		

class StartPomodoroTimerCommand(sublime_plugin.ApplicationCommand):
	
	def run(self):
		thread = Pomodoro()
		thread.start()
		sublime.status_message("Pomodoro timer started!")
		
	def is_enabled(self):
		return not Pomodoro.is_running


class StopPomodoroTimerCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		sublime.status_message("Pomodoro timer stopped!")
		Pomodoro.is_running = False

				
	def is_enabled(self):
		return Pomodoro.is_running