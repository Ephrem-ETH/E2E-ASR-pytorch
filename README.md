# E2E ASR experiments on Librispeech 
This experiment is done on 100 hours of librispeech data for the task of E2E ASR using an intermediate character level representation and Connectionist Temporal Classifications(CTC) loss function by transforming the coorsponding transcription each utterance of both training and development set from sequence of words to sequence of characters by adding additional character(">") at the end of each word in the transcription file. We used a CTC beam search decoder to reverse back the sequence of characters to word. Statistical language model is also used for scoring the beams to improve performace of the beam search decoder.




## File description
* model.py: rnnt joint model
* model2012.py: graves2012 model
* train_rnnt.py: rnnt training script
* train_ctc.py: ctc acoustic model training script
* eval.py: rnnt & ctc decode
* DataLoader.py: kaldi feature loader





# Prepare Data
 * All the following python programs to prepare the training data are found in utils folder
### Step 1
Prepare custom lexicon file that maps word to sequence of characters
```
python word_to_characters.py --path [path-to-your-original-lexicon-file]
```
### Step 2
Transform the word transcription to sequence of charcters by adding ">" the end of each word
#### Example
 * THE SUNDAY SCHOOL  => T H E > S U N D A Y > S C H O O L >
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
excute `run.sh` to extract 13 dim mfcc feature
run `feature_transform.sh` to get 39 dim feature 

### Train CTC acoustic model
```
python train_ctc.py --lr 1e-3 --bi --dropout 0.5 --out exp/ctc_bi_lr1e-3 --schedule
```
##### Results
###### Loss curve
<img src="img/loss1.png"/>


### Decode 
```
python eval.py <path to best model> [--ctc] --bi
```


## Results
|model|beam width | CER(%)| WER(%)|
|-----|:---------:|:---:|:----|
|CTC  |1 | 30.47 |35.71|
|CTC | 3| 29.65| 34.86|
|CTC |10 | 31.05|34.66|
|CTC|15| 32.00| 34.44|


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
