from openai import OpenAI
client = OpenAI()


# story_line = 'You take a deep breath and step into the cave, your senses on high alert. The temperature drops noticeably as you move further inside, and the light from the entrance quickly fades. You fumble in your pack for a torch and light it, casting flickering shadows on the rough stone walls. The passageway narrows, forcing you to proceed single file. As you advance, you notice the ground becoming slick with moisture, making each step treacherous.'

def generate_image_from_story_lines(story_line):
    

  instructions = """In a land of dragons, knights, dungeon, and magic (medieval fantasy era), a human player goes on a journey. Generate an image that describes the storyline below (Do not show any text in the generated image):\n\n"""

  response = client.images.generate(
    model="dall-e-3",
    prompt=instructions+story_line,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url

  return image_url