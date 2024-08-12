"""
Blackboard API Client

Powered by `tiny-api-client`
"""

import logging
from .api import BlackboardSession

__all__ = ['BlackboardSession']

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
