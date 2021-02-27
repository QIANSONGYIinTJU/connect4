import sys
from tqdm import tqdm

from alphaconnect4.agents.neural_mcts_agent import NeuralMCTSAgent

from gameplay.game import Game

# Parallelize to generate samples in parallel
for _ in tqdm(range(500)):
    try:
        agent0 = NeuralMCTSAgent(simulation_time=3, model_path="./models/model_0.pth")
        agent1 = NeuralMCTSAgent(simulation_time=3, model_path="./models/model_1.pth",
                                 training_path="./data/training_2b.npy")

        game = Game(agent0=agent0, agent1=agent1, enable_ui=False)
        game.play()
    except Exception as exception:
        print(exception)

sys.exit()
