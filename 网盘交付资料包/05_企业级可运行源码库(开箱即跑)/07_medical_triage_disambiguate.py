"""
07_medical_triage_disambiguate.py
=============================================================================
第 7 章：医疗智能多模态分诊与画像动态加权消歧系统
包含：
  1. 患者多维静态与动态画像建模 (PatientProfile)
  2. 三级场景与意图消歧引擎 (Level 1~3 Intent Disambiguation)
  3. 医疗危急重症风控拦截规则库
  4. 临床证据链条推演与结构化报告输出 (TriageReport)

运行方法：
  python src/07_medical_triage_disambiguate.py
=============================================================================
"""

import json
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field, asdict


@dataclass
class PatientProfile:
    """患者多维健康画像"""
    patient_id: str
    age: int
    gender: Literal["male", "female"]
    chronic_diseases: List[str] = field(default_factory=list)  # 如: 高血压, 冠心病, 糖尿病
    allergies: List[str] = field(default_factory=list)          # 过敏史: 青霉素, 磺胺
    vital_signs: Dict[str, Any] = field(default_factory=dict)   # 生命体征: {"sbp": 160, "dbp": 105, "hr": 115}
    recent_habits: List[str] = field(default_factory=list)      # 近期生活习惯: 熬夜, 暴饮暴食


@dataclass
class TriageDecision:
    """分诊与消歧决策输出"""
    level_1_category: str     # 一级大类: 门诊导诊 / 急危重症 / 慢病复诊 / 药物咨询
    target_department: str    # 推荐科室: 急诊抢救室 / 心内科 / 呼吸内科
    urgency_level: str        # 危险等级: P1-致命危急 / P2-中危紧急 / P3-普通门诊
    clinical_rationale: str   # 临床证据链逻辑
    action_guidance: str      # 患者即刻行动指引
    red_flag_warning: bool    # 是否触发危急重症红色拦截警报


class MedicalSemanticDisambiguator:
    """
    生产级三级意图消歧引擎：
    解决“同一主诉表象，在不同患者画像上对应完全不同致病机理与急迫度”的致命缺陷。
    """
    def __init__(self):
        # 知识图谱高危关联特征
        self.cardiac_keywords = ["胸闷", "胸痛", "心慌", "压迫感", "压榨感", "出冷汗", "冷汗", "放射痛", "心前区", "闷痛"]
        self.cerebral_keywords = ["口角歪斜", "单侧肢体无力", "言语不清", "突发剧烈头痛"]

    def disambiguate(self, complaint_text: str, profile: PatientProfile) -> TriageDecision:
        print(f"\n[启动语义消歧] 患者: {profile.patient_id} (年龄: {profile.age}, 性别: {profile.gender})")
        print(f"  主诉描述: \"{complaint_text}\"")
        print(f"  基础病史: {profile.chronic_diseases} | 体征: {profile.vital_signs}")

        # 1. 一级特征匹配
        matched_cardiac = any(k in complaint_text for k in self.cardiac_keywords)
        matched_cerebral = any(k in complaint_text for k in self.cerebral_keywords)

        # 2. 脑卒中 FAST 紧急拦截
        if matched_cerebral:
            return TriageDecision(
                level_1_category="急危重症抢救",
                target_department="急诊卒中绿色通道",
                urgency_level="P1-致命危急",
                clinical_rationale="主诉命中神经系统缺血/出血特异体征，存在急性脑血管病可能。",
                action_guidance="立即拨打 120 呼叫急救车，患者保持平卧位、头偏向一侧，切勿剧烈搬动或盲目喂水喂药！",
                red_flag_warning=True
            )

        # 3. 胸痛三级动态加权消歧
        if matched_cardiac:
            # 因子 A: 年龄 >= 55 岁
            # 因子 B: 伴有高血压/冠心病/高血脂
            # 因子 C: 伴有放射痛或冷汗
            high_risk_score = 0
            if profile.age >= 55:
                high_risk_score += 3
            if "高血压" in profile.chronic_diseases or "冠心病" in profile.chronic_diseases:
                high_risk_score += 4
            if "压榨感" in complaint_text or "出冷汗" in complaint_text or "放射痛" in complaint_text:
                high_risk_score += 5
            
            sbp = profile.vital_signs.get("sbp", 120)
            if sbp >= 160:
                high_risk_score += 2

            print(f"  --> 心血管危急加权得分: {high_risk_score} 分 (>=6 分触发急诊拦截)")

            if high_risk_score >= 6:
                return TriageDecision(
                    level_1_category="急危重症抢救",
                    target_department="急诊科 / 心血管重症监护室 (CCU)",
                    urgency_level="P1-致命危急",
                    clinical_rationale=f"高龄合并慢性病患者出现典型心前区不适(风险分 {high_risk_score})，高度警惕急性冠脉综合征(ACS)/心肌梗死。",
                    action_guidance="请即刻停止一切活动并坐下休息，立即呼叫家人或急救车(120)，备好硝酸甘油(若血压不低)，尽快到院复查心电图与心肌酶谱！",
                    red_flag_warning=True
                )
            elif profile.age < 35 and ("熬夜" in profile.recent_habits or "咖啡" in complaint_text):
                return TriageDecision(
                    level_1_category="普通门诊导诊",
                    target_department="心内科普通门诊 / 心身健康门诊",
                    urgency_level="P3-普通门诊",
                    clinical_rationale="年轻患者、无心脑血管基础病，近期有熬夜等不良诱因，考虑生理性心动过速或交感神经过度兴奋。",
                    action_guidance="建议近几日早睡休息，暂停饮用浓茶与咖啡。如心悸反复发作，可前往门诊预约 24 小时动态心电图(Holter)排查。",
                    red_flag_warning=False
                )
            else:
                return TriageDecision(
                    level_1_category="专科门诊检查",
                    target_department="心血管内科门诊",
                    urgency_level="P2-中危紧急",
                    clinical_rationale="症状具有心前区特异性，但暂无极高危伴随症状，需常规心血管专科排查。",
                    action_guidance="建议 24 小时内就诊心血管内科门诊，完善基础心电图及心脏彩超检查。",
                    red_flag_warning=False
                )

        # 默认兜底
        return TriageDecision(
            level_1_category="全科门诊分流",
            target_department="全科医学科 / 综合内科",
            urgency_level="P3-普通门诊",
            clinical_rationale="未捕获特征性急危重症靶标关键词，建议由全科医师进行初诊查体。",
            action_guidance="请前往全科门诊挂号，由接诊医生进一步问询详细病史与体格检查。",
            red_flag_warning=False
        )


if __name__ == "__main__":
    engine = MedicalSemanticDisambiguator()

    # 案例一：67岁老年男性，既往高血压，突发胸闷冷汗
    patient_a = PatientProfile(
        patient_id="PT_1001_OLD",
        age=67,
        gender="male",
        chronic_diseases=["高血压", "高脂血症"],
        vital_signs={"sbp": 165, "dbp": 102, "hr": 98},
        recent_habits=[]
    )
    result_a = engine.disambiguate("今天上午起突然感觉胸口有些闷痛，胸前区有压迫感，身上一直在冒冷汗", patient_a)
    print("=" * 70)
    print(f"【患者 A 分诊报告】")
    print(f"  分类大项: {result_a.level_1_category} | 推荐科室: {result_a.target_department}")
    print(f"  紧迫等级: {result_a.urgency_level} | 红色警报: {result_a.red_flag_warning}")
    print(f"  证据链分析: {result_a.clinical_rationale}")
    print(f"  指引意见: {result_a.action_guidance}")

    # 案例二：22岁年轻女性，既往体健，连续加班后胸口心慌
    patient_b = PatientProfile(
        patient_id="PT_2002_YOUNG",
        age=22,
        gender="female",
        chronic_diseases=[],
        vital_signs={"sbp": 115, "dbp": 75, "hr": 105},
        recent_habits=["熬夜", "连续通宵加班"]
    )
    result_b = engine.disambiguate("最近连续加了三天班，今天坐着工位上总感觉心慌心跳特别快", patient_b)
    print("=" * 70)
    print(f"【患者 B 分诊报告】")
    print(f"  分类大项: {result_b.level_1_category} | 推荐科室: {result_b.target_department}")
    print(f"  紧迫等级: {result_b.urgency_level} | 红色警报: {result_b.red_flag_warning}")
    print(f"  证据链分析: {result_b.clinical_rationale}")
    print(f"  指引意见: {result_b.action_guidance}")
