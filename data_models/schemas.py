"""
数据结构定义
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class TaskType(Enum):
    """任务类型枚举"""
    LOGICAL_REASONING = "logical_reasoning"      # 逻辑推理
    PROBLEM_SOLVING = "problem_solving"          # 问题解决
    MORAL_JUDGMENT = "moral_judgment"            # 道德判断
    CREATIVE_THINKING = "creative_thinking"      # 创造性思维
    TIME_PERCEPTION = "time_perception"          # 时间认知
    SPATIAL_COGNITION = "spatial_cognition"      # 空间认知
    DECISION_MAKING = "decision_making"          # 决策判断


class Difficulty(Enum):
    """难度级别"""
    BEGINNER = "beginner"      # 入门
    INTERMEDIATE = "intermediate"  # 进阶
    ADVANCED = "advanced"      # 挑战


@dataclass
class TaskContent:
    """单个语言版本的任务内容"""
    language: str
    title: str
    description: str
    question: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    hint: Optional[str] = None


@dataclass
class Task:
    """推理任务"""
    task_id: str
    task_type: TaskType
    difficulty: Difficulty
    versions: Dict[str, TaskContent]  # key: 语言代码, value: 任务内容
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    reference: Optional[str] = None  # 参考文献或经典实验来源


@dataclass
class ThinkingSession:
    """单次思考会话"""
    session_id: str
    user_id: str
    task_id: str
    language: str
    start_time: datetime
    end_time: Optional[datetime] = None
    answer: Optional[str] = None
    thinking_process: Optional[str] = None  # 思考过程描述
    confidence: Optional[float] = None  # 自信度 0-100
    difficulty_rating: Optional[float] = None  # 感知难度 0-100
    is_correct: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class User:
    """用户信息"""
    user_id: str
    nickname: str
    languages: Dict[str, str]  # 语言: 熟练度 (native, advanced, intermediate, beginner)
    created_at: datetime = field(default_factory=datetime.now)
    contribute_data: bool = False  # 是否同意贡献匿名数据
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReflectionNote:
    """反思记录"""
    note_id: str
    user_id: str
    session_ids: List[str]  # 关联的思考会话（可能多个，用于对比）
    languages_compared: List[str]
    question: str
    observations: str  # 观察到的差异
    surprising_aspects: Optional[str] = None
    insights: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class LanguageFeature:
    """语言认知特征"""
    language_code: str
    language_name: str
    family: str  # 语系
    features: Dict[str, Any]  # 认知特征描述
    # 例如：时态系统、语法性、敬语系统、量词系统等


# 辅助函数
def create_task_id(task_type: TaskType, index: int) -> str:
    """生成任务ID"""
    return f"{task_type.value}_{index:04d}"


def create_session_id() -> str:
    """生成会话ID"""
    return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
