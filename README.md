# League of Lessons

This application contains the League of Lessons. An educational LLM-based tabletop RPG that helps teachers and students
to learn a study material in an engaging and entertaining manner.

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

## Running the Application

To run the application, do the following command:

```sh
streamlit run app.py
```