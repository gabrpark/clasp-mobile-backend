import torch
import spacy
from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer, BertModel, BertTokenizer
from openai import OpenAI
from transformers import T5EncoderModel, T5Tokenizer

openai = OpenAI()


class Similarity:
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2

    def compare_bert(self):
        # Load pre-trained model and tokenizer
        model_name = 'bert-base-uncased'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertModel.from_pretrained(model_name)

        # Encode the texts
        inputs1 = tokenizer(self.text1, return_tensors="pt",
                            padding=True, truncation=True)
        inputs2 = tokenizer(self.text2, return_tensors="pt",
                            padding=True, truncation=True)

        # Generate embeddings
        with torch.no_grad():
            outputs1 = model(**inputs1)
            outputs2 = model(**inputs2)

        # Use the mean of the last hidden states as the sentence embedding
        embedding1 = outputs1.last_hidden_state.mean(dim=1).numpy()[0]
        embedding2 = outputs2.last_hidden_state.mean(dim=1).numpy()[0]

        # Compute cosine similarity
        similarity = 1 - cosine(embedding1, embedding2)

        return similarity

    def compare_llama2(self):
        model_name = 'meta-llama/Llama-2-7b-chat-hf'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        text1 = self.text1
        text2 = self.text2

        # Encode the texts
        inputs1 = tokenizer(text1, return_tensors="pt",
                            padding=True, truncation=True)
        inputs2 = tokenizer(text2, return_tensors="pt",
                            padding=True, truncation=True)

        # Generate embeddings
        with torch.no_grad():
            outputs1 = model(**inputs1)
            outputs2 = model(**inputs2)

        # Use the mean of the last hidden states as the sentence embedding
        embedding1 = outputs1.last_hidden_state.mean(dim=1).numpy()[0]
        embedding2 = outputs2.last_hidden_state.mean(dim=1).numpy()[0]

        # Compute cosine similarity
        similarity = 1 - cosine(embedding1, embedding2)

        return similarity

    def compare_t5(self):
        # Initialize the T5 model and tokenizer
        model_name = 't5-small'  # You can choose other sizes like 't5-base', 't5-large'
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5EncoderModel.from_pretrained(model_name)

        # Function to generate embeddings using T5

        def get_embedding(text, tokenizer, model):
            inputs = tokenizer(text, return_tensors="pt",
                               padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model(input_ids=inputs.input_ids,
                                attention_mask=inputs.attention_mask)
            # Return the mean of the embeddings
            return outputs.last_hidden_state.mean(dim=1).numpy()

        # Define the texts to compare
        text1 = self.text1
        text2 = self.text2

        # Generate embeddings
        embedding1 = get_embedding(text1, tokenizer, model).flatten()
        embedding2 = get_embedding(text2, tokenizer, model).flatten()

        # Compute cosine similarity between the embeddings
        similarity = 1 - cosine(embedding1, embedding2)

        return similarity
