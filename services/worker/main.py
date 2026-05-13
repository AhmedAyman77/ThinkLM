import json
from shared import queue_service, files_repository
from controllers.processing_controller import ProcessingController

processing_controller = ProcessingController()

print("Worker started. Waiting for jobs...")

while True:
    result = queue_service.consume_job()

    if result:
        _, job_data = result
        job = json.loads(job_data)

        file_id = job["file_id"]
        user_id = job["user_id"]

        print(f"Processing job: {file_id}")

        try:
            processing_controller.process(job)
            queue_service.publish_status(user_id, file_id, "ready")
            print(f"Job completed: {file_id}")

        except Exception as e:
            files_repository.update_file_status(file_id, "failed")
            queue_service.publish_status(user_id, file_id, "failed", str(e))
            print(f"Job failed: {file_id} — {e}")
