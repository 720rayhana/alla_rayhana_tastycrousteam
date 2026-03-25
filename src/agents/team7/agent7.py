import numpy as np
import random

from utils.track_utils import compute_curvature, compute_slope
from agents.kart_agent import KartAgent

class Agent7(KartAgent):
    def __init__(self, env, path_lookahead=3):
        super().__init__(env)
        self.path_lookahead = path_lookahead
        self.agent_positions = []
        self.obs = None
        self.isEnd = False
        self.name = "Alla-Rayhana" # Changement du nom

    def reset(self):
        self.obs, _ = self.env.reset()
        self.agent_positions = []

    def endOfTrack(self):
        return self.isEnd

    def follow_track(self, obs) : 
        """
        Méthode qui renvoie le steer adapté selon la position de notre kart et les prochains noeuds devant lui.

        Args :
            obs (dict) : Dictionnaire des variables d'observation (on utilise "paths_end")

        Returns :
            steer (float) : La valeur du steer corrigée
        """
        next_node = obs["paths_end"][self.path_lookahead - 1]   # Récupération du prochain noeud à viser
        steer = 0
        if abs(next_node[0]) > 2 :                              # Si le noeud visé n'est pas sur notre trajectoire en X
            steer = next_node[0]                                # Le steer corrigé vise le noeud
        return steer

    def choose_action(self, obs):
        acceleration = 1 # Accélération constante
        steering = self.follow_track(obs)
        action = {
            "acceleration": acceleration,
            "steer": steering,
            "brake": False, # bool(random.getrandbits(1)),
            "drift": False,
            "nitro": False,
            "rescue": False,
            "fire": False,
        }
        # On désactive toutes les autres actions (drift, brake...) car on ne les utilise pas
        return action
