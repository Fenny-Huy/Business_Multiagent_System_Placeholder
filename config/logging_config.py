# config/logging_config.py
import logging
import structlog
from pathlib import Path
import sys
from typing import Any, Dict


def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    enable_file_logging: bool = True,
    enable_console_logging: bool = True
) -> None:
    """Setup structured logging for the multi-agent system
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files
        enable_file_logging: Whether to log to files
        enable_console_logging: Whether to log to console
    """
    # Create logs directory
    Path(log_dir).mkdir(exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    handlers = []
    
    if enable_console_logging:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        handlers.append(console_handler)
    
    if enable_file_logging:
        file_handler = logging.FileHandler(f"{log_dir}/multiagent.log")
        file_handler.setLevel(getattr(logging, log_level))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        handlers=handlers,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger
    
    Args:
        name: Logger name
        
    Returns:
        Configured structured logger
    """
    return structlog.get_logger(name)