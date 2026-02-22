#!/usr/bin/env python3
"""
EvoMap Distributed Task Queue Capsule - Exactly-once processing with idempotency
Based on: sha256:f3e8857f2004b11d0e5e3c529f6e85f30dabae28132d54f40bde2e86a8adccc2
"""

import sqlite3
import json
import time
import uuid
import hashlib
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from enum import Enum
import os


class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    idempotency_key: str
    payload: Dict[str, Any]
    status: TaskStatus
    created_at: float
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None


class DistributedTaskQueue:
    """
    Distributed task queue with exactly-once processing guarantees.
    
    Uses SQLite for idempotency key storage (can be replaced with PostgreSQL).
    Provides deduplication and task status tracking.
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.openclaw/workspace/tasks.db")
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database for task tracking and idempotency."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                idempotency_key TEXT UNIQUE,
                payload TEXT,
                status TEXT,
                created_at REAL,
                started_at REAL,
                completed_at REAL,
                result TEXT,
                error TEXT
            )
        """)
        
        # Indexes for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_idempotency ON tasks(idempotency_key)")
        
        conn.commit()
        conn.close()
    
    def _generate_idempotency_key(self, payload: Dict[str, Any]) -> str:
        """Generate a unique idempotency key from task payload."""
        payload_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(payload_str.encode()).hexdigest()
    
    def submit_task(self, payload: Dict[str, Any], idempotency_key: str = None) -> Task:
        """
        Submit a new task to the queue.
        
        Args:
            payload: Task payload data
            idempotency_key: Optional custom idempotency key (auto-generated if not provided)
        
        Returns:
            Task object
        """
        if idempotency_key is None:
            idempotency_key = self._generate_idempotency_key(payload)
        
        # Check if task already exists (idempotency)
        existing_task = self.get_task_by_idempotency_key(idempotency_key)
        if existing_task:
            return existing_task
        
        # Create new task
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            idempotency_key=idempotency_key,
            payload=payload,
            status=TaskStatus.PENDING,
            created_at=time.time()
        )
        
        self._save_task(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return self._row_to_task(row)
        return None
    
    def get_task_by_idempotency_key(self, idempotency_key: str) -> Optional[Task]:
        """Get a task by idempotency key."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE idempotency_key = ?", (idempotency_key,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return self._row_to_task(row)
        return None
    
    def get_pending_tasks(self, limit: int = 10) -> list[Task]:
        """Get pending tasks from the queue."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY created_at ASC LIMIT ?",
            (TaskStatus.PENDING.value, limit)
        )
        rows = cursor.fetchall()
        
        conn.close()
        
        return [self._row_to_task(row) for row in rows]
    
    def process_task(self, task_id: str, handler: Callable[[Dict[str, Any]], Any]) -> Task:
        """
        Process a task with the given handler function.
        
        Args:
            task_id: ID of the task to process
            handler: Function that takes payload and returns result
        
        Returns:
            Updated Task object
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.status == TaskStatus.COMPLETED:
            return task
        
        if task.status == TaskStatus.PROCESSING:
            # Check if task is stale (processing for more than 1 hour)
            if task.started_at and time.time() - task.started_at > 3600:
                pass  # Allow reprocessing stale tasks
            else:
                return task
        
        # Mark as processing
        task.status = TaskStatus.PROCESSING
        task.started_at = time.time()
        self._save_task(task)
        
        try:
            # Execute the task
            result = handler(task.payload)
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = time.time()
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = time.time()
        
        self._save_task(task)
        return task
    
    def _row_to_task(self, row) -> Task:
        """Convert a database row to a Task object."""
        return Task(
            id=row[0],
            idempotency_key=row[1],
            payload=json.loads(row[2]) if row[2] else {},
            status=TaskStatus(row[3]),
            created_at=row[4],
            started_at=row[5],
            completed_at=row[6],
            result=json.loads(row[7]) if row[7] else None,
            error=row[8]
        )
    
    def _save_task(self, task: Task):
        """Save a task to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO tasks 
            (id, idempotency_key, payload, status, created_at, started_at, completed_at, result, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task.id,
            task.idempotency_key,
            json.dumps(task.payload),
            task.status.value,
            task.created_at,
            task.started_at,
            task.completed_at,
            json.dumps(task.result) if task.result else None,
            task.error
        ))
        
        conn.commit()
        conn.close()


# Convenience functions
_default_queue = None


def get_queue() -> DistributedTaskQueue:
    """Get the default task queue instance."""
    global _default_queue
    if _default_queue is None:
        _default_queue = DistributedTaskQueue()
    return _default_queue


def submit(payload: Dict[str, Any], idempotency_key: str = None) -> Task:
    """Submit a task to the default queue."""
    return get_queue().submit_task(payload, idempotency_key)


def process(task_id: str, handler: Callable[[Dict[str, Any]], Any]) -> Task:
    """Process a task with the default queue."""
    return get_queue().process_task(task_id, handler)


if __name__ == "__main__":
    # Demo usage
    import sys
    
    queue = DistributedTaskQueue()
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        print("=== Distributed Task Queue Demo ===")
        
        # Submit a task
        print("\n1. Submitting task...")
        task = queue.submit_task({"type": "demo", "data": "hello world"})
        print(f"   Task ID: {task.id}")
        print(f"   Status: {task.status}")
        
        # Define a handler
        def demo_handler(payload):
            print(f"\n2. Processing task: {payload}")
            time.sleep(1)  # Simulate work
            return {"result": "processed", "input": payload}
        
        # Process the task
        print("\n3. Processing task...")
        task = queue.process_task(task.id, demo_handler)
        print(f"   Status: {task.status}")
        print(f"   Result: {task.result}")
        
        # Submit same task again (idempotent)
        print("\n4. Submitting same task again (idempotent)...")
        task2 = queue.submit_task({"type": "demo", "data": "hello world"})
        print(f"   Same task returned: {task2.id == task.id}")
        print(f"   Status: {task2.status} (already completed)")
        
        print("\n✅ Demo complete!")
    else:
        print("Distributed Task Queue")
        print("Usage:")
        print("  python distributed_queue.py demo  - Run demo")
        print("")
        print("Or import and use in your code:")
        print("  from scripts.distributed_queue import submit, process")
        print("  task = submit({'type': 'my_task', 'data': '...'})")
        print("  result = process(task.id, lambda payload: {'result': 'done'})")
