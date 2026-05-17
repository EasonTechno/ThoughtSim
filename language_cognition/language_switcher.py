"""
语言切换引导器
帮助用户在不同语言间平滑切换思考模式
"""
import time
from typing import List, Dict
from .language_features import get_language_feature, get_immersion_text, get_thinking_hints


class LanguageSwitcher:
    """语言切换引导器"""

    def __init__(self):
        self.current_language = None

    def get_switch_steps(self, target_language: str) -> List[Dict]:
        """
        获取语言切换的引导步骤

        Args:
            target_language: 目标语言代码

        Returns:
            引导步骤列表
        """
        steps = [
            {
                "step": 1,
                "title": "准备开始",
                "instruction": "找一个安静的环境，深呼吸三次，让大脑准备切换语言模式。",
                "duration": 30,  # 建议时长（秒）
            },
            {
                "step": 2,
                "title": "语言沉浸",
                "instruction": "阅读下面这段文字，让自己沉浸在目标语言的氛围中。",
                "content": get_immersion_text(target_language),
                "duration": 60,
            },
            {
                "step": 3,
                "title": "默念练习",
                "instruction": "在心中用目标语言默念几个简单的句子，描述你现在看到的周围环境。\n\n"
                               "例如：\n"
                               "- 我现在坐在椅子上\n"
                               "- 窗外有阳光\n"
                               "- 我的电脑是银色的",
                "duration": 60,
            },
            {
                "step": 4,
                "title": "认知特征提醒",
                "instruction": "了解这种语言可能影响你思考方式的特征：\n\n" +
                               "\n".join([f"• {hint}" for hint in get_thinking_hints(target_language)]),
                "duration": 45,
            },
            {
                "step": 5,
                "title": "准备完成",
                "instruction": "现在你已经准备好了！记住：\n"
                               "❌ 不要在心里翻译\n"
                               "✅ 直接用目标语言思考\n"
                               "✅ 如果卡住了，用最简单的词汇表达",
                "duration": 15,
            }
        ]
        return steps

    def compare_languages(self, lang1: str, lang2: str) -> Dict:
        """
        对比两种语言的认知特征

        Args:
            lang1: 语言1代码
            lang2: 语言2代码

        Returns:
            对比结果
        """
        feat1 = get_language_feature(lang1)
        feat2 = get_language_feature(lang2)

        comparison = {
            "languages": [feat1.get("name", lang1), feat2.get("name", lang2)],
            "key_differences": []
        }

        # 对比关键认知特征
        features_to_compare = [
            ("tense_system", "时态系统"),
            ("grammatical_gender", "语法性别"),
            ("honorifics", "敬语系统"),
            ("classifiers", "量词系统"),
            ("spatial_metaphors", "空间隐喻"),
        ]

        for feat_key, feat_name in features_to_compare:
            val1 = feat1.get("cognitive_features", {}).get(feat_key, "N/A")
            val2 = feat2.get("cognitive_features", {}).get(feat_key, "N/A")

            if val1 != val2:
                comparison["key_differences"].append({
                    "feature": feat_name,
                    f"{lang1}": val1,
                    f"{lang2}": val2,
                    "implication": self._get_implication(feat_key, val1, val2)
                })

        return comparison

    def _get_implication(self, feat_key: str, val1: str, val2: str) -> str:
        """获取特征差异的认知含义"""
        implications = {
            "tense_system": "时态系统的差异可能影响对时间精确性的感知",
            "grammatical_gender": "语法性别的存在可能影响对物体属性的联想",
            "honorifics": "敬语复杂度影响对社会关系和等级的敏感度",
            "classifiers": "量词丰富度影响对物体分类的思维方式",
            "spatial_metaphors": "空间隐喻的差异影响对时间的空间化思考",
        }
        return implications.get(feat_key, "这一差异可能带来独特的认知视角")


class LanguageSwitchGuide:
    """语言切换引导流程控制器（用于Streamlit）"""

    def __init__(self):
        self.switcher = LanguageSwitcher()
        self.current_step = 0

    def start_switch(self, target_language: str) -> List[Dict]:
        """开始语言切换流程"""
        self.current_step = 0
        return self.switcher.get_switch_steps(target_language)

    def get_progress_message(self, step_index: int, total_steps: int = 5) -> str:
        """获取进度消息"""
        messages = [
            "让我们开始吧...",
            "沉浸在语言中...",
            "激活语言中枢...",
            "理解认知特征...",
            "准备完成！",
        ]
        return messages[min(step_index, len(messages) - 1)]
