import torch

class PGBrain:

    def __init__(self):
        self.N     = 10       # batch size
        self.D_in  = 11       # input dimension
        self.H     = 100      # hidden dimension
        self.D_out = 10       # output dimension


        # Create random Tensors to hold inputs and outputs
        # x = torch.randn(N, D_in)
        # y = torch.randn(N, D_out)

        # Use the nn package to define our model and loss function.
        self.model = torch.nn.Sequential(
            torch.nn.Linear(self.D_in, self.H),
            torch.nn.ReLU(),
            torch.nn.Linear(self.H, self.D_out),
        )

        self.loss_fn = torch.nn.MSELoss(size_average=False)


        self.learning_rate = 1e-4
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        # optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)



    