import torch
import torch.nn as nn
import math

class InputEmbeddings(nn.Module):

    def __init__(self,d_model:int,vocab_size:int):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)

    def forward(self,x):
        return self.embedding(x) * math.sqrt(self.d_model)

class PositionalEncoding(nn.Module):

    def __init__(self,d_model:int, seq_len:int, dropout: float) -> None:
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)

        # create a matrix of shape (seq_len, d_model)
        pe = torch.zeros(seq_len,d_model)

        #create a vector of shape (seq_length, 1)
        position = torch.arange(0,seq_len,dtype=torch.float).unsqueeze(1) #numerator
        div_term = torch.exp(torch.arange(0,d_model,2).float() * (-math.log(1000.0)/d_model)) #denominator but calculated in log space

        #apply the sin to even positions/cos to odd positions
        pe[:,0::2] = torch.sin(position * div_term)
        pe[:,1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0) #(1,Seq_len,d_model) - we do this to handle batches of sentences

        self.register_buffer('pe',pe) #this is to save the tensor in the file
    
    def forward(self,x):
        # we need to add the positional vector to every word in the sentence
        x = x + (self.pe[:,:x.shape[1],:]).requires_grad_(False) #false because this tensor is fixed and is not learned
        return self.dropout(x)
    
class LayerNormalization(nn.Module):

    def __init__(self, eps:float = 10**-6) -> None: #we add epsilon to avoid dividing by zero - and to make sure we don't get super big or small numbers in denominator
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones(1)) #nn.parameter makes the parameter learnable #multiplied
        self.bias = nn.Parameter(torch.zeros(1)) #added

    def forward(self,x):
        mean = x.mean(dim = -1, keepdim=True)