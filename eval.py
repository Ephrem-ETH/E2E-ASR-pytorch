import argparse
import logging
import math
import os
import time

import editdistance
import Levenshtein as Lev
import kaldi_io
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
from model import Transducer, RNNModel
from DataLoader import SequentialLoader, TokenAcc, rephone

parser = argparse.ArgumentParser(description='MXNet Autograd RNN/LSTM Acoustic Model on TIMIT.')
parser.add_argument('model', help='trained model filename')
parser.add_argument('--beam', type=int, default=0, help='apply beam search, beam width')
parser.add_argument('--ctc', default=False, action='store_true', help='decode CTC acoustic model')
parser.add_argument('--bi', default=False, action='store_true', help='bidirectional LSTM')
parser.add_argument('--dataset', default='test', help='decoding data set')
parser.add_argument('--out', type=str, default='', help='decoded result output dir')
args = parser.parse_args()

logdir = args.out if args.out else os.path.dirname(args.model) + '/decode.log'
# if args.out: os.makedirs(args.out, exist_ok=True)
logging.basicConfig(format='%(asctime)s: %(message)s', datefmt="%H:%M:%S", filename=logdir, level=logging.INFO)

# Load model
Model = RNNModel if args.ctc else Transducer
model = Model(39, 30, 250, 3, bidirectional=args.bi)
model.load_state_dict(torch.load(args.model, map_location='cpu'))

use_gpu = torch.cuda.is_available()
if use_gpu:
    model.cuda()

# data set
feat = 'ark:copy-feats scp:mydata/data/{}/feats.scp ark:- | apply-cmvn --utt2spk=ark:mydata/data/{}/utt2spk scp:mydata/data/{}/cmvn.scp ark:- ark:- |\
 add-deltas --delta-order=2 ark:- ark:- | nnet-forward mydata/data/final.feature_transform ark:- ark:- |'.format(args.dataset, args.dataset, args.dataset)
with open('mydata/data/'+args.dataset+'/text', 'r') as f:
    label = {}
    for line in f:
        line = line.split()
        label[line[0]] = line[1:]

# Phone map
with open('mydata/conf/word.200000.map', 'r') as f:
    pmap = {rephone[0]: rephone[0]}
    for line in f:
        line = line.split()
        if len(line) < 3: pmap[line[0]] = rephone[0]
        else: pmap[line[0]] = line[2]
print(pmap)

def distance(y, t, blank=rephone[0]):
    def remap(y, blank):
        prev = blank
        seq = []
        for i in y:
            if i != blank and i != prev: seq.append(i)
            prev = i
        return seq
    y = remap(y, blank)
    t = remap(t, blank)
    return y, t, editdistance.eval(y, t)
# calculate sentence level character error rate(CER)
def calculate_cer(y,t):
    y = ' '.join(y)
    t = ' '.join(t)
    char_t_len = len(t)
    return char_t_len, editdistance.eval(y, t)

  

model.eval()
def decode():
    logging.info('Decoding transduction model:')
    total_word, total_char, total_cer, total_wer = 0,0,0,0
    for k, v in kaldi_io.read_mat_ark(feat):
        xs = Variable(torch.FloatTensor(v[None, ...]), volatile=True)
        if use_gpu:
            xs = xs.cuda()
        if args.beam > 0:
            y,nll = model.beam_search(xs, args.beam)
            #print("beam {}".format(y))
        else:
            y, nll = model.greedy_decode(xs)
        y = [pmap.get(i) for i in y if pmap.get(i)]
        t = [pmap.get(i) for i in label[k] if pmap.get(i)]
        y, t, wer = distance(y, t)
        total_wer += wer; total_word += len(t)
        #Compute CER
        sen_len, cer = calculate_cer(y,t)
        total_cer += cer; total_char += sen_len
        logging.info('[{}]: {}'.format(k, ' '.join(t)))
        logging.info('[{}]: {}\nlog-likelihood: {:.2f}\n'.format(k, ' '.join(y),nll))
    logging.info('{} set {} CER {:.2f}% and WER {:.2f}%\n'.format(
        args.dataset.capitalize(), 'CTC' if args.ctc else 'Transducer', 100*total_cer/total_char,100*total_wer/total_word))

decode()
