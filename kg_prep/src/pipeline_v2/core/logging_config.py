"""
Pipeline V2 Structured Logging Configuration.

Provides contextual, credential-safe structured logging with execution tracking.
Ensures zero secret leakage (API keys, authorization headers, passwords).
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any

# Regex patterns to detect and redact sensitive keys and headers
SENSITIVE_KEY_PATTERN = re.compile(
    r"(?i)(api[_-]?key|auth|bearer|secret|password|token|credential)"
)
AUTH_HEADER_PATTERN = re.compile(
    r"(?i)(authorization:\s*(bearer|basic)\s+)[^\s,]+", re.IGNORECASE
)


class CredentialSanitizingFilter(logging.Filter):
    """Logging filter that scrubs sensitive credentials from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = AUTH_HEADER_PATTERN.sub(r"\1[REDACTED]", record.msg)
            # Generic pattern for key=value or "key": "value"
            record.msg = re.sub(
                r'("?(?:api[_-]?key|password|token|secret)"?\s*[:=]\s*["\'])([^"\']+)(["\'])',
                r"\1[REDACTED]\3",
                record.msg,
                flags=re.IGNORECASE,
            )

        # Sanitize arguments if present
        if record.args:
            if isinstance(record.args, dict):
                sanitized = {}
                for k, v in record.args.items():
                    if SENSITIVE_KEY_PATTERN.search(str(k)):
                        sanitized[k] = "[REDACTED]"
                    else:
                        sanitized[k] = v
                record.args = sanitized
            elif isinstance(record.args, (list, tuple)):
                sanitized_list = []
                for item in record.args:
                    if isinstance(item, str):
                        sanitized_list.append(
                            AUTH_HEADER_PATTERN.sub(r"\1[REDACTED]", item)
                        )
                    else:
                        sanitized_list.append(item)
                record.args = tuple(sanitized_list) if isinstance(record.args, tuple) else sanitized_list

        return True


class StructuredJsonFormatter(logging.Formatter):
    """JSON formatter emitting standardized structured log entries."""

    def __init__(self, execution_id: Optional[str] = None):
        super().__init__()
        self.execution_id = execution_id or "EXEC_UNSET"

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
            "execution_id": getattr(record, "execution_id", self.execution_id),
        }

        if hasattr(record, "source_id"):
            log_entry["source_id"] = record.source_id

        if hasattr(record, "dataset_id"):
            log_entry["dataset_id"] = record.dataset_id

        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            # Scrub extra_data before writing
            safe_extra = {
                k: ("[REDACTED]" if SENSITIVE_KEY_PATTERN.search(k) else v)
                for k, v in record.extra_data.items()
            }
            log_entry["extra"] = safe_extra

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logger(
    name: str = "pipeline_v2",
    execution_id: Optional[str] = None,
    log_level: int = logging.INFO,
    log_to_file: Optional[str] = None,
    as_json: bool = False,
) -> logging.Logger:
    """
    Configures and returns a credential-safe logger for Pipeline V2.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    # Avoid duplicate handlers on re-configuration
    if logger.handlers:
        logger.handlers.clear()

    filter_sanitizer = CredentialSanitizingFilter()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.addFilter(filter_sanitizer)

    if as_json:
        console_handler.setFormatter(StructuredJsonFormatter(execution_id=execution_id))
    else:
        text_formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] [%(module)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        )
        console_handler.setFormatter(text_formatter)

    logger.addHandler(console_handler)

    # Optional File Handler
    if log_to_file:
        os.makedirs(os.path.dirname(os.path.abspath(log_to_file)), exist_ok=True)
        file_handler = logging.FileHandler(log_to_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.addFilter(filter_sanitizer)
        file_handler.setFormatter(StructuredJsonFormatter(execution_id=execution_id))
        logger.addHandler(file_handler)

    return logger
