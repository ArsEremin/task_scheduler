from enum import StrEnum


class TaskStatus(StrEnum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class TaskPriority(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
