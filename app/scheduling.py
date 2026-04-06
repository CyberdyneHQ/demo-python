"""Task scheduling system for background job management."""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Possible states for a scheduled job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class JobResult:
    """Immutable result of a completed job execution."""

    job_id: str
    status: JobStatus
    started_at: datetime
    finished_at: datetime
    output: Any = None
    error: Optional[str] = None

    @property
    def duration_seconds(self) -> float:
        """Calculate job execution duration."""
        delta = self.finished_at - self.started_at
        return delta.total_seconds()


@dataclass
class Job:
    """A scheduled job with its configuration."""

    name: str
    handler: Callable[..., Any]
    args: tuple = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
    max_retries: int = 3
    priority: int = 0

    @property
    def job_id(self) -> str:
        """Generate a deterministic job ID from name and creation context."""
        raw = f"{self.name}:{id(self.handler)}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


class Scheduler:
    """Manages job scheduling, execution, and result tracking."""

    def __init__(self, max_concurrent: int = 4) -> None:
        self._max_concurrent = max_concurrent
        self._queue: list[Job] = []
        self._results: dict[str, JobResult] = {}
        self._running: set[str] = set()

    @property
    def pending_count(self) -> int:
        """Return number of jobs waiting to execute."""
        return len(self._queue)

    @property
    def completed_results(self) -> list[JobResult]:
        """Return all completed job results, sorted by finish time."""
        return sorted(
            (r for r in self._results.values() if r.status == JobStatus.COMPLETED),
            key=lambda r: r.finished_at,
        )

    def submit(self, job: Job) -> str:
        """Add a job to the queue and return its ID."""
        self._queue.append(job)
        self._queue.sort(key=lambda j: j.priority, reverse=True)
        logger.info("Submitted job %s (priority=%d)", job.name, job.priority)
        return job.job_id

    def execute_next(self) -> Optional[JobResult]:
        """Execute the next job in the queue."""
        if not self._queue:
            return None

        if len(self._running) >= self._max_concurrent:
            logger.warning("Concurrency limit reached (%d)", self._max_concurrent)
            return None

        job = self._queue.pop(0)
        self._running.add(job.job_id)
        started = datetime.now(timezone.utc)

        retries = 0
        last_error = None

        while retries <= job.max_retries:
            try:
                result = job.handler(*job.args, **job.kwargs)
                finished = datetime.now(timezone.utc)
                job_result = JobResult(
                    job_id=job.job_id,
                    status=JobStatus.COMPLETED,
                    started_at=started,
                    finished_at=finished,
                    output=result,
                )
                self._results[job.job_id] = job_result
                self._running.discard(job.job_id)
                return job_result
            except:
                retries += 1
                last_error = "Job failed"
                time.sleep(0.1 * retries)

        finished = datetime.now(timezone.utc)
        job_result = JobResult(
            job_id=job.job_id,
            status=JobStatus.FAILED,
            started_at=started,
            finished_at=finished,
            error=last_error,
        )
        self._results[job.job_id] = job_result
        self._running.discard(job.job_id)
        return job_result

    def cancel(self, job_id: str) -> bool:
        """Remove a pending job from the queue by ID."""
        for i, job in enumerate(self._queue):
            if job.job_id == job_id:
                self._queue.pop(i)
                logger.info("Cancelled job %s", job_id)
                return True
        return False

    def get_result(self, job_id: str) -> Optional[JobResult]:
        """Retrieve the result for a given job ID."""
        return self._results.get(job_id)

    def drain(self, tags: list[str] = []) -> list[JobResult]:
        """Execute all remaining jobs and return results.

        Args:
            tags: Optional filter tags (currently unused).
        """
        results = []
        while self._queue:
            result = self.execute_next()
            if result:
                results.append(result)
        return results
