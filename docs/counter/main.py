from dataclasses import dataclass
from multiprocessing import Process
import logging
import time
import asyncio
from typing import Any
import vlc
import sys
from RPLCD.i2c import CharLCD

from fastapi import FastAPI
from pydantic import BaseModel


def format_seconds(seconds: int) -> str:
	return time.strftime('%H:%M:%S', time.gmtime(seconds))[-5:]


@dataclass
class Context:
	logger: logging.Logger = None
	lcd: CharLCD = None
	media: Any = None
	vlc_instance: vlc.Instance = None


class Song(BaseModel):
	name: str


class BackgroundRunner:
	def __init__(self, ctx: Context):
		self.ctx = ctx
		self.step = 4

		self.name = ""
		self.length = 0
		self.is_playing = False
		self.counter = 0

	async def run_main(self):
		self.ctx.lcd.clear()
		self.ctx.lcd.write_string("Ready")

		while True:
			if not self.is_playing:
				await asyncio.sleep(1/self.step)
				continue

			self.run_display(self.counter)
			
			self.counter = self.counter + 1
			await asyncio.sleep(1/self.step)
	
	def run_display(self, counter: int) -> None:	
		lcd = self.ctx.lcd
		logger = self.ctx.logger
		
		seconds = self.counter//self.step
		ellapsed_a_second = self.counter % self.step == 0

		if ellapsed_a_second and self.length == seconds:
			lcd.clear()
			self.is_playing = False
			lcd.write_string("On hold")
			logger.info("Song has been completed")
			return

		if counter < 2:
			lcd.clear()
			lcd.write_string(self.name[:16])
			lcd.crlf()
			length = format_seconds(self.length)
			lcd.write_string(f"00:00 of {length}")

		if ellapsed_a_second:
			ellapsed = format_seconds(seconds)
			lcd.cursor_pos = (1, 0)	
			lcd.write_string(ellapsed)
	
	def change_song(self, length: int, name: str) -> None:
		self.is_playing = True
		self.name = name
		self.length = length
		self.counter = 0


app = FastAPI()
context = Context()
runner = BackgroundRunner(context)


@app.on_event("startup")
async def startup_event():
	#Creating and Configuring Logger
	Log_Format = "%(levelname)s %(asctime)s - %(message)s"

	logging.basicConfig(stream = sys.stdout,
						format = Log_Format,
						level = logging.DEBUG)

	logger = logging.getLogger()

	# Setting values of the LCD
	logger.info("Configure LCD")
	lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

	# Configure vlc
	vlc_instance = vlc.Instance()
	player = vlc_instance.media_player_new()

	context.logger = logger
	context.lcd = lcd
	context.player = player
	context.vlc_instance = vlc_instance
	asyncio.create_task(runner.run_main())


# http://127.0.0.1:8000/lcd/?message=Hello%20World!%0AFrom%20Fast%20API
@app.get("/lcd/")
def read_root(message: str = ""):
	logger = context.logger
	lcd = context.lcd

	# TODO validate input
	msg = message.replace("\n", "\n\r")
	logger.info(f"message to write {msg}")
	lcd.clear()
	lcd.write_string(msg)
	logger.info("Message written")

	return {"result": "ok", "msg": message}


# More details https://fastapi.tiangolo.com/tutorial/body/
@app.post("/play")
def play_song(song: Song):
	if not song.name:
		return { "result": "error", "msg": f"Not valid song {song.name}" }

	player = context.player

	source = f"/home/pi/workspace/data/{song.name}"
	media = context.vlc_instance.media_new(source)
	player.set_media(media)
	player.play()

	time.sleep(0.5)
	seconds = player.get_length()//1000
	runner.change_song(seconds, song.name)

	return {"result": "done", "msg": song.name}