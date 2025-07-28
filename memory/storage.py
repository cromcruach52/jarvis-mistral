import json
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class ConversationMemory:
    def __init__(self, db_path="jarvis_memory.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_input TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                session_id TEXT
            )
        """)

        # Create context table for long-term memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def save_conversation(
        self, user_input: str, ai_response: str, session_id: str = None
    ):
        """Save a conversation exchange"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT INTO conversations (timestamp, user_input, ai_response, session_id)
            VALUES (?, ?, ?, ?)
        """,
            (timestamp, user_input, ai_response, session_id),
        )

        conn.commit()
        conn.close()

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations for context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, user_input, ai_response 
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT ?
        """,
            (limit,),
        )

        results = cursor.fetchall()
        conn.close()

        conversations = []
        for row in results:
            conversations.append(
                {"timestamp": row[0], "user_input": row[1], "ai_response": row[2]}
            )

        return list(reversed(conversations))  # Return in chronological order

    def save_context(self, key: str, value: str):
        """Save long-term context information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute(
            """
            INSERT OR REPLACE INTO context (key, value, updated_at)
            VALUES (?, ?, ?)
        """,
            (key, value, timestamp),
        )

        conn.commit()
        conn.close()

    def get_context(self, key: str) -> Optional[str]:
        """Get context information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM context WHERE key = ?", (key,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def build_context_prompt(self, current_input: str) -> str:
        """Build a context-aware prompt"""
        recent_conversations = self.get_recent_conversations(5)

        context_prompt = "Previous conversation context:\n"
        for conv in recent_conversations:
            context_prompt += f"User: {conv['user_input']}\n"
            context_prompt += f"Assistant: {conv['ai_response']}\n\n"

        context_prompt += f"Current user input: {current_input}\n"
        context_prompt += "Please respond considering the conversation history above."

        return context_prompt


# Global memory instance
memory = ConversationMemory()


def save_conversation(user_input: str, ai_response: str):
    memory.save_conversation(user_input, ai_response)


def get_context_prompt(user_input: str) -> str:
    return memory.build_context_prompt(user_input)
