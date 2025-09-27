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
    
    # Clear existing handlers to prevent duplicate logging
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Setup state change logger - this is a separate logger that goes to its own file
    state_logger = logging.getLogger("agent_states")
    state_logger.handlers.clear()
    state_logger.setLevel(getattr(logging, log_level))
    state_file_handler = logging.FileHandler(f"{log_dir}/state_changes.log")
    state_file_formatter = logging.Formatter('%(asctime)s - %(message)s')
    state_file_handler.setFormatter(state_file_formatter)
    state_logger.addHandler(state_file_handler)
    state_logger.propagate = False  # Don't propagate to root logger
    
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
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Force reconfiguration even if basicConfig was called before
    )


def get_logger(name: str):
    """Get a logger
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger - either a structlog logger or a standard logger for special cases
    """
    # For state logging, return the standard logger we configured separately
    if name == "agent_states":
        return logging.getLogger(name)
    
    # For all other loggers, return a structlog logger
    return structlog.get_logger(name)