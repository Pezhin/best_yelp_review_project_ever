#!/usr/bin/python3

from datatool import YELP
from utils import preprocess_data
import torch
import torch.utils.data
import argparse
import os
import nltk

if __name__ == "__main__":
    # set hyperparameters
    parser = argparse.ArgumentParser()

    parser.add_argument('--lr', type=float, default=1e-2, help='learning rate')
    parser.add_argument('--wd', type=float, default=1e-3, help='weight decay')
    parser.add_argument('--epochs', type=int, default=50,
                        help='number of epochs for training')
    parser.add_argument('--batch_size', type=int,
                        default=128, help='the size of each batch')

    # set training parameters
    parser.add_argument('--gpu', type=bool, default=False, 
                        help='use gpu for training')
    parser.add_argument('--load', type=bool, default=False, 
                        help='load model from check point')
    parser.add_argument('--optim', type=str, default='adam', 
                        help='optimizer type, adam or rmsprop')

    # set path of data and ckp
    parser.add_argument("--preprocess", type=str, default="../data/preprocess_data",
                        help='path of preprocess data')
    parser.add_argument('--data', type=str, default="../data",
                        help='path of data')
    parser.add_argument('--ckp', type=str, default="../check_point",
                        help='path of check point')

    args = parser.parse_args()
    
    # Install the punkt package
    if not os.path.exists("../nltk_data"):
        os.mkdir("../nltk_data")
        nltk.download('punkt', download_dir="../nltk_data")
    nltk.data.path.append("../nltk_data")

    # Load dataset with proprocessing, download if empt. Preprocess will only do once.
    train_set = YELP(root=args.data, preprocess_path=args.preprocess, train=True, download=True)
    test_set = YELP(root=args.data, preprocess_path=args.preprocess, train=False, download=False)

    # Load batch data automatically
    train_loader = torch.utils.data.DataLoader(
        train_set, batch_size=args.batch_size, shuffle=True, num_workers=2
    )
    test_loader = torch.utils.data.DataLoader(
        test_set, batch_size=args.batch_size, shuffle=False, num_workers=2
    )