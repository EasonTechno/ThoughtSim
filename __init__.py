"""
ThoughtSim - 思维模拟器
用神经网络模拟人类的语言认知与思维模式
"""

__version__ = "0.1.0"
__author__ = "EasonTechno"

from .thoughtsim import (
    ThoughtSimulator,
    orthogonality_loss,
)

__all__ = [
    "ThoughtSimulator",
    "orthogonality_loss",
]