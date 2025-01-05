import unittest
import pygame
from unittest.mock import patch, Mock
from ..main import main

class TestAudioDeviceUnavailable(unittest.TestCase):
    @patch("pygame.mixer.init")
    @patch("pygame.mixer.Sound")
    @patch("pygame.event.get")
    def test_audio_device_unavailable(self, mock_event_get, mock_sound, mock_mixer_init):
        # Simulate audio initialization failure
        mock_mixer_init.side_effect = Exception("No such audio device")
        
        # Mock the event queue to include a QUIT event to close the game
        mock_event_get.side_effect = [
            [pygame.event.Event(pygame.QUIT)]  # Simulate a QUIT event
        ]
        
        with patch("builtins.print") as mock_print:
            # Run the main function (it will exit after the simulated QUIT event)
            main()
            
            # Check that the audio error was logged
            mock_print.assert_any_call("Error loading sound: No such audio device")