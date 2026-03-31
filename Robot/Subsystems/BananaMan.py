"""Class-based Banana Man audio playback helpers."""

from pathlib import Path

import pygame


class BananaMan:
	def __init__(self):
		self._mixer_ready = False
		self._banana_sound = None
		self._banana_channel = None

	def _get_banana_mp3_path(self) -> Path:
		return (Path(__file__).resolve().parents[2] / "jigboard" / "assets" / "Banana_Man.mp3")

	def _ensure_mixer(self) -> None:
		if not self._mixer_ready:
			pygame.mixer.init()
			self._mixer_ready = True

	def is_playing(self) -> bool:
		if self._banana_channel is None:
			return False
		return self._banana_channel.get_busy()

	def play(self, loop_forever: bool = True) -> None:
		"""Start playing Banana_Man.mp3.

		If it is already playing, it is stopped first and restarted.
		"""
		self._ensure_mixer()
		self.stop()

		mp3_path = self._get_banana_mp3_path()
		if not mp3_path.exists():
			raise FileNotFoundError(f"Audio file not found: {mp3_path}")

		self._banana_sound = pygame.mixer.Sound(str(mp3_path))
		loops = -1 if loop_forever else 0
		self._banana_channel = self._banana_sound.play(loops=loops)

	def stop(self) -> None:
		"""Stop Banana_Man.mp3 if it is currently playing."""
		if self._banana_channel is not None:
			self._banana_channel.stop()
			self._banana_channel = None

	def toggle(self) -> bool:
		"""Toggle playback state.

		Returns True if audio is now playing, False if it was stopped.
		"""
		if self.is_playing():
			self.stop()
			return False

		self.play(loop_forever=True)
		return True
