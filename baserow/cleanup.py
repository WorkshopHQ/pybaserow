from dotenv import load_dotenv

from baserow import login

load_dotenv()

token = login()
print(token)
