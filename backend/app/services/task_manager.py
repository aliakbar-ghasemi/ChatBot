import asyncio
from typing import Dict, Any

class TaskManager:
    """Manages background tasks and allows clean cancellation."""
    def __init__(self):
        self.tasks = {}

    def add_task(self, conversation_id: str, task: asyncio.Task, queue: asyncio.Queue):
        """Stores the task and queue associated with a conversation."""
        self.tasks[conversation_id] = (task, queue)

    def cancel_task(self, conversation_id: str):
        """Cancels the task if it exists."""
        if conversation_id in self.tasks:
            task, queue = self.tasks.pop(conversation_id)
            task.cancel()
            return True
        return False

    def has_task(self, conversation_id: str):
        """Checks if a task exists for a conversation."""
        return conversation_id in self.tasks

task_manager = TaskManager()
