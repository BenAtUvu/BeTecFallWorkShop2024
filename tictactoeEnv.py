from enum import Enum
import numpy as np
import gymnasium as gym
from gymnasium import spaces

class tictactoe():
    def __init__(self, stableAPI,render_mode=None, play_mode="human", firstMove = True):
        


        
        self.play_mode = play_mode
        self.stableAPI = stableAPI
        self.firstMove = firstMove
        self.moveNumber = 0
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.mask = [1,1,1,1,1,1,1,1,1]
        if(self.firstMove == False):
            if(play_mode == "human"):
                self.otherPlayerTurn()
        

        # We have 9 actions
        self.action_space = spaces.Discrete(9)
        self.render_mode = render_mode

        if(play_mode == "human"):
            print("pick action 0-8")
            hr = "----------------"
            iter = 0
            for row in self.board:
                print(hr)
                line = ""
                
                for x in list(row):
                    line += f"  {iter}  |"
                    iter+=1
                print(line[:-1])
            print(hr)
    def win_check(self,board):
        #row
        for i in range(3):
            if board[i][0] and board[i][0:3] == [board[i][0], board[i][0], board[i][0]]:
                return board[i][0]
        #column
        for i in range(3):
            col = [board[0][i], board[1][i], board[2][i]]
            if board[0][i] and col == [board[0][i], board[0][i], board[0][i]]:
                return board[0][i]
        #diagnals
        if board[0][0] and [board[0][0], board[1][1], board[2][2]] == [board[0][0], board[0][0], board[0][0]]:
            return board[0][0]
        if board[0][2] and [board[0][2], board[1][1], board[2][0]] == [board[0][2], board[0][2], board[0][2]]:
            return board[0][2]
        return 0
    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}
    def _get_info(self):
        mask = self.flattenBoard()
        it = 0
        for val in self.flattenBoard():
            mask[it] = 0 if val else 1
            it +=1
        # print("mask:", mask)
        return {
            'mask': mask
        }
    def flattenBoard(self):
        flatboard = np.array([self.board])
        # print("flat",flatboard.ravel().tolist())
        return flatboard.ravel().tolist()
    def reset(self, seed=None, options=None):
        self.moveNumber = 0
        # print("reset")
        self.board = [[0,0,0],
                      [0,0,0], 
                      [0,0,0]]
        
        info = self._get_info()
        self.mask = [1,1,1,1,1,1,1,1,1]
        observation = []
        if self.render_mode == "human":
            self._render_frame()

        if self.stableAPI == True:
            return str(self.board)
        else:
            return observation, info
    def step(self, action, q_table = None):
        reward = 0
        #play with 1s goes first
        # if action == 4:
        #     reward += 1
        terminated = False
        # print("mask: ",self._get_info()["mask"], "action:",action)
        # print("win check:",self.win_check(self.board))
        if(self._get_info()["mask"][action] == 0):
            print("invalid move "+str(self.board)+" action ", action)
            quit()
        if self.firstMove == True:
            row = action // 3
            col = action % 3
            self.board[row][col] = 1
            if self.win_check(self.board) == 1:
                reward += 2
                if self.play_mode == "human":
                    print("Computer Won")
                    self.render()
                terminated = True
            elif self.win_check(self.board) == 2:
                if self.play_mode == "human":
                    print("Human Won")
                    self.render()
                reward = -1
                terminated = True
            else:
                reward += 0
                if(self.moveNumber != 4):
                    # print("move number", self.moveNumber)
                    self.otherPlayerTurn(q_table)
        else:
            row = action // 3
            col = action % 3
            self.board[row][col] = 2
            if self.win_check(self.board) == 1:
                reward = -1
                terminated = True
            elif self.win_check(self.board) == 2:
                reward += 2
                terminated = True
            else:
                reward += 0
                if(self.play_mode == "human"):
                    self.otherPlayerTurn(q_table)
        
        self.moveNumber += 1
        if self.firstMove == True:
            if(self.moveNumber == 5):
                terminated = True
                reward = 0
        else:
            if(self.moveNumber == 4):
                terminated = True
                reward = 0
                
        observation = self.board
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        if(terminated == 1):
            # print(observation)
            self.reset()
        # if(terminated):
        #     self.reset()
        
        return str(observation), reward, terminated, False, info
    def otherPlayerTurn(self,q_table):
        #negative one corresponds to human player
        if(self.play_mode == "human"):
            self.render()
            info = self._get_info()
            while True:
                otherAction = int(input("Your move: "))
                if otherAction > len(info["mask"]) or info["mask"][otherAction] == 0:
                    print("incorrect move")
                else:
                    break
        else:
            if(self.firstMove == True):
                otherAction = self.action_space.sample(np.array(self.mask,dtype = np.int8))
                #CHECK IS WE CAN WIN
                if(self.moveNumber >= 2):
                    #row
                    for i in range(3):
                        # if the sum is 4 and there is a zero
                        if sum(self.board[i][0:3]) == 4:
                            if 0 in self.board[i][0:3]:
                                otherAction = i * 3
                                otherAction += self.board[i][0:3].index(0)
                                
                    #column
                    for i in range(3):
                        col = [self.board[0][i], self.board[1][i], self.board[2][i]]
                        if sum(col) == 4:
                            if 0 in col:
                                otherAction = col.index(0) * 3
                                otherAction += i
                    #diagnals
                    dag = [self.board[0][0], self.board[1][1], self.board[2][2]]
                    if sum(dag) == 4:
                        if 0 in dag:
                            otherAction = dag.index(0)*3 + dag.index(0)
                            
                    dag = [self.board[0][2], self.board[1][1], self.board[2][0]]
                    if sum(dag) == 4:
                        if 0 in dag:
                            otherAction = dag.index(0)*3 + (2 - dag.index(0))
            else:
                print("sorry only only the bot can go first")
                quit()
                
                
        if self.firstMove == False:
            row = otherAction // 3
            col = otherAction % 3
            self.self.board[row][col] = 1
        else:
            row = otherAction // 3
            col = otherAction % 3
            self.board[row][col] = 2
        # print("board:",self.board)
        self.mask = self._get_info()["mask"]
    def render(self):
        hr = "----------------"
        for row in self.board:
            print(hr)
            line = ""
            for x in list(row):
                if x == 0:
                    draw = " "
                elif x == 1:
                    draw = "X"
                else: 
                    draw = "O"
                line += f"  {draw}  |"
            print(line[:-1])

        print(hr)

    def _render_frame(self):
        if self.render_mode == "human":
            print(self.board)
