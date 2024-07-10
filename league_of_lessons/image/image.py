from league_of_lessons import OPENAI_CLIENT

def generate_image_from_story_lines(story_line):
    
  instructions = """In a land of dragons, knights, dungeon, and magic (medieval fantasy era), a human player goes on a journey. Generate an image that describes the storyline below (Do not show any text in the generated image):\n\n"""

  response = OPENAI_CLIENT.images.generate(
    model="dall-e-3",
    prompt=instructions+story_line,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url

  return image_url