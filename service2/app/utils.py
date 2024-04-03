from openai import OpenAI
from dotenv import load_dotenv
import spacy


nlp = spacy.load("en_core_web_sm")


def split_sentences(text):
    """
    Indexes and separates sentences from a given text using SpaCy's language model.

    This function utilizes SpaCy's natural language processing capabilities to segment
    a given text into sentences. Each sentence is then paired with its corresponding index,
    creating a list of tuples. Each tuple contains an index and the sentence at that index.

    :param text: A string of text to be segmented into sentences.
    :return: A list of tuples, where each tuple contains an index and a sentence.
    """

    # Process the text using SpaCy's NLP pipeline to get a Doc object
    doc = nlp(text)

    # Extract sentences from the Doc and strip any leading/trailing whitespace
    sentences = [sent.text.strip() for sent in doc.sents]

    # Enumerate over the sentences to pair each sentence with its index
    indexed_sentences = [(index, sentence)
                         for index, sentence in enumerate(sentences)]

    return indexed_sentences


def concatenate_sentences(indexed_sentences, start_index):
    """
    Concatenates sentences from a given index to the end of the list.
    If the start_index is out of range, returns an empty string.
    If the start_index is the first index in the list, returns all sentences concatenated.
    If the start_index is the last index in the list, returns only that sentence.

    :param indexed_sentences: List of tuples where each tuple contains (index, sentence) :param start_index: The
    index from which to start concatenation :return: A tuple of strings, where the first string is the concatenated
    string before the start_index, and the second string is the concatenated string after the start_index
    """

    # Check if start_index is out of range
    if start_index >= len(indexed_sentences):
        return '', ''

    # Check if start_index is the first index in the list
    if start_index == 0:
        return '', ' '.join([sentence for idx, sentence in indexed_sentences[:]])

    # Check if start_index is the last index in the list
    if start_index + 1 == len(indexed_sentences):
        all_before_last = [sentence for idx,
                           sentence in indexed_sentences[:-1]]
        return ' '.join(all_before_last), indexed_sentences[start_index][1]

    # Filter sentences before 'start_index'
    all_before_start_index = [sentence for idx,
                              sentence in indexed_sentences[:start_index + 1]]

    # Filter sentences starting from 'start_index'
    all_after_start_index = [sentence for idx,
                             sentence in indexed_sentences[start_index + 1:]]

    # Concatenate the sentences
    concatenated_string_before = ' '.join(all_before_start_index)
    concatenated_string_after = ' '.join(all_after_start_index)

    return concatenated_string_before, concatenated_string_after


def create_prompt_messages(original_text, previous_sentences, target_sentences, user_input2):
    """
    Creates the messages to be sent to the model.

    :param original_text: A string of text to be rephrased.
    :param previous_sentences: A string of text containing the previous sentences.
    :param target_sentences: A string of text containing the target sentences.
    :param user_input2: A string of text containing the user emotional response.
    """

    # Assign the original text
    original_text = original_text

    # Assign the previous sentences
    previous_sentences = previous_sentences

    # Assign the target sentences
    target_sentences = target_sentences

    # Assign the user query
    user_input2 = user_input2

    # Define the delimiter to be used for the system message and the user query
    delimiter = "####"

    # Set up the system message to be sent to messages to the model
    system_message = f"""
        You rephrase the target text based on user's emotional feedback.
        Refer the previous text for the context.
        The user's' feedback will be delimited with four hashtags,\
        i.e. {delimiter}.
        
        Previous text: {previous_sentences}
        Target text: {target_sentences}
        """

    # Set up the user message to be sent to messages to the model
    user_message = f"""
        {user_input2}"""

    # Set up the messages to be sent to the model, including the system message and the user query
    messages = [
        {'role': 'system',
         'content': system_message},
        {'role': 'user',
         'content': f"{delimiter}{user_message}{delimiter}"
         },
    ]

    return messages


# Load environment variables from .env file
load_dotenv()
client = OpenAI()


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.0):
    """
    This function sends the input text to the LLM for rephrasing.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":

    text = ("In mathematics, the Hodge conjecture is a major unsolved problem in algebraic geometry and complex geometry "
            "that relates the algebraic topology of a non-singular complex algebraic variety to its subvarieties. In "
            "simple terms, the Hodge conjecture asserts that the basic topological information like the number of holes "
            "in certain geometric spaces, complex algebraic varieties, can be understood by studying the possible nice "
            "shapes sitting inside those spaces, which look like zero sets of polynomial equations. The latter objects "
            "can be studied using algebra and the calculus of analytic functions, and this allows one to indirectly "
            "understand the broad shape and structure of often higher-dimensional spaces which can not be otherwise "
            "easily visualized. More specifically, the conjecture states that certain de Rham cohomology classes are "
            "algebraic; that is, they are sums of Poincaré duals of the homology classes of subvarieties.")
    indexed_sentences = split_sentences(text)
    print(indexed_sentences)
    print(len(indexed_sentences))

    # Example usage
    # indexed_sentences = [(0,
    #                       'In mathematics, the Hodge conjecture is a major unsolved problem in algebraic geometry and '
    #                       'complex geometry that relates the algebraic topology of a non-singular complex algebraic '
    #                       'variety to its subvarieties.'),
    #                      (1,
    #                       'In simple terms, the Hodge conjecture asserts that the basic topological information like the '
    #                       'number of holes in certain geometric spaces, complex algebraic varieties, can be understood by '
    #                       'studying the possible nice shapes sitting inside those spaces, which look like zero sets of '
    #                       'polynomial equations.'),
    #                      (2,
    #                       'The latter objects can be studied using algebra and the calculus of analytic functions, '
    #                       'and this allows one to indirectly understand the broad shape and structure of often '
    #                       'higher-dimensional spaces which can not be otherwise easily visualized.'),
    #                      (3,
    #                       'More specifically, the conjecture states that certain de Rham cohomology classes are '
    #                       'algebraic; that is, they are sums of Poincaré duals of the homology classes of '
    #                       'subvarieties.')]

    # indexed_sentences = [(0,
    #                       'a'),
    #                      (1,
    #                       'b'),
    #                      (2,
    #                       'c'),
    #                      (3,
    #                       'd')]

    # start_index = 0

    # for start_index in range(0, len(indexed_sentences)):
    #     result = concatenate_sentences(indexed_sentences, start_index)
    #     print(result)
    #     print(len(result))
