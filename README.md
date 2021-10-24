# Japanese Phoneme Balance Sentence Extractor
If you input texts of Aozora Bunko into this extractor, phoneme balance sentences will be extracted. This extractor counts the two-phoneme and three-phoneme chains contained in the texts and outputs a few sentences that cover the types of phoneme chains.

## Supported platforms
- Linux

## Dependencies
- Python 3
- [jumanpp](https://github.com/ku-nlp/jumanpp)
- [pyopenjtalk](https://github.com/r9y9/pyopenjtalk)

## Download Data
Please download text files from [Aozora Bunko](https://www.aozora.gr.jp/).

## Run
To run this extractor, please store the downloaded texts in "aosora" directory.

```
cd /path/to/phoneme-balance-sentence-extractor/
mkdir aosora
mkdir aosora_utf8
```

When you run the script, balance sentences will be output to "extracted_sentences.txt".

```
sh aosora_analysis.sh
```
