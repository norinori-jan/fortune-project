from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_audit import FortuneRuntimeAuditService
from fortune_core.services.runtime_jobs import FortuneRuntimeJobService
from fortune_core.services.runtime_pipeline import FortuneRuntimePipeline
class FortuneRuntimeGateway:
    def __init__(
        self,
        pipeline: FortuneRuntimePipeline | None = None,
        jobs: FortuneRuntimeJobService | None = None,
        audit: FortuneRuntimeAuditService | None = None,
    ) -> None:
        self.pipeline = pipeline or FortuneRuntimePipeline()
        self.jobs = jobs or FortuneRuntimeJobService(self.pipeline)
        self.audit = audit or FortuneRuntimeAuditService()
    def execute(
        self,
        request: HubRuntimeRequest,
    ) -> dict[str, Any]:
        try:
            result = self.pipeline.execute_dict(request)
            request_id = str(result.get("request_id", ""))
            self.audit.record(
                request_id=request_id,
                event_type="runtime.execute",
                operation=request.operation,
                user_key=request.user_key,
                success=True,
                details={
                    "theme": request.theme,
                    "cached": result.get("cached", False),
                },
            )
            return result
        except Exception as exc:
            self.audit.record(
                request_id="",
                event_type="runtime.execute",
                operation=request.operation,
                user_key=request.user_key,
                success=False,
                details={"error": str(exc)},
            )
            raise
    def submit(
        self,
        request: HubRuntimeRequest,
    ) -> dict[str, Any]:
        job = self.jobs.submit(request)
        self.audit.record(
            request_id=job.job_id,
            event_type="runtime.job",
            operation=request.operation,
            user_key=request.user_key,
            success=job.status == "completed",
            details={"status": job.status},
        )
        return job.to_dict()
