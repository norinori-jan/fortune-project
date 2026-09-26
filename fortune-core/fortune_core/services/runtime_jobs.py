from __future__ import annotations
import hashlib
import json
from threading import RLock
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.models.runtime_job import FortuneRuntimeJob
from fortune_core.services.runtime_pipeline import FortuneRuntimePipeline
class FortuneRuntimeJobService:
    def __init__(
        self,
        pipeline: FortuneRuntimePipeline | None = None,
        max_jobs: int = 500,
    ) -> None:
        self.pipeline = pipeline or FortuneRuntimePipeline()
        self.max_jobs = max(1, max_jobs)
        self._jobs: dict[str, FortuneRuntimeJob] = {}
        self._lock = RLock()
    def submit(self, request: HubRuntimeRequest) -> FortuneRuntimeJob:
        job_id = self._job_id(request)
        job = FortuneRuntimeJob(
            job_id=job_id,
            operation=request.operation,
            user_key=request.user_key,
            theme=request.theme,
            question=request.question,
        )
        with self._lock:
            self._jobs[job_id] = job
            self._trim()
        return self.run(job_id, request)
    def run(
        self,
        job_id: str,
        request: HubRuntimeRequest,
    ) -> FortuneRuntimeJob:
        with self._lock:
            self._jobs[job_id] = FortuneRuntimeJob(
                job_id=job_id,
                operation=request.operation,
                user_key=request.user_key,
                theme=request.theme,
                question=request.question,
                status="running",
            )
        try:
            result = self.pipeline.execute_dict(request)
            job = FortuneRuntimeJob(
                job_id=job_id,
                operation=request.operation,
                user_key=request.user_key,
                theme=request.theme,
                question=request.question,
                status="completed",
                result=result,
            )
        except Exception as exc:
            job = FortuneRuntimeJob(
                job_id=job_id,
                operation=request.operation,
                user_key=request.user_key,
                theme=request.theme,
                question=request.question,
                status="failed",
                error=str(exc),
            )
        with self._lock:
            self._jobs[job_id] = job
            self._trim()
        return job
    def get(self, job_id: str) -> FortuneRuntimeJob | None:
        with self._lock:
            return self._jobs.get(job_id)
    def list(
        self,
        user_key: str | None = None,
    ) -> list[FortuneRuntimeJob]:
        with self._lock:
            jobs = list(self._jobs.values())
        if user_key is not None:
            jobs = [
                job for job in jobs
                if job.user_key == user_key
            ]
        return jobs
    def _trim(self) -> None:
        if len(self._jobs) <= self.max_jobs:
            return
        for key in list(self._jobs)[: len(self._jobs) - self.max_jobs]:
            del self._jobs[key]
    @staticmethod
    def _job_id(request: HubRuntimeRequest) -> str:
        payload: dict[str, Any] = {
            "user_key": request.user_key,
            "question": request.question,
            "theme": request.theme,
            "operation": request.operation,
        }
        return hashlib.sha256(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:24]