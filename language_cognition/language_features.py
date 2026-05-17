"""
语言认知特征库
定义各语言的认知特征，用于引导和分析
"""
from typing import Dict, List


LANGUAGE_FEATURES = {
    "zh": {
        "name": "中文",
        "family": "汉藏语系",
        "writing_system": "意音文字（汉字）",
        "cognitive_features": {
            "tense_system": "弱时态系统，通过语境和助词表达时间",
            "grammatical_gender": "无语法性别",
            "honorifics": "有限的敬语系统（您、请等）",
            "classifiers": "丰富的量词系统，影响物体分类思维",
            "spatial_metaphors": "垂直时间隐喻为主（上星期、下个月）",
            "pronoun_drop": "常省略代词，语境依赖强",
            "character_visual": "汉字的视觉空间特性影响记忆",
            "tonal": "声调语言，音调影响语义",
        },
        "thinking_hints": [
            "用中文思考时，你可能更关注整体关系而非个体特征",
            "时间概念更多是垂直流动的（上/下）",
            "量词选择会影响你对物体属性的感知",
            "语境比形式语法更重要",
        ],
        "immersion_text": """
春天来了，公园里的花都开了。老人们在树下打太极，孩子们在草地上奔跑。
阳光透过树叶洒下来，在地面上投下斑驳的影子。一位妈妈指着天上的风筝对孩子说：
"你看，风筝飞得越来越高了。"孩子兴奋地拍着手。这就是生活中最简单的幸福。
"""
    },
    "en": {
        "name": "英文",
        "family": "印欧语系",
        "writing_system": "拼音文字（拉丁字母）",
        "cognitive_features": {
            "tense_system": "强时态系统，16种时态精确表达时间关系",
            "grammatical_gender": "几乎没有语法性别",
            "honorifics": "敬语系统很弱，基本用you称呼所有人",
            "classifiers": "量词系统非常有限",
            "spatial_metaphors": "水平时间隐喻为主（before/after）",
            "pronoun_required": "句子通常需要主语",
            "phonetic_writing": "拼音文字，音形对应较规则",
        },
        "thinking_hints": [
            "用英文思考时，你会更精确地表达时间关系",
            "时间概念更多是水平流动的（前/后）",
            "句子结构更强调主语的动作",
            "对因果关系的表达更明确",
        ],
        "immersion_text": """
Spring has arrived. Flowers are blooming in the park. Elderly people practice
Tai Chi under the trees while children run on the grass. Sunlight filters
through leaves, casting dappled shadows on the ground. A mother points to
a kite in the sky and says to her child: "Look, the kite is flying higher
and higher!" The child claps excitedly. This is the simplest happiness in life.
"""
    },
    "ja": {
        "name": "日文",
        "family": "日本语系",
        "writing_system": "汉字+假名混合",
        "cognitive_features": {
            "tense_system": "过去/非过去二元时态",
            "grammatical_gender": "无语法性别",
            "honorifics": "极其复杂的敬语系统，反映严格的社会等级",
            "classifiers": "非常丰富的量词系统",
            "spatial_metaphors": "垂直与水平隐喻并存",
            "wa_ga_distinction": "は/が区别影响主题与焦点的认知",
            "omission_pronoun": "频繁省略人称代词",
            "ambiguity_tolerant": "容忍歧义，依赖语境理解",
        },
        "thinking_hints": [
            "用日语思考时，你会自动意识到社会等级和人际关系",
            "は标记主题，が标记新信息——这影响你的注意力分配",
            "模糊性被视为自然和优雅的",
            "听者需要读懂言外之意",
        ],
        "immersion_text": """
春が来ました。公園の花が咲いています。お年寄りたちは木の下で太極拳をし、
子供たちは芝生の上を走っています。木漏れ日が地面にまだらな影を落としています。
母親が空の凧を指して子供に言いました：「ほら、凧がどんどん高くなっているわ。」
子供は興奮して手をたたきました。これが人生で最も単純な幸せです。
"""
    },
    "de": {
        "name": "德文",
        "family": "印欧语系",
        "writing_system": "拉丁字母",
        "cognitive_features": {
            "tense_system": "复杂时态系统",
            "grammatical_gender": "三个语法性别（阳、阴、中）",
            "honorifics": "Sie/du 正式/非正式区分",
            "case_system": "四格变格系统",
            "compound_nouns": "复合名词能力极强",
            "verb_final": "从句中动词置于句末",
        },
        "thinking_hints": [
            "用德语思考时，每个名词都有性别属性",
            "格系统让你更清晰地思考角色关系",
            "复合名词允许创造新概念",
            "动词在句末让你听完整个句子才能理解核心动作",
        ]
    },
    "fr": {
        "name": "法文",
        "family": "印欧语系",
        "writing_system": "拉丁字母",
        "cognitive_features": {
            "tense_system": "丰富时态，包括条件式和虚拟式",
            "grammatical_gender": "两个语法性别",
            "honorifics": "vous/tu 区分",
            "formality": "非常重视正式性的语言",
            "subjunctive": "虚拟式使用频繁",
        },
        "thinking_hints": [
            "用法语思考时，你会更多使用虚拟语气表达可能性",
            "每个名词都带有性别",
            "你会更关注社交距离和正式程度",
        ]
    }
}


def get_supported_languages() -> List[str]:
    """获取支持的语言列表"""
    return list(LANGUAGE_FEATURES.keys())


def get_language_feature(lang_code: str, feature: str = None) -> Dict:
    """获取语言的认知特征"""
    if lang_code not in LANGUAGE_FEATURES:
        return {}

    lang_data = LANGUAGE_FEATURES[lang_code]
    if feature:
        return lang_data.get("cognitive_features", {}).get(feature, "")
    return lang_data


def get_thinking_hints(lang_code: str) -> List[str]:
    """获取某语言的思考提示"""
    return LANGUAGE_FEATURES.get(lang_code, {}).get("thinking_hints", [])


def get_immersion_text(lang_code: str) -> str:
    """获取某语言的沉浸文本"""
    return LANGUAGE_FEATURES.get(lang_code, {}).get("immersion_text", "")
