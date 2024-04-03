import torch
from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


class Emobeddings:
    def __init__(self, emotions):
        self.emotion_embeddings = {}
        self.emotions = emotions

    # Corrected to include 'self' and use the correct libraries
    def get_embedding(self, emotion):
        inputs = tokenizer(emotion, return_tensors="pt",
                           padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

    def get_embeddings(self):
        # Generate embeddings for each emotion
        self.emotion_embeddings = {
            emotion: self.get_embedding(emotion) for emotion in self.emotions}
        return self.emotion_embeddings

    def calculate_similarity(self, emotion1, emotion2):
        embedding1 = self.emotion_embeddings[emotion1].flatten()
        embedding2 = self.emotion_embeddings[emotion2].flatten()
        similarity = 1 - cosine(embedding1.detach().numpy(),
                                embedding2.detach().numpy())
        return similarity


if __name__ == "__main__":

    # List of emotions (feel free to add more)
    emotions = ['curious',
                'excited',
                'intrigued',
                'amused',
                'delighted',
                'moved',
                'sympathetic',
                'empathetic',
                'nostalgic',
                'inspired',
                'motivated',
                'anxious',
                'scared',
                'suspenseful',
                'surprised',
                'confused',
                'frustrated',
                'disappointed',
                'sad',
                'angry',
                'satisfied',
                'content',
                'reflective',
                'thoughtful',
                'calm',
                'peaceful',
                'relieved']

    emobeddings = Emobeddings(emotions)
    # Generate embeddings for each emotion
    emobeddings.get_embeddings()

    # Example usage: Calculate similarity between "happy" and "sad"
    user_input = "confused"
    # target_emotion = "delighted"
    # similarity_score = positioning.calculate_similarity(
    #     f"{target_emotion}", f"{user_input}")
    # print(
    #     f"Similarity between {target_emotion} and {user_input}: {similarity_score}")

    for emotion in emotions:
        print(
            f"Similarity between {emotion} and {user_input}: {emobeddings.calculate_similarity(emotion, user_input)}")
