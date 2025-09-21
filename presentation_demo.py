#!/usr/bin/env python3
"""
PR Review Agent - Live Presentation Demo Script
A conversational, dialogue-driven demonstration
"""
import time
import sys
import requests
import json
from datetime import datetime

class PresentationDemo:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.presenter_name = "Demo Presenter"
        
    def speak(self, text, pause=2