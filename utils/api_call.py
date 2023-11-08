import openai
import time
import os
import pickle

class OpenAIAPI:
    def __init__(self, settings):
        self.settings = settings
        openai.api_key = self.settings["key"]
    
    def gpt_response(self, message):
        try:
            response = openai.Completion.create(
                        prompt=message,
                        temperature=self.settings['temperature'],
                        max_tokens=self.settings['max_tokens'],
                        model=self.settings['model']
                    )
            gpt_answer = response['choices'][0]['text'].strip("\n").lower()
            return gpt_answer
        
        except openai.error.RateLimitError as e:
            # Handle rate limit error
            print(f"Rate limited. Error message: {e}")
            # Wait for 60 seconds before retrying
            print("Waiting for 60 seconds to start again...")
            time.sleep(60)
            # Retry the API call
            return self.gpt_response(message)

    def chatgpt_response(self, message):
        try:
            response = openai.ChatCompletion.create(
                        model=self.settings['model'],
                        messages=[
                            {"role": "user", "content": message}
                            ]
                    )
            chatgpt_answer = response['choices'][0]['message']['content'].strip("\n").lower()
            return chatgpt_answer
        except openai.error.RateLimitError as e:
            # Handle rate limit error
            print(f"Rate limited. Error message: {e}")
            # Wait for the recommended duration before retrying
            print("Waiting for 60 seconds to start again...")
            time.sleep(60)
            # Retry the API call
            return self.chatgpt_response(message)
    
    def generate_response(self, data, prompt, model, ckpt):
        i = 0
        result = []
        if ckpt:
            with open(ckpt, 'rb') as f:
                result = pickle.load(f)
            i = len(result)
            data = data[i:]

        for sent in data:
            if len(sent)==0: break
            
            print(i)
            message = prompt.format(sent)

            if model=='gpt3':
                answer = self.gpt_response(message)
            elif model=='chatgpt' or model=='gpt4':
                answer = self.chatgpt_response(message)
            result.append(answer)
            i += 1
            
            # Save partial response
            CKPT = "./results/ckpt/"
            if not os.path.exists(CKPT):
                print(f"{CKPT} does not exist. Creating...")
                os.mkdir(CKPT)
            with open(f"{CKPT}{model}_result_part.pkl", "wb") as f:
                pickle.dump(result, f)
        print('---Done')
        return result