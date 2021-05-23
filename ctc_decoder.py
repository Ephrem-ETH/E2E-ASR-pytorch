"""
Author: Awni Hannun

This is an example CTC decoder written in Python. The code is
intended to be a simple example and is not designed to be
especially efficient.

The algorithm is a prefix beam search for a model trained
with the CTC loss function.

For more details checkout either of these references:
  https://distill.pub/2017/ctc/#inference
  https://arxiv.org/abs/1408.2873

"""

import numpy as np
import math
import collections
from word_to_characters import lexicon_dic
import arpa

with open('mydata/data/local/lm/phones.txt','r') as f:
    alphabet = []
    for char in f:
        alphabet.append(char[0])
      
NEG_INF = -float("inf")
lexicon_dict = lexicon_dic() 
print("dict length : {}".format(len(lexicon_dict)))
#load the language models
lm_models = arpa.loadf("/home/emekonnen/mydata/E2E-ASR/mydata/data/local/lm/3-gram.pruned.3e-7.arpa")
lm = lm_models[0]


def make_new_beam():
    fn = lambda : (NEG_INF, NEG_INF)
    return collections.defaultdict(fn)

def logsumexp(*args):
    """
    Stable log sum exp.
    """
    if all(a == NEG_INF for a in args):
        return NEG_INF
    a_max = max(args)
    lsp = math.log(sum(math.exp(a - a_max)
                       for a in args))
    return a_max + lsp

def decode(probs, beam_size=10, blank=0, alpha=0.3):
    """
    Performs inference for the given output probabilities.

    Arguments:
      probs: The output probabilities (e.g. log post-softmax) for each
        time step. Should be an array of shape (time x output dim).
      beam_size (int): Size of the beam to use during inference.
      blank (int): Index of the CTC blank label.

    Returns the output label sequence and the corresponding negative
    log-likelihood estimated by the decoder.
    """
    T, S = probs.shape
    W = lambda l: re.findall(r'\w+[\s|>]', l)
    #print("len {0},{1}".format(len(alphabet),S))
    # Elements in the beam are (prefix, (p_blank, p_no_blank))
    # Initialize the beam with the empty sequence, a probability of
    # 1 for ending in blank and zero for ending in non-blank
    # (in log space).
    beam = [(tuple(), (0.0, NEG_INF))]

    for t in range(T): # Loop over time

        # A default dictionary to store the next step candidates.
        next_beam = make_new_beam()
        #pruned_alphabet = [alphabet[i] for i in np.where(probs[t] > -55.00 )[0]]
        for s in range(S-1): # Loop over vocab
        #for c in pruned_alphabet:
            #s = alphabet.index(c)
            p = probs[t, s]

            # The variables p_b and p_nb are respectively the
            # probabilities for the prefix given that it ends in a
            # blank and does not end in a blank at this time step.
            for prefix, (p_b, p_nb) in beam: # Loop over beam

                # If we propose a blank the prefix doesn't change.
                # Only the probability of ending in blank gets updated.
                if s == blank:
                  n_p_b, n_p_nb = next_beam[prefix]
                  n_p_b = logsumexp(n_p_b, p_b + p, p_nb + p)
                  next_beam[prefix] = (n_p_b, n_p_nb)
                  continue

                # Extend the prefix by the new character s and add it to
                # the beam. Only the probability of not ending in blank
                # gets updated.
                end_t = prefix[-1] if prefix else None
                n_prefix = prefix + (alphabet[s],)
                n_p_b, n_p_nb = next_beam[n_prefix]
                if alphabet[s] != end_t:
                  n_p_nb = logsumexp(n_p_nb, p_b + p, p_nb + p)
                                    
                    #sample code to score the prefix by LM 
                     
                else:
                  # We don't include the previous probability of not ending
                  # in blank (p_nb) if s is repeated at the end. The CTC
                  # algorithm merges characters not separated by a blank.
                  n_p_nb = logsumexp(n_p_nb, p_b + p)

                # *NB* this would be a good place to include an LM score.
                # if alphabet[s]=='>':
                #     last_word = "".join(n_prefix).split(">")[-2]
                #     #print(last_word)
                #     if last_word in list(lexicon_dict.keys()):
                #       words = " ".join("".join(n_prefix).split(">")).strip()
                #       print(words)
                #       n_p_nb = logsumexp(lm.log_p(words),n_p_nb) 
                #       print(n_p_nb)
                if len(n_prefix) > 1 and alphabet[s] == '>':
                      last_word = "".join(n_prefix).split(">")[-2]   
                                
                      #print(last_word)
                      if len(last_word) > 0  and last_word  in list(lexicon_dict.keys()):
                        words = ("".join(n_prefix).replace(">"," ")).strip()
                        #print(n_prefix)
                        #print(words)
                        lm_prob = lm.log_p(words)* alpha
                        #print(lm_prob)
                        n_p_nb = logsumexp(n_p_nb,lm_prob , p_nb + p, p_b + p) 
                        #n_p_nb = logsumexp(n_p_nb, p_nb + p, p_b + p) 
                        #print(n_p_nb)
                next_beam[n_prefix] = (n_p_b, n_p_nb)
                #print("n_p_b {0}, n_p_nb {1}".format(n_p_b,n_p_nb))

                # If s is repeated at the end we also update the unchanged
                # prefix. This is the merging case.
                if alphabet[s] == end_t:
                  n_p_b, n_p_nb = next_beam[prefix]
                  n_p_nb = logsumexp(n_p_nb, p_nb + p)
                  next_beam[prefix] = (n_p_b, n_p_nb)

        # Sort and trim the beam before moving on to the
        # next time-step.
        beam = sorted(next_beam.items(),
                key=lambda x : logsumexp(*x[1]),
                reverse=True)
        beam = beam[:beam_size]

    best = beam[0]
    best_beam = "".join(best[0]).split(">")
    print(best_beam)
    return tuple(best_beam[:-1]), -logsumexp(*best[1])
