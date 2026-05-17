"""
数据持久层
使用SQLite存储用户会话和记录
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from ..数据模型.schemas import ThinkingSession, User, ReflectionNote, create_session_id


class DataStore:
    """数据存储管理器"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent.parent / "数据" / "用户数据" / "sessions.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()

            # 用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    nickname TEXT,
                    languages TEXT,
                    contribute_data INTEGER DEFAULT 0,
                    created_at TEXT,
                    metadata TEXT
                )
            """)

            # 思考会话表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS thinking_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    task_id TEXT,
                    language TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    answer TEXT,
                    thinking_process TEXT,
                    confidence REAL,
                    difficulty_rating REAL,
                    is_correct INTEGER,
                    metadata TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            # 反思记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reflection_notes (
                    note_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    session_ids TEXT,
                    languages_compared TEXT,
                    question TEXT,
                    observations TEXT,
                    surprising_aspects TEXT,
                    insights TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)

            conn.commit()

    # ===== 用户管理 =====

    def create_user(self, user_id: str, nickname: str, languages: Dict[str, str]) -> User:
        """创建新用户"""
        user = User(
            user_id=user_id,
            nickname=nickname,
            languages=languages,
            created_at=datetime.now(),
            contribute_data=False,
            metadata={}
        )

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, nickname, languages, contribute_data, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user.user_id,
                user.nickname,
                json.dumps(user.languages, ensure_ascii=False),
                1 if user.contribute_data else 0,
                user.created_at.isoformat(),
                json.dumps(user.metadata, ensure_ascii=False)
            ))
            conn.commit()

        return user

    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户信息"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row:
                return User(
                    user_id=row[0],
                    nickname=row[1],
                    languages=json.loads(row[2]),
                    contribute_data=bool(row[3]),
                    created_at=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]) if row[5] else {}
                )
        return None

    def update_user_languages(self, user_id: str, languages: Dict[str, str]):
        """更新用户语言能力"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET languages = ? WHERE user_id = ?
            """, (json.dumps(languages, ensure_ascii=False), user_id))
            conn.commit()

    # ===== 思考会话管理 =====

    def start_session(self, user_id: str, task_id: str, language: str) -> ThinkingSession:
        """开始新的思考会话"""
        session = ThinkingSession(
            session_id=create_session_id(),
            user_id=user_id,
            task_id=task_id,
            language=language,
            start_time=datetime.now(),
            end_time=None,
            answer=None,
            thinking_process=None,
            confidence=None,
            difficulty_rating=None,
            is_correct=None,
            metadata={}
        )

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO thinking_sessions 
                (session_id, user_id, task_id, language, start_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.user_id,
                session.task_id,
                session.language,
                session.start_time.isoformat(),
                json.dumps(session.metadata, ensure_ascii=False)
            ))
            conn.commit()

        return session

    def complete_session(self, session_id: str, answer: str, thinking_process: str = None,
                        confidence: float = None, difficulty_rating: float = None,
                        is_correct: bool = None):
        """完成思考会话"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE thinking_sessions 
                SET end_time = ?, answer = ?, thinking_process = ?, 
                    confidence = ?, difficulty_rating = ?, is_correct = ?
                WHERE session_id = ?
            """, (
                datetime.now().isoformat(),
                answer,
                thinking_process,
                confidence,
                difficulty_rating,
                1 if is_correct else 0 if is_correct is not None else None,
                session_id
            ))
            conn.commit()

    def get_user_sessions(self, user_id: str, limit: int = 100) -> List[ThinkingSession]:
        """获取用户的所有思考会话"""
        sessions = []
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM thinking_sessions 
                WHERE user_id = ? ORDER BY start_time DESC LIMIT ?
            """, (user_id, limit))

            for row in cursor.fetchall():
                sessions.append(ThinkingSession(
                    session_id=row[0],
                    user_id=row[1],
                    task_id=row[2],
                    language=row[3],
                    start_time=datetime.fromisoformat(row[4]),
                    end_time=datetime.fromisoformat(row[5]) if row[5] else None,
                    answer=row[6],
                    thinking_process=row[7],
                    confidence=row[8],
                    difficulty_rating=row[9],
                    is_correct=bool(row[10]) if row[10] is not None else None,
                    metadata=json.loads(row[11]) if row[11] else {}
                ))

        return sessions

    # ===== 反思记录管理 =====

    def save_reflection(self, user_id: str, session_ids: List[str],
                       languages_compared: List[str], question: str,
                       observations: str, surprising_aspects: str = None,
                       insights: str = None) -> ReflectionNote:
        """保存反思记录"""
        import uuid
        note = ReflectionNote(
            note_id=f"ref_{uuid.uuid4().hex[:12]}",
            user_id=user_id,
            session_ids=session_ids,
            languages_compared=languages_compared,
            question=question,
            observations=observations,
            surprising_aspects=surprising_aspects,
            insights=insights,
            created_at=datetime.now()
        )

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reflection_notes 
                (note_id, user_id, session_ids, languages_compared, question,
                 observations, surprising_aspects, insights, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note.note_id,
                note.user_id,
                json.dumps(note.session_ids, ensure_ascii=False),
                json.dumps(note.languages_compared, ensure_ascii=False),
                note.question,
                note.observations,
                note.surprising_aspects,
                note.insights,
                note.created_at.isoformat()
            ))
            conn.commit()

        return note

    def get_user_reflections(self, user_id: str, limit: int = 50) -> List[ReflectionNote]:
        """获取用户的反思记录"""
        notes = []
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reflection_notes 
                WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
            """, (user_id, limit))

            for row in cursor.fetchall():
                notes.append(ReflectionNote(
                    note_id=row[0],
                    user_id=row[1],
                    session_ids=json.loads(row[2]),
                    languages_compared=json.loads(row[3]),
                    question=row[4],
                    observations=row[5],
                    surprising_aspects=row[6],
                    insights=row[7],
                    created_at=datetime.fromisoformat(row[8])
                ))

        return notes

    # ===== 统计数据 =====

    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """获取用户统计数据"""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()

            # 会话统计
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_sessions,
                    COUNT(DISTINCT task_id) as tasks_completed,
                    COUNT(DISTINCT language) as languages_used,
                    AVG(confidence) as avg_confidence,
                    AVG(difficulty_rating) as avg_difficulty
                FROM thinking_sessions WHERE user_id = ?
            """, (user_id,))
            row = cursor.fetchone()

            # 按语言统计
            cursor.execute("""
                SELECT language, COUNT(*) 
                FROM thinking_sessions 
                WHERE user_id = ? 
                GROUP BY language
            """, (user_id,))
            by_language = dict(cursor.fetchall())

            # 按任务类型统计（需要关联任务数据，这里简化）
            cursor.execute("""
                SELECT task_id, COUNT(*) 
                FROM thinking_sessions 
                WHERE user_id = ? 
                GROUP BY task_id
            """, (user_id,))
            by_task = dict(cursor.fetchall())

            # 反思数量
            cursor.execute("SELECT COUNT(*) FROM reflection_notes WHERE user_id = ?", (user_id,))
            reflections_count = cursor.fetchone()[0]

        return {
            "total_sessions": row[0] or 0,
            "tasks_completed": row[1] or 0,
            "languages_used": row[2] or 0,
            "avg_confidence": round(row[3] or 0, 1),
            "avg_difficulty": round(row[4] or 0, 1),
            "by_language": by_language,
            "by_task": by_task,
            "reflections_count": reflections_count
        }
