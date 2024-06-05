import hashlib 
import hmac
import requests

from INITIAL import rtp_val

class CrashGame:
    """
    A class to simulate the Stake crash game.

    Attributes
    ----------
    last_hash : str
        The last hash to generate game from.
    rtp_val : float
        The return to player value for the game.
    """
    def __init__(self, rtp_val=0.99):
        self.rtp_val = rtp_val
        self.hash_chain = []
        print("Generating hash chain...")
        self.generate_hash_chain()

    def fetch_block_hash(self):
        """ Fetch the latest block hash from a Bitcoin blockchain API """
        response = requests.get('https://blockchain.info/q/latesthash')
        block_hash = response.text
        return block_hash

    def generate_hash_chain(self, length=10000000):
        """ Generate a chain of hashes to use in the game """
        current_hash = self.fetch_block_hash()
        for _ in range(length):
            new_hash = hashlib.sha256(current_hash.encode()).hexdigest()
            self.hash_chain.append(new_hash)
            current_hash = new_hash
        self.hash_chain.reverse()

    def calculate_crash_point(self, game_hash):
        hex_result = hmac.new(bytes.fromhex(game_hash), digestmod=hashlib.sha256).hexdigest()[:8]
        int_result = int(hex_result, 16)
        crash_point = max(1, (2 ** 32 / (int_result + 1)) * self.rtp_val)
        return crash_point

    def play_game(self):
        block_hash = self.fetch_block_hash()  # New block hash for each game
        game_hash = hashlib.sha256((self.hash_chain.pop() + block_hash).encode()).hexdigest()
        crash_point = self.calculate_crash_point(game_hash)
        return round(crash_point, 2)



if __name__ == "__main__":
    game = CrashGame(rtp_val)
    crash_point = game.play_game()

    cash_in = input("Enter the amount you want to cash in: ")
    cash_in = float(cash_in)
    multiplier = float(input("Enter the multiplier you want to cash out at: "))

    if multiplier < 1:
        print("Multiplier must be greater than or equal to 1.")
        exit()

    if cash_in <= 0:
        print("Cash in amount must be greater than 0.")
        exit()

    if multiplier > crash_point:
        print(f"Crashed at {crash_point}. You lost!")
        exit()
    else:
        cash_out = cash_in * multiplier
        print(f"Crashed at {crash_point}. You won {cash_out}!")
        exit()

   



