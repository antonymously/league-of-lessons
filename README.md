# League of Lessons

This application contains the League of Lessons. An educational LLM-based tabletop RPG that helps teachers and students learn a study material in an engaging and entertaining manner.

## Setting up on your Local Device

Download [Anaconda](https://www.anaconda.com/download) and install [Git](https://git-scm.com/downloads).

Open Anaconda Prompt, and then run ```git init``` .

To clone the [League of Lessons repository](https://github.com/antonymously/league-of-lessons), run the command snippet below. This will download the necessary library requirements to run the app.

```sh
git clone https://github.com/antonymously/league-of-lessons.git
```

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

Before running the application, you will need some API keys in a `.env` file.

Make a copy of the `.env.example` file, then rename it to `.env`.

Open the `.env` file and input your API keys:

1. Anthropic API Key
    - Create an [Anthropic API key](https://console.anthropic.com/settings/keys).
    - Record your key as you will not be able to view it again.
    - Input your key in the `.env` file: `ANTHROPIC_API_KEY=<input your key here>`

2. OpenAI API Key
    - Create an [OpenAI API key](https://openai.com/index/openai-api/).
    - Record your key as you will not be able to view it again.
    - Input your key in the `.env` file: `OPENAI_API_KEY=<input your key here>`

3. (Optional) Playht
    - Create a [Playht API key](https://play.ht/app/api-access).
    - Input your User ID and Secret key in the `.env` file:
        - `PYHT_USER_ID=<input your User ID here>`
        - `PYHT_SECRET=<input your secret key here>`

## Running the Application

To run the application, do the following command:

```sh
streamlit run app.py
```

## How to use the Application/Demo Guide 
There are 2 ways in which you can navigate through the application. You can either play as a teacher or as a student. Each type of user has its specific features unique to them. 

You can either view as a teacher or as a student

As a teacher you can test out the application by doing the following commands: 
1. Select view as a teacher in the upper right corner 
2. Input and save your own API keys using “Manage API keys”
3. As part of the demo, upload study material in the form of .txt or .pdf to generate study questions. You can refer to the the following links to download necessary materials to test the generation of questions of the application
    a. Biology : https://www.researchgate.net/publication/348327156_Biology_Notes
4. Upon uploading you may also specify how many questions to generate and Verify correctness of questions generated from study material manually for teacher role
5. Verify the answers of the generated questions then click save if you are already satisfied. 
6. Once questions are generated this will be saved into the application and students will be able to play the game.

As a student, you can do the following:
1. Start a new game/story and choose a specific study material to use
2. Based on study material chosen, students will be given a D&D storyline related to this wherein key questions are integrated into the overall storyline. 
3. As students progress through the overall story, there will be prompted various questions based on the material uploaded by the teacher.
