"""
任务加载器
加载和管理推理任务
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from ..数据模型.schemas import Task, TaskContent, TaskType, Difficulty, create_task_id


class TaskLoader:
    """任务加载器"""

    def __init__(self, tasks_dir: str = None):
        if tasks_dir is None:
            tasks_dir = Path(__file__).parent.parent.parent / "数据" / "任务数据"

        self.tasks_dir = Path(tasks_dir)
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self._tasks_cache = {}

    def load_all_tasks(self) -> Dict[str, Task]:
        """加载所有任务"""
        if self._tasks_cache:
            return self._tasks_cache

        tasks = {}
        for task_file in self.tasks_dir.glob("**/*.json"):
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    task = self._dict_to_task(data)
                    tasks[task.task_id] = task
            except Exception as e:
                print(f"加载任务文件失败 {task_file}: {e}")

        self._tasks_cache = tasks
        return tasks

    def _dict_to_task(self, data: Dict) -> Task:
        """将字典转换为Task对象"""
        versions = {}
        for lang, content_data in data.get("versions", {}).items():
            versions[lang] = TaskContent(
                language=lang,
                title=content_data.get("title", ""),
                description=content_data.get("description", ""),
                question=content_data.get("question", ""),
                options=content_data.get("options"),
                correct_answer=content_data.get("correct_answer"),
                hint=content_data.get("hint")
            )

        return Task(
            task_id=data.get("task_id", ""),
            task_type=TaskType(data.get("task_type")),
            difficulty=Difficulty(data.get("difficulty")),
            versions=versions,
            tags=data.get("tags", []),
            reference=data.get("reference")
        )

    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        """按类型获取任务"""
        tasks = self.load_all_tasks()
        return [t for t in tasks.values() if t.task_type == task_type]

    def get_tasks_by_language(self, language: str) -> List[Task]:
        """获取有某语言版本的任务"""
        tasks = self.load_all_tasks()
        return [t for t in tasks.values() if language in t.versions]

    def get_tasks_by_difficulty(self, difficulty: Difficulty) -> List[Task]:
        """按难度获取任务"""
        tasks = self.load_all_tasks()
        return [t for t in tasks.values() if t.difficulty == difficulty]

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取单个任务"""
        tasks = self.load_all_tasks()
        return tasks.get(task_id)

    def save_task(self, task: Task):
        """保存任务到文件"""
        task_data = self._task_to_dict(task)
        task_file = self.tasks_dir / f"{task.task_id}.json"

        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)

        # 清除缓存
        self._tasks_cache = {}

    def _task_to_dict(self, task: Task) -> Dict:
        """将Task对象转换为字典"""
        versions = {}
        for lang, content in task.versions.items():
            versions[lang] = {
                "title": content.title,
                "description": content.description,
                "question": content.question,
                "options": content.options,
                "correct_answer": content.correct_answer,
                "hint": content.hint
            }

        return {
            "task_id": task.task_id,
            "task_type": task.task_type.value,
            "difficulty": task.difficulty.value,
            "versions": versions,
            "tags": task.tags,
            "reference": task.reference
        }

    def get_task_statistics(self) -> Dict:
        """获取任务统计信息"""
        tasks = self.load_all_tasks()

        stats = {
            "total": len(tasks),
            "by_type": {},
            "by_difficulty": {},
            "languages": set(),
        }

        for task in tasks.values():
            # 按类型统计
            task_type = task.task_type.value
            stats["by_type"][task_type] = stats["by_type"].get(task_type, 0) + 1

            # 按难度统计
            difficulty = task.difficulty.value
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1

            # 收集语言
            stats["languages"].update(task.versions.keys())

        stats["languages"] = sorted(list(stats["languages"]))
        return stats
