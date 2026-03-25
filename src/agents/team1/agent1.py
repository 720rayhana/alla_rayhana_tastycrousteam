import numpy as np
import random

from agents.kart_agent import KartAgent
# Suppression des modules non utilisés

class Agent1(KartAgent):
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
        next_node = obs["paths_end"][self.path_lookahead - 2]   # Récupération du prochain noeud à viser
        steer = 0
        if abs(next_node[0]) > 1 :                              # Si le noeud visé n'est pas sur notre trajectoire en X
            steer = next_node[0] * 0.2                          # Le steer corrigé vise le noeud
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

        # Première étape du demi tour
        if self.steps < 27 :
            action = {
            "acceleration": 0,
            "steer": 1,
            "brake": True, 
            "drift": False,
            "nitro": False,
            "rescue": False,
            "fire": False,
            }

        # Deuxième étape du demi tour
        elif self.steps < 50 :
            steering = self.backtrack(obs)
            action = {
            "acceleration": 0.5,
            "steer": steering,
            "brake": False, 
            "drift": False,
            "nitro": False,
            "rescue": False,
            "fire": False,
            }

        # Si on est devant l'arrivée de la course, après un grand nombre de steps
        elif (obs["distance_down_track"] < 10) and self.steps > 300 :
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

        # Sinon, on suit la piste en marche arrière
        else : 
            steering = self.follow_track(obs)
            action = {
                "acceleration": 0,
                "steer": steering,
                "brake": True, 
                "drift": False,
                "nitro": False,
                "rescue": False,
                "fire": False,
            }
        return action
