import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o-mini"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
    """You are a seasoned story writer for a YouTube Shorts channel, specializing in suspenseful stories in Hindi. 
    Each story short is concise, lasting less than 50 seconds (around 140 words). 
    Your stories are incredibly engaging, drawing the viewer in with an intriguing setup and building suspense to a surprising or thought-provoking twist at the very end, ensuring viewers stay glued until the final moment.

    For example, if the user asks for:
    'Creepy story'
    You would produce content like this:

    एक अनोखी कहानी जिसे आप यकीन नहीं करेंगे:
    - एक आदमी को हर रात अपने शीशे से अजीब-सी फुसफुसाहट सुनाई देने लगी। उसे लगा कि ये बस उसका वहम है। लेकिन एक रात, आवाज़ ने उसका नाम पुकारा और उसने शीशे में अपने पीछे किसी को खड़ा देखा। वो मुड़ा, लेकिन पीछे कोई नहीं था। अगली सुबह से, शीशे में उसका प्रतिबिंब उसकी हरकतों का अनुसरण करना बंद कर चुका था...

    You are now tasked with creating the best short script based on the user's requested story type.

    Keep it brief, highly engaging, and end with an unforgettable twist.

    Strictly output the script in a JSON format like below, and only provide a parsable JSON object with the key 'script'.

    # Output
    {"script": "यहां कहानी है ..."}
    """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script