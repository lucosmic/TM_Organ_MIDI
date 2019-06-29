from guizero import App,PushButton

def play():
	return 1	

def stop():
	return 1

app = App(title = "Organ")
play = PushButton(app, command = play, text = "play", align = "left", grid = [1,2])
stop = PushButton(app,command = stop, text = "stop")
app.display()
