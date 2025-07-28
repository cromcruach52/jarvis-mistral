from langchain.memory import ConversationBufferWindowMemory
from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import json
import os
from datetime import datetime


class JarvisMemory:
    def __init__(self, model_name="mistral:latest"):
        # Initialize Ollama chat model with optimized settings
        self.llm = ChatOllama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0.7,
            num_predict=512,  # Limit response length for speed
            num_ctx=2048,  # Smaller context window for speed
        )

        # Smaller memory window for faster processing
        self.memory = ConversationBufferWindowMemory(
            k=5,  # Keep only last 5 exchanges for speed
            return_messages=True,
        )

        # Simplified prompt for faster processing
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""Previous context: {history}

User: {input}
Jarvis:""",
        )

        # Create conversation chain
        self.conversation = ConversationChain(
            llm=self.llm, memory=self.memory, prompt=self.prompt, verbose=False
        )

        # File to persist memory (optional)
        self.memory_file = "jarvis_memory.json"
        self.load_memory()

    def chat(self, user_input: str) -> str:
        """Chat with memory context"""
        try:
            response = self.conversation.predict(input=user_input)
            self.save_memory()  # Save after each interaction
            return response
        except Exception as e:
            print(f"Memory chat error: {e}")
            return "I'm sorry, I'm having trouble processing that request right now."

    def save_memory(self):
        """Save conversation memory to file"""
        try:
            # Get conversation history
            messages = self.memory.chat_memory.messages
            memory_data = {
                "timestamp": datetime.now().isoformat(),
                "messages": [
                    {"type": type(msg).__name__, "content": msg.content}
                    for msg in messages
                ],
            }

            with open(self.memory_file, "w") as f:
                json.dump(memory_data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def load_memory(self):
        """Load conversation memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    memory_data = json.load(f)

                # Restore messages to memory
                from langchain.schema import HumanMessage, AIMessage

                for msg_data in memory_data.get("messages", []):
                    if msg_data["type"] == "HumanMessage":
                        self.memory.chat_memory.add_user_message(msg_data["content"])
                    elif msg_data["type"] == "AIMessage":
                        self.memory.chat_memory.add_ai_message(msg_data["content"])

                print(f"📚 Loaded conversation history from {self.memory_file}")
        except Exception as e:
            print(f"Error loading memory: {e}")

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        if os.path.exists(self.memory_file):
            os.remove(self.memory_file)
        print("🧹 Memory cleared")

    def get_memory_summary(self):
        """Get a summary of current memory"""
        messages = self.memory.chat_memory.messages
        return f"Memory contains {len(messages)} messages"


# Global memory instance
jarvis_memory = JarvisMemory()


def chat_with_memory(user_input: str) -> str:
    return jarvis_memory.chat(user_input)


def clear_conversation_memory():
    jarvis_memory.clear_memory()


def get_memory_info():
    return jarvis_memory.get_memory_summary()
