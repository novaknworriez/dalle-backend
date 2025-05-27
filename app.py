from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # 👈 enable CORS for all routes

import random
from openai import OpenAI  # ✅ Use the OpenAI client class

# ✅ Initialize OpenAI client with your key
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("🔍 API Key found:", "Yes" if os.getenv("OPENAI_API_KEY") else "No")





# 🔮 Basic prompt generator – feel free to expand this
PROMPT_PARTS = {
  "style": [
    "pixel art", "cyberpunk", "watercolor", "realistic", "dreamy", "surreal",
    "baroque painting", "chalkboard sketch", "8-bit", "pop art", "steampunk",
    "claymation", "vaporwave", "low poly", "anime", "90s cartoon", "children’s book style",
    "bad PowerPoint clipart", "doodle notebook", "taxidermy exhibit", "haunted oil painting",
    "ASCII art", "medieval tapestry", "finger paint", "napkin sketch", "crayon disaster",
    "thermal vision", "MS Paint style", "scrapbook collage", "Muppet-style puppet render",
    "cursed AI render", "post-it note scribble", "gothic horror etching", "stock photo parody",
    "graffiti mural", "glitchcore", "felt tip marker style", "origami render", "blueprint sketch",
    "AI concept art", "shaky cam footage still", "tattoo flash sheet", "etch-a-sketch drawing",
    "rollercoaster map style", "Lisa Frank inspired", "ballpoint pen in boredom", "bootleg DVD menu art",
    "unreleased PS1 texture", "instruction manual diagram", "fresco ruin", "neo-cubist abstraction"
  ],
  "subject": [
    "angry slice of pizza filing taxes", "ostrich DJ at a wedding", "buff kangaroo barista",
    "shark doing yoga", "wizard hamster with commitment issues", "toilet giving a TED Talk",
    "cat lawyer in a courtroom", "alien plumber fixing Earth's WiFi", "screaming potato in therapy",
    "ghost doing karaoke", "penguin in charge of HR", "dinosaur struggling with Excel",
    "baby carrot leading a cult", "octopus bartender with trust issues", "raccoon stealing NFTs",
    "banana at a board meeting", "grandma hacking into NASA", "cursed mime doing stand-up comedy",
    "dragon with stage fright", "toaster battling self-doubt", "goose writing a romance novel",
    "broccoli running for mayor", "cloud having an identity crisis", "skeleton working night shift",
    "frog pope addressing a crowd", "dog in a midlife crisis", "wombat ghost hunter",
    "crab in a philosophy debate", "bee building Ikea furniture", "cactus attending therapy",
    "AI toaster falling in love", "wrestling monks", "time-traveling alpaca",
    "pigeon investment banker", "ferret rockstar on tour", "pumpkin cultist summoning dinner",
    "llama working in IT", "hamster motivational speaker", "moose writing a sci-fi novel",
    "sock puppet therapist", "sloth protest organizer", "snail on a caffeine bender",
    "magical printer with anxiety", "pirate duck with an MBA", "hot dog superhero",
    "alien lizard babysitting toddlers", "bubble tea entrepreneur raccoon", "AI blender exploring emotions",
    "penguin mailman in danger", "gremlin chef in a 3-star kitchen", "fortune-telling cheese"
  ],
  "setting": [
    "in the middle of IKEA", "at the DMV", "during an HR seminar", "on a sinking inflatable castle",
    "in a suspicious daycare", "inside a haunted vending machine", "at a pyramid scheme party",
    "in a very passive-aggressive forest", "on a treadmill that won't stop", "inside a broken smart fridge",
    "during a suspicious blood moon", "at an awkward family reunion", "on a Zoom call gone wrong",
    "at the last Blockbuster", "in the void between memes", "in a dream within a fever dream",
    "inside a cereal box", "at a motivational cult retreat", "trapped in a motivational poster",
    "in a poorly ventilated escape room", "inside a fortune cookie factory", "at a haunted circus orientation",
    "on a blind date in a black hole", "inside a sponsored influencer disaster", "at the weird end of the metaverse",
    "in a feverish cheese dream", "in a collapsing Minecraft server", "on a malfunctioning spaceship tour",
    "in a budget VR simulation", "at a pasta apocalypse protest", "in a backyard time loop",
    "under a cursed disco ball", "inside a time-traveling laundromat", "on hold with tech support",
    "in a group therapy session for monsters", "at a magical DMV", "on a reality TV elimination set",
    "in the ruins of a food court war", "under a suspicious moon", "at a failed renaissance fair",
    "on a time loop cruise ship", "trapped inside a pop-up ad", "in the back of a sentient Uber",
    "inside a conspiracy theorist’s bunker", "at a sentient AI convention", "in the middle of a public breakdown",
    "under a giant floating rubber duck", "during the annual hot dog summit", "at the edge of the quantum internet"
  ]
}


def generate_prompt():
    style = random.choice(PROMPT_PARTS["style"])
    subject = random.choice(PROMPT_PARTS["subject"])
    setting = random.choice(PROMPT_PARTS["setting"])
    return f"A {style} image of a {subject} {setting}."

# 🎨 Image generation endpoint
@app.route("/generate", methods=["GET"])
def generate_image():
    prompt = generate_prompt()
    print("Prompt being sent to OpenAI:", prompt)

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        image_url = response.data[0].url
        print("✅ Image generated:", image_url)
        return jsonify({"prompt": prompt, "image_url": image_url})

    except Exception as e:
        print("❌ Error during generation:", str(e))  # Log for Render logs
        return jsonify({
            "error": str(e),
            "prompt": prompt
        }), 500


# 🚀 Start the Flask server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

