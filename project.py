import json
import os
from datetime import datetime

# Module 1: User Management with Persistent Storage
class UserManager:
    def __init__(self, storage_file="chat_users.json"):
        self.storage_file = storage_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def authenticate(self, username):
        if username not in self.users:
            self.users[username] = []
        print(f"User '{username}' logged in.")
        return username

# Module 2: Chat Processing with Keyword Pattern Matching
class ChatBot:
    def init(self):
        self.exit_commands = {"bye", "exit", "quit"}

    def get_response(self, user_input):
        user_input = user_input.lower()
        # Detect exit commands
        if any(cmd in user_input for cmd in self.exit_commands):
            return "Goodbye!"
        # Simple keyword-based responses
        if "hello" in user_input or "hi" in user_input:
            return "Hello! How can I help you today?"
        if "time" in user_input:
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
        if "help" in user_input:
            return "You can say hello, ask for time, or say 'bye' to exit."
        return "Sorry, I didn't get that. Can you try again?"

    def is_exit(self, user_input):
        user_input = user_input.lower()
        return any(cmd in user_input for cmd in self.exit_commands)

# Module 3: Logging Conversations with Persistence
class ConversationLogger:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def log(self, username, user_input, bot_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"timestamp": timestamp, "user_input": user_input, "bot_response": bot_response}
        self.user_manager.users[username].append(entry)
        self.user_manager.save_users()

    def print_log(self, username):
        print(f"\nConversation log for {username}:")
        for entry in self.user_manager.users[username]:
            print(f"[{entry['timestamp']}] You: {entry['user_input']}")
            print(f"             Bot: {entry['bot_response']}")

# Main flow tying modules together
def main():
    user_manager = UserManager()
    chatbot = ChatBot()
    logger = ConversationLogger(user_manager)

    username = input("Enter username: ").strip()
    username = user_manager.authenticate(username)

    print("\nStart chatting with the bot (type 'bye', 'exit', or 'quit' to stop):")
    while True:
        user_input = input("You: ").strip()
        response = chatbot.get_response(user_input)
        print("Bot:", response)
        logger.log(username, user_input, response)
        if chatbot.is_exit(user_input):
            break

    logger.print_log(username)
    print("Chat session ended.")

if __name__ == "__main__":
    main()