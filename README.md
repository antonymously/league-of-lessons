# League of Lessons

This application contains the League of Lessons. An educational LLM-based tabletop RPG that helps teachers and students learn a study material in an engaging and entertaining manner.

## Library Requirements Installation

To install the necessary libraries for this application, run the command snippet below.
This will create a `league-of-lessons` conda environment.

```sh
conda env create -f environment.yml
```

Alternatively, you may create you own virtual environment and install the using
the `requirements.txt` directly.

```sh
pip install -r requirements.txt
```

## Getting API Keys

To run the application, you will need API keys from Anthropic, OpenAI and (Optional) PlayHT.
These can be acquired thru the following platforms:
1. Anthropic: https://console.anthropic.com
2. OpenAI: https://platform.openai.com/
3. PlayHT: https://play.ht

Once obtained, you can use these by creating a .env file or using the 'Manage API Keys' page in the app.

## Running the Application

To run the application, do the following command:

```sh
streamlit run app.py
```