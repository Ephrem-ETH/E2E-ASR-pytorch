# E2E ASR using An intermediate character level representations and graves 2013 experiments on Librispeech 
This experiment is done on 100 hours of librispeech data for the task of E2E ASR using an intermediate character representation and Connectionist Temporal Classifications(CTC) loss by transforming the target file of both training and development set from sequence of words to sequence of characters by adding additional character(i.e. >) at the end of each word in the transcription file. We used a CTC beam search decoder to reverse back the Sequence of characters to word. We also included a statistical language model to improve the  ctc beam search decoder.



## File description
* model.py: rnnt joint model
* model2012.py: graves2012 model
* train_rnnt.py: rnnt training script
* train_ctc.py: ctc acoustic model training script
* eval.py: rnnt & ctc decode
* DataLoader.py: kaldi feature loader



# Prepare Data
### Step 1
Prepare custom lexicon file that maps word to sequence of characters
```
python word_to_characters.py --path [path-to-your-original-lexicon-file]
```
### Step 2
Transform the word transcription to sequence of charcters by adding ">" the end of each word
```
python prepare_target.py --path [path-of-your-traget-file]
```
### Step 3
Reterive unique characters from the lexicon
```
python prepare.phone.py --path [path-to-your-original-lexicon-file]
```

## Run
* Extract feature
link kaldi librispeech example dirs (`local` `steps` `utils` )
excute `run.sh` to extract 40 dim fbank feature
run `feature_transform.sh` to get 123 dim feature as described in Graves2013

* Train CTC acoustic model
```
python train_ctc.py --lr 1e-3 --bi --dropout 0.5 --out exp/ctc_bi_lr1e-3 --schedule
```

* Train RNNT joint model
```
python train_rnnt.py --lr 4e-4 --bi --dropout 0.5 --out exp/rnnt_bi_lr4e-4 --schedule
```

* Decode 
```
python eval.py <path to best model> [--ctc] --bi
```

## Results

| Model | CER| | WER |
| --- |---| --- |
| CTC-beam 1 |29 | 35.71 |
| CTC-beam 2 | | 20.59 |

## Requirements
* Python 3.6
* PyTorch >= 0.4
* numpy 1.14
* [warp-transducer](https://github.com/HawkAaron/warp-transducer)

## Reference
* RNN Transducer (Graves 2012): [Sequence Transduction with Recurrent Neural Networks](https://arxiv.org/abs/1211.3711)
* RNNT joint (Graves 2013): [Speech Recognition with Deep Recurrent Neural Networks](https://arxiv.org/abs/1303.5778 )
* (PyTorch End-to-End Models for ASR)[https://github.com/awni/speech]
* (A Fast Sequence Transducer GPU Implementation with PyTorch Bindings)[https://github.com/HawkAaron/warp-transducer/tree/add_network_accelerate]
