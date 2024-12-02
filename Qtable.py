
import collections
from tictactoeEnv import tictactoe
import numpy as np
GAMMA = 0.9
ALPHA = 0.2
class Agent:
    def __init__(self):
        self.env = tictactoe(True, play_mode="bot")
        self.state = self.env.reset()
        self.values = collections.defaultdict(float)
        self.mask = {"mask":np.array([1,1,1,1,1,1,1,1,1], dtype=np.int8)}
        
    def best_value_and_action(self, state):
        best_value, best_action = None, None
        for action in range(self.env.action_space.n):
            if(self.mask["mask"][action] == 0):
                    action_value = -10.0
            else:
                action_value = self.values[(state, action)]
            if best_value is None or best_value < action_value:
                best_value = action_value
                best_action = action
        # print("best values",state, best_value, best_action, self.mask)
        return best_value, best_action
    def best_value_and_action_debug(self, state):
        best_value, best_action = None, None
        for action in range(self.env.action_space.n):
            if(self.mask["mask"][action] == 0):
                action_value = -10.0
                print("bad action",action)
            else:
                action_value = self.values[(state, action)]
            if best_value is None or best_value < action_value:
                best_value = action_value
                best_action = action
            print("best", action, action_value)
        # print("best values",state, best_value, best_action, self.mask)
        return best_value, best_action
    def sample_env(self):
        # print("action sample" , self.state,self.mask["mask"])
        action = self.env.action_space.sample(np.array(self.mask["mask"], dtype=np.int8))
        old_state = self.state
        new_state, reward, is_done, _, self.mask = self.env.step(action)
        if is_done:
            self.state = self.env.reset()  
            # print("reset")
        else:
            self.state = new_state
        return old_state, action, reward, new_state
    
    def value_update(self, s, a, r, next_s):
        best_v, _ = self.best_value_and_action(next_s)
        new_v = r + GAMMA * best_v
        old_v = self.values[(s, a)]
        self.values[(s, a)] = old_v * (1-ALPHA) + new_v * ALPHA
        
    def play_episode(self, env):
        total_reward = 0.0
        state = env.reset()
        self.mask = {"mask":np.array([1,1,1,1,1,1,1,1,1], dtype=np.int8)}
        while True:
            _, action = self.best_value_and_action(state)
            # print(state, "best action", action, "value", _)
            new_state, reward, is_done, _, self.mask = env.step(action)
            total_reward += reward
            if is_done:
                self.state = self.env.reset()
                self.mask = {"mask":np.array([1,1,1,1,1,1,1,1,1], dtype=np.int8)}
                break
            state = new_state
        return total_reward
