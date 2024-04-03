from app.utils import split_sentences, concatenate_sentences, create_prompt_messages, get_completion_from_messages
from app.similarity import Similarity
# from app.embeddings import Emobeddings


# Create the Adaptator class
class Adaptator:
    def __init__(self, current_text, selected_sentence_index, current_emotion, target_emotion):
        self.current_text = current_text
        self.selected_sentence_index = selected_sentence_index
        self.current_emotion = current_emotion
        self.target_emotion = target_emotion
        self.rephrased_text = None

    def adapt(self):
        # Process the text with the user query
        # indexed_sentences = split_sentences(current_text)
        # print("\n[INDEXED_SENTENCES]:\n", indexed_sentences)

        # Concatenate the sentences before and after (including the selected sentence) the selected sentence
        # previous_sentences, target_sentences = concatenate_sentences(
        #     indexed_sentences, selected_sentence_index)
        # print("\n[PREVIOUS_SENTENCES]:\n", previous_sentences)
        # print("\n[TARGET_SENTENCES]:\n", target_sentences)

        # Define the delimiter to be used for the system message and the user query
        delimiter = "####"

        # Set up the system message to be sent to messages to the model
        system_message = f"""
        You are tasked with rephrasing a specific sentence or surrounding sentences in a given text based on the user's emotional feedback, which is indicated by their chosen sentence index and emotion. The goal is to adjust the sentence to better align with the user's needs—whether it's simplifying the sentence for better comprehension or making it more engaging to alleviate boredom. User feedback is marked using the delimiter {delimiter}. Please adjust the sentence accordingly.
        """

        # Set up the user message to be sent to messages to the model
        user_message = f"""
        Current text: {self.current_text}
        User feedback on emotion:
        {delimiter}{self.current_emotion}{delimiter}
        """

        # Set up the messages to be sent to the model, including the system message and the user query
        messages = [
            {'role': 'system', 'content': system_message.strip()},
            {'role': 'user', 'content': user_message.strip()},
        ]

        # Get the completion from the model API. Rephrase the source text with the user emotion and print the result
        self.rephrased_text = get_completion_from_messages(
            messages, temperature=0.7)

        # Semantic similarity check
        # TODO: Put a threshold for the similarity distance. If below the threshold, rephrase again. <0.9
        similarity_texts = Similarity(self.current_text, self.rephrased_text)
        simlarity_distance = similarity_texts.compare_bert()

        # Calculate emotion embeddings vector similarity
        similarity_emotions = Similarity(
            self.current_emotion, self.target_emotion)
        emotion_distance = similarity_emotions.compare_bert()
        # TODO: Visualize the embeddings on a 2D plane

        # Log the instance of the adaptation
        print(
            f"\nCurrent Emotion: {self.current_emotion}, Target Emotion: {self.target_emotion}")
        print(
            f"Similarity Distance: {simlarity_distance}, Emotion Distance: {emotion_distance}")

        # Save the rephrased text to the output file
        # output_filename = "../logs/rephrased_text_data.txt"

        return self.rephrased_text, simlarity_distance, emotion_distance


if __name__ == "__main__":
    current_text = ("In mathematics, the Hodge conjecture is a major unsolved problem in algebraic geometry and complex geometry "
                    "that relates the algebraic topology of a non-singular complex algebraic variety to its subvarieties. In "
                    "simple terms, the Hodge conjecture asserts that the basic topological information like the number of holes "
                    "in certain geometric spaces, complex algebraic varieties, can be understood by studying the possible nice "
                    "shapes sitting inside those spaces, which look like zero sets of polynomial equations. The latter objects "
                    "can be studied using algebra and the calculus of analytic functions, and this allows one to indirectly "
                    "understand the broad shape and structure of often higher-dimensional spaces which can not be otherwise "
                    "easily visualized. More specifically, the conjecture states that certain de Rham cohomology classes are "
                    "algebraic; that is, they are sums of Poincaré duals of the homology classes of subvarieties.")
    selected_sentence_index = 3
    target_emotion = "interested"
    current_emotion = "confused"

    adpt = Adaptator(current_text, selected_sentence_index,
                     target_emotion, current_emotion)

    adpt.adapt()
