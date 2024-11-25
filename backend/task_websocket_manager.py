from typing import DefaultDict, Set
from collections import defaultdict
from asyncio import Event


class TaskWebsocketManager:
    def __init__(self):
        self.connections: DefaultDict[int, Set[Event]] = defaultdict(set)
        
    def connect(self, user_id: int):
        event = Event()
        self.connections[user_id].add(event)
        return event
        
    def disconnect(self, user_id: int, event: Event):
        self.connections[user_id].remove(event)
        
    def notify_conections(self, user_id: int):
        for event in self.connections[user_id]:
            event.set()