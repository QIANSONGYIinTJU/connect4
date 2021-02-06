import torch

from neural_evaluator.stub_nn import StubNet
from neural_evaluator.naive_nn import NaiveNet
from gameplay.constants import ROW_COUNT, COLUMN_COUNT


class NeuralInterface:
    def __init__(self, model_path=None):
        self.model = NaiveNet(num_rows=ROW_COUNT, num_cols=COLUMN_COUNT)
        if model_path:
            self.model.load_state_dict(torch.load(model_path))
        self.model.eval()
        self.softmax = torch.nn.Softmax(dim=0)

    def score(self, node):
        """Should include logic for who's turn it is and get based on that
        Board should be one-hot encoded / categorical
        Flip board so that agent is always with pieces #1"""
        board = node.board.copy()
        if node.turn == 1:
            # Would be better just to switch dimensions around when we will have 2 layers
            board[node.board == 1] = 2
            board[node.board == 2] = 1

        input_ = torch.from_numpy(board).unsqueeze(0).float()
        col_evaluation, score_evaluation = self.model(input_)

        score = self.softmax(score_evaluation.squeeze())[1].item()
        policy = self.softmax(col_evaluation.squeeze()).detach().cpu().numpy()
        return score, policy
