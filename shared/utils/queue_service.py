import json
from ..constant import RedisEnum
from ..redis_client import redis_client

class QueueService:
    def __init__(self):
        self.client = redis_client
    
    def push_job(self, file_id: str, user_id: str, file_name: str, mime_type: str, storage_path: str):
        job = {
            "file_id": file_id,
            "user_id": user_id,
            "file_name": file_name,
            "mime_type": mime_type,
            "storage_path": storage_path,
        }
        self.client.lpush(RedisEnum.QUEUE_NAME.value, json.dumps(job))
    
    def consume_job(self) -> dict|None:
        result = self.client.brpop(RedisEnum.QUEUE_NAME.value, timeout=5)
        if result:
            _, job_data = result
            return json.loads(job_data)
        return None
    
    def publish_status(self, user_id: str, file_id: str, status: str, error: str|None = None):
        event = {
            "file_id": file_id,
            "status": status
        }

        if error:
            event["error"] = error
        
        self.client.publish(f"user:{user_id}:files", json.dumps(event))

queue_service = QueueService()