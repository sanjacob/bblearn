"""
Blackboard API Client

Powered by `tiny-api-client`
"""

import logging
from .api import BlackboardSession

__all__ = ['BlackboardSession']

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())
