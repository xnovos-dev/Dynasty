from discord.ext import commands
from discord import app_commands
import discord
import random

COG = True

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    Fun = app_commands.Group(name="fun", description="Fun commands")

    @Fun.command(name="random-int", description="Gets a random integer between a range of numbers")
    @app_commands.describe(min="The minimum number", max="The maximum number")
    async def random_int(self, interaction: discord.Interaction, min: int = 1, max: int = 100):
        if min > max:
            min, max = max, min
        
        result = random.randint(min, max)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Random Integer",
            description=f"> **Range:** `{min}` to `{max}`\n> **Result:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="8ball", description="Ask the magic 8ball a question")
    @app_commands.describe(question="The question to ask")
    async def eightball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Yes", "No", "Maybe", "Definitely", "Absolutely not",
            "I don't know", "Ask again later", "Probably", "Unlikely",
            "Without a doubt", "Very doubtful", "Signs point to yes"
        ]
        
        result = random.choice(responses)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | 8ball",
            description=f"> **Question:** {question}\n> **Answer:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="coinflip", description="Flip a coin")
    async def coinflip(self, interaction: discord.Interaction):
        result = random.choice(["Heads", "Tails"])
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Coin Flip",
            description=f"> **Result:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="roll", description="Roll a dice (6-sided)")
    async def roll(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Dice Roll",
            description=f"> **You rolled:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="choose", description="Choose from a list of options (separate with commas)")
    @app_commands.describe(options="The options to choose from, separated by commas")
    async def choose(self, interaction: discord.Interaction, options: str):
        choices = [opt.strip() for opt in options.split(",")]
        
        if len(choices) < 2:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | Choose",
                description="> **Please provide at least 2 options separated by commas!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        result = random.choice(choices)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Choose",
            description=f"> **Options:** {', '.join([f'`{opt}`' for opt in choices])}\n> **Chosen:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="rps", description="Play rock paper scissors")
    @app_commands.describe(choice="Your choice")
    @app_commands.choices(choice=[
        app_commands.Choice[str](name="Rock", value="rock"),
        app_commands.Choice[str](name="Paper", value="paper"),
        app_commands.Choice[str](name="Scissors", value="scissors")
    ])
    async def rps(self, interaction: discord.Interaction, choice: str = "rock"):
        choices = ["rock", "paper", "scissors"]
        user_choice = choice.lower()
        
        bot_choice = random.choice(choices)
        
        if user_choice == bot_choice:
            result = "Tie!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "Dynasty wins!"
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Rock Paper Scissors",
            description=f"> **Your choice:** `{user_choice}`\n> **Dynasty's choice:** `{bot_choice}`\n> **Result:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="random-color", description="Get a random color")
    async def random_color(self, interaction: discord.Interaction):
        color = discord.Color(random.randint(0, 0xFFFFFF))
        
        hex_code = format(color.value, '06x').upper()
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Random Color",
            description=f"> **Hex:** `#{hex_code}`",
            color=color
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="fact", description="Get a random fun fact")
    async def fact(self, interaction: discord.Interaction):
        facts = [
            "Honey never spoils - archaeologists found 3000-year-old honey in Egyptian tombs that was still edible.",
            "Octopuses have three hearts and blue blood.",
            "A day on Venus is longer than a year on Venus.",
            "Bananas are berries, but strawberries aren't.",
            "The shortest war in history lasted 38-45 minutes between Britain and Zanzibar in 1896.",
            "A group of flamingos is called a 'flamboyance'.",
            "The unicorn is the national animal of Scotland.",
            "The world's oldest known living tree is over 5,000 years old.",
            "There are more stars in the universe than grains of sand on all Earth's beaches.",
            "Dolphins sleep with one eye open.",
            "A jiffy is an actual unit of time: 1/100th of a second.",
            "The Eiffel Tower can grow 15 centimeters taller during hot summer days."
        ]
        
        result = random.choice(facts)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Fun Fact",
            description=f"> {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="guess-number", description="Guess a number between 1-100")
    @app_commands.describe(guess="Your guess (1-100)")
    async def guess_number(self, interaction: discord.Interaction, guess: int = 50):
        number = random.randint(1, 100)
        
        if guess == number:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | Guess Number",
                description=f"> **Your guess:** `{guess}`\n> **Number:** `{number}`\n> **Result:** 🎉 Correct!",
                color=100
            )
        elif guess > number:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | Guess Number",
                description=f"> **Your guess:** `{guess}`\n> **Number:** `{number}`\n> **Result:** Too high!",
                color=100
            )
        else:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | Guess Number",
                description=f"> **Your guess:** `{guess}`\n> **Number:** `{number}`\n> **Result:** Too low!",
                color=100
            )
        
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="joke", description="Get a random joke")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "Why don't scientists trust atoms?\n> Because they make up everything!",
            "Why did the scarecrow win an award?\n> Because he was outstanding in his field!",
            "What do you call a fake noodle?\n> An impasta!",
            "Why don't eggs tell jokes?\n> They'd crack each other up!",
            "What did the ocean say to the beach?\n> Nothing, it just waved.",
            "Why did the math book look so sad?\n> Because it had too many problems.",
            "What do you call a bear with no teeth?\n> A gummy bear!",
            "How does a penguin build its house?\n> Igloos it together!",
            "Why did the bicycle fall over?\n> Because it was two-tired!",
            "What do you call a dog that does magic tricks?\n> A Labracadabrador!",
            "Why did the coffee file a police report?\n> It got mugged!",
            "What do you call a lazy kangaroo?\n> A pouch potato!"
        ]
        
        result = random.choice(jokes)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Joke",
            description=f"> {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="wyr", description="Would you rather...")
    async def wyr(self, interaction: discord.Interaction):
        questions = [
            "Would you rather be able to fly or be invisible?",
            "Would you rather have unlimited money or unlimited time?",
            "Would you rather live in the past or the future?",
            "Would you rather be a famous actor or a famous musician?",
            "Would you rather always have to say everything on your mind or never be able to speak again?",
            "Would you rather be able to talk to animals or speak all human languages?",
            "Would you rather have super strength or super speed?",
            "Would you rather explore space or the ocean?",
            "Would you rather be the smartest person or the happiest person?",
            "Would you rather have no phone or no computer for a year?",
            "Would you rather fight one horse-sized duck or 100 duck-sized horses?",
            "Would you rather have a rewind button or a pause button in your life?"
        ]
        
        result = random.choice(questions)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Would You Rather",
            description=f"> {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="meme", description="Get a random meme category")
    @app_commands.describe(category="The category of meme")
    @app_commands.choices(category=[
        app_commands.Choice[str](name="Random", value="random"),
        app_commands.Choice[str](name="Animal", value="animal"),
        app_commands.Choice[str](name="Coding", value="coding"),
        app_commands.Choice[str](name="Gaming", value="gaming")
    ])
    async def meme(self, interaction: discord.Interaction, category: str = "random"):
        memes = {
            "random": [
                "When you finally fix that bug but create three more...",
                "Me: *sets alarm* Also me: *wakes up 1 hour earlier*",
                "That moment when you realize you've been on Reddit for 4 hours..."
            ],
            "animal": [
                "When your cat brings you a dead mouse as a gift 🐱",
                "Dogs: 95% good bois, 100% good girls 🐕",
                "When the hamster runs on its wheel at 3am 🐹"
            ],
            "coding": [
                "It works on my machine - Classic Developer Quote 💻",
                "console.log('debugging...') - The only debugging many do",
                "Stack Overflow: Where we copy-paste our way to success 📋"
            ],
            "gaming": [
                "One more turn... it's 4am now 🎮",
                "When your team goes 0-5 in the first 5 minutes 🎮",
                "Lag: The only enemy that never misses 🎯"
            ]
        }
        
        if category == "random":
            all_memes = sum(memes.values(), [])
            result = random.choice(all_memes)
        else:
            result = random.choice(memes.get(category, memes["random"]))
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Meme",
            description=f"> {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="slot", description="Play slot machine")
    async def slot(self, interaction: discord.Interaction):
        emojis = ["🍒", "🍋", "🍊", "🍇", "⭐", "🔔"]
        
        slots = [random.choice(emojis) for _ in range(3)]
        
        if slots[0] == slots[1] == slots[2]:
            result = "🎉 JACKPOT! 🎉"
        elif slots[0] == slots[1] or slots[1] == slots[2] or slots[0] == slots[2]:
            result = "Nice! You got a pair!"
        else:
            result = "Better luck next time!"
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Slot Machine",
            description=f"> **{slots[0]} | {slots[1]} | {slots[2]}**\n> **Result:** {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="shuffle", description="Shuffle a list of items")
    @app_commands.describe(items="The items to shuffle, separated by commas")
    async def shuffle(self, interaction: discord.Interaction, items: str):
        item_list = [item.strip() for item in items.split(",")]
        
        if len(item_list) < 2:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | Shuffle",
                description="> **Please provide at least 2 items separated by commas!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        random.shuffle(item_list)
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Shuffle",
            description=f"> **Original:** `{items}`\n> **Shuffled:** {', '.join([f'`{item}`' for item in item_list])}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="number", description="Get a random fun number fact")
    @app_commands.describe(number="A specific number (optional)")
    async def number(self, interaction: discord.Interaction, number: int = None):
        if number is None:
            number = random.randint(1, 1000)
        
        facts = {
            7: "7 is considered the luckiest number in many cultures!",
            13: "13 is often considered an unlucky number in Western cultures.",
            42: "42 is the answer to life, the universe, and everything (Hitchhiker's Guide)!",
            100: "100 is a perfect score in many tests!",
            365: "There are 365 days in a year!",
            1000: "1000 is the number of years in a millennium!"
        }
        
        result = facts.get(number, f"The number {number} is special in its own way!")
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Number Fact",
            description=f"> **Number:** `{number}`\n> **Fact:** {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="rock-paper-scissors-lizard-spock", description="Play the extended RPSLS game")
    @app_commands.describe(choice="Your choice")
    @app_commands.choices(choice=[
        app_commands.Choice[str](name="Rock", value="rock"),
        app_commands.Choice[str](name="Paper", value="paper"),
        app_commands.Choice[str](name="Scissors", value="scissors"),
        app_commands.Choice[str](name="Lizard", value="lizard"),
        app_commands.Choice[str](name="Spock", value="spock")
    ])
    async def rpsls(self, interaction: discord.Interaction, choice: str = "rock"):
        choices = ["rock", "paper", "scissors", "lizard", "spock"]
        user_choice = choice.lower()
        
        if user_choice not in choices:
            embed = discord.Embed(
                title="<:extension:1473327064458330237> | Dynasty | RPSLS",
                description="> **Please choose:** `rock`, `paper`, `scissors`, `lizard`, or `spock`",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        bot_choice = random.choice(choices)
        
        wins = {
            "rock": ["scissors", "lizard"],
            "paper": ["rock", "spock"],
            "scissors": ["paper", "lizard"],
            "lizard": ["spock", "paper"],
            "spock": ["scissors", "rock"]
        }
        
        if user_choice == bot_choice:
            result = "Tie!"
        elif bot_choice in wins[user_choice]:
            result = "You win!"
        else:
            result = "Dynasty wins!"
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | RPSLS",
            description=f"> **Your choice:** `{user_choice}`\n> **Dynasty's choice:** `{bot_choice}`\n> **Result:** `{result}`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Fun.command(name="emoji", description="Convert text to emoji")
    @app_commands.describe(text="The text to convert")
    async def emoji(self, interaction: discord.Interaction, text: str):
        emoji_map = {
            'a': '🅰️', 'b': '🅱️', 'c': '©️', 'd': '🅿️', 'e': '📧',
            'f': '🫱', 'g': '🇬', 'h': '♓', 'i': 'ℹ️', 'j': '🎹',
            'k': '🇰', 'l': '🟗', 'm': 'Ⓜ️', 'n': '🇳', 'o': '🅾️',
            'p': '🅿️', 'q': '🇶', 'r': '®️', 's': '💲', 't': '✝️',
            'u': '🇺', 'v': '✅', 'w': '🇼', 'x': '❌', 'y': '🇾',
            'z': '🇿', '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣',
            '4': '4️⃣', '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣',
            '9': '9️⃣', '!': '❗', '?': '❓', '*': '⭐'
        }
        
        result = ' '.join([emoji_map.get(c.lower(), c) for c in text])
        
        embed = discord.Embed(
            title="<:extension:1473327064458330237> | Dynasty | Emoji",
            description=f"> **Input:** {text}\n> **Output:** {result}",
            color=100
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
