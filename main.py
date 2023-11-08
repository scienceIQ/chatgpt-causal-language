import argparse
import os
from itertools import combinations

from utils.api_call import OpenAIAPI
from utils.data import *
from utils.stats import *

def define_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--work', type=str, default='api',
                        choices=['api', 'quant'])

    # Model
    parser.add_argument('--model', type=str, default='gpt3',
                        choices=['gpt3', 'chatgpt', 'gpt4'],
                        help='default gpt3') 

    # Data files
    parser.add_argument('--data-path', type=str, default='./data/pubmed_sample150.csv',
                        help='default data directory. \
                        Write down another path if you want to load your own data')
    parser.add_argument('--settings', type=str, default='./settings.json',
                        help='default settings json file directory.')
    parser.add_argument('--prompt', type=str, default='BASE',
                        help='default prompt name. The prompt file name should be in the format: prompt_{}.txt')
    parser.add_argument('--output-path', type=str, default='./results/',
                        help='default data output directory.')
    parser.add_argument('--checkpoint', type=str, default=None,\
                        help='default None. Designate checkpoint directory if needed.')

    config = parser.parse_args()
    return config

def main(args):
    if not os.path.exists(args.output_path):
        print(f"{args.output_path} does not exist. Creating...")
        os.mkdir(args.output_path)

    if args.work=='api':
        data = load_sentences(args.data_path, 'sentence')
        settings = load_settings(args.settings, args.model)
        prompt = load_prompt(f"prompt_{args.prompt}.txt")
        output_path = args.output_path+'{}-results-{}.csv'

        api = OpenAIAPI(settings)
        result = api.generate_response(data, prompt, args.model, args.checkpoint)

        df = load_data(args.data_path)
        df[f'{args.model}-results'] = result
        df.to_csv(output_path.format(args.model, args.prompt), index=False)
        print('Saved result file')
    
    elif args.work=='quant':
        data = load_data(args.data_path)
        colnames = data.columns[1:]
        output_path = args.output_path+'{}'+f'-{args.prompt}.txt'
        for label1, label2 in combinations(colnames, 2):
            if label1=='label':
                get_confusion_matrix(data, label1, label2, output_path)
                get_macrof1_score(data, label1, label2, output_path)
                get_kappa_score(data, label1, label2, output_path)
            elif label1!='label':
                get_kappa_score(data, label1, label2, output_path)


if __name__ == '__main__':
    config = define_argparser()
    main(config)
