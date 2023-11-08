# Trust-nlp
## Prompt text files
To run the model with specific prompts, you should save the prompt in a text file. The file name should start with `prompt_{}.txt` where the specific name of the prompt be added in place of the brackets. (e.g. `prompt_BASE.txt`)

## Run API Call
These arguments are the default settings which executes GPT3.5 API model. You can simply run `python main.py` to get the same result.
```python
python main.py --work='api' \
               --model='gpt3' \
               --data-path='./data/pubmed_sample150.csv' \
               --settings='./settings.json' \
               --prompt='BASE' \
               --output-path='./results/' \
               --checkpoint=None
```
A checkpoint pickle file is created in `./results/ckpt/` folder per instance. If the API stops running for any reason you can rerun the model from when it stopped by setting the checkpoint argument to the saved pickle file. (e.g. `--checkpoint='./results/ckpt/gpt3_result_part.pkl`)

To use **ChatGPT** model, arguements can be modified as the following:

```python
python main.py --model='chatgpt'
```

## Run Statistics Test
To run the statistics test, your dataset should include integer label values from the second column. 

Below is the sample code to run statistics from `final_result.csv` and save the statistics text file into `./results/stats/` folder.
```python
python main.py --work='quant' \
               --data-path="./results/final_result.csv" \
               --output-path="./results/stats/"
```