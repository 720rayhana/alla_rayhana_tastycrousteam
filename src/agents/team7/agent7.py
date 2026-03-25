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
        self.steps = 0

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
    
    def backtrack(self, obs) : 
        """
        Méthode qui renvoie le steer adapté selon la position de notre kart et les prochains noeuds derrière lui.
        Même stratégie que follow_track mais inversée.

        Args :
            obs (dict) : Dictionnaire des variables d'observation (on utilise "paths_start")

        Returns :
            steer (float) : La valeur du steer corrigée
        """
        previous_node = obs["paths_start"][0]                   # Récupération du noeud derrière nous
        steer = 0
        if abs(previous_node[0]) > 1 :                          # Si le noeud visé n'est pas sur notre trajectoire en X
            steer = previous_node[0] * 0.2                      # Le steer corrigé vise le noeud
        return steer

    def choose_action(self, obs):
        self.steps += 1
        if self.steps < 200 :                                   # Si on n'a pas dépassé les 200 steps, on avance normalement
            acceleration = 1 # Accélération constante
            steering = self.follow_track(obs)
            action = {
                "acceleration": acceleration,
                "steer": steering,
                "brake": False,
                "drift": False,
                "nitro": False,
                "rescue": False,
                "fire": False,
            }
        elif obs["distance_down_track"] < 10 :                  # Sinon, si on est devant l'arrivée de la course
            # Aucune action, on s'arrête
            action = {
                "acceleration": 0,
                "steer": 0,
                "brake": False,
                "drift": False,
                "nitro": False,
                "rescue": False,
                "fire": False,
            }
        else :                                                  # Sinon, on recule
            steering = self.backtrack(obs)
            action = {
                "acceleration": 0,
                "steer": steering,
                "brake": True, 
                "drift": False,
                "nitro": False,
                "rescue": False,
                "fire": False,
            }
        # On désactive toutes les autres actions (drift, brake...) car on ne les utilise pas
        return action
