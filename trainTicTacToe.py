from Qtable import *
from tictactoeEnv import tictactoe

agent = Agent()
# writer = SummaryWriter(comment="-q-learning")
total_iter = 100000
iter_no = 0
best_reward = 0.0
while True:
    iter_no += 1
    s, a, r, next_s = agent.sample_env()
    agent.value_update(s, a, r, next_s)
    if iter_no == total_iter:
        print("finished")
        break


test_env = tictactoe(True,play_mode="human")
# print(agent.values)
# for values in agent.values.values():
#     if values != 0.0:
#         print("value: ",values)
while True:
    agent.play_episode(test_env)
# writer.close()
