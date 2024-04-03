# Adaptive Text through Interaction Using Mobile Application

## Description
This is a capstone project for the Master of Science in Data Science program at the Rochester Institute of Technology (RIT). The project aims to develop an interactive machine learning system using a mobile application that rephrases text using a Large Language Model (LLM) and adapts to the user's emotional response to the rephrased text. The application is built using the Flutter framework and using the OpenAI API.
This system sends a user-input text to the OpenAI API, receives a rephrased version, and logs the original, user inputs, and rephrased text to a file.

## Installation

### Prerequisites
- Python 3.8
- OpenAI API key

### Setup
1. **Clone the repository**
    ```bash
    git clone https://github.com/gabrpark/Adaptive-Text.git
    cd Adaptive-Text
    ```

2. **Create and activate a virtual environment (optional but recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your OpenAI API key**
    - Create a `.env` file in the project root.
    - Add your API key to the file:
        ```bash
        OPENAI_API_KEY='your-api-key-here'
        ```

## Usage

Run the main script from the command line:

```bash
python src/main.py
```

The program will output the rephrased text and log both the original and rephrased versions to `logs/rephrased_text_data.txt`.

The adjustable parameters are:
- `original_text (Straing)`: The text to be rephrased.
- `user_input (Int)`: The index of the sentence where the user wants to start rephrasing.
- `user_input2 (String)`: The user's emotional response to the text.

## Structure

- `src/`: Contains the source code.
    - `main.py`: Runs the main script.
    - `create_prompt_message.py`: Creates the prompt message for OpenAI API.
    - `get_completion_from_messages.py`: Sends the prompt message to OpenAI API and returns the generated text.
    - `logger.py`: Manages logging functionalities.
    - `index_sentences.py`: Indexes the sentences into a tuple and returns a list of tuples (index, sentence).
    - `concatenate_from_index.py`: Concatenates the sentences from the index and returns strings of before and after the index.
- `data/`: Stores the original text.
- `logs/`: Stores the logs of rephrased texts.
- `tests/`: Contains unit tests for the application.
- `requirements.txt`: Lists the Python dependencies for the project.

## Testing

Run the unit tests from `tests` directory

## Next Steps
The next steps for this project are:
- Further test the output of the API with prompt engineering.
- Change the log output format to csv, or other format that can be easily read by other applications.
- Create a database to store the logs.
- Implement the semantic similarity algorithm to compare the original and rephrased text.
- Apply advanced OOP design principles to the application. Class, inheritance, etc, if necessary.
- Implement touchable text to allow the user to select the text to be rephrased.
- Test with the Flutter app.
- Integrate the application with a mobile application and database.