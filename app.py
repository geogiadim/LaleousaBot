from dotenv import load_dotenv
from bot import Laleousa
import os

load_dotenv()


def main():
    bot = Laleousa()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
