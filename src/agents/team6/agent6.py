import numpy as np
import random

from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent


class Agent6(KartAgent):
    def __init__(self, env, path_lookahead=3):
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.name = "Alla-Rayhana"  # Remplacement par (nom-prénom)

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def endOfTrack(self):
        return self.isEnd

    def choose_action(self, obs):
        acceleration = 1    # accélération constante
        steering = -1        # ou -1 si on veut qu'il tourne à gauche
        # On ne traite pas le cas où l'agent se cogne à un obstacle en tournant sur lui-même et se retrouve bloqué
        action = {
            "acceleration": acceleration,
            "steer": steering,
            "brake": False, 
            "drift": False,
            "nitro": False,
            "rescue": False,
            "fire": False,
        }
        # On désactive toutes les autres actions (drift, brake...) car on ne les utilise pas
        return action
