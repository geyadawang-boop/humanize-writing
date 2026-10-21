"""Regression probes for quantity preservation and non-prescriptive advice."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    'lint_advice_subject', Path(__file__).resolve().parents[1] / 'scripts' / 'ai_smell_lint.py')
LINT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINT)

FRACTION = (
    '第一组样本抽取总量的十分之一，用于测量初始状态；第二组样本抽取余量的十分之一，'
    '用于复核仪器读数；第三组样本仍按原定方案抽取总量的十分之一，用于核对批次差异。'
    '三个分母并不相同，操作人员应分别登记总量、余量与抽样数量，不能将三个比例直接相加，'
    '也不能为了表述简短省略分母。')


class LintAdviceTests(unittest.TestCase):
    def test_fraction_is_not_a_degree_adverb(self):
        issues, status, _ = LINT.evaluate(FRACTION, 'tech')
        self.assertEqual(status, 'ok')
        self.assertFalse(any(w > 0 and "'十分'" in m for w, m in issues), issues)

    def test_time_quantity_exclusions_preserve_real_adverbs(self):
        quantities = '十分之一 十分之三 四十分之一 十分钟 三十分鐘 九点十分 十點十分 九时十分 九点二十分 十点五十分'
        self.assertEqual(LINT.count_degree_word(quantities, '十分'), 0)
        self.assertEqual(LINT.count_degree_word(quantities + ' 当时十分清楚 平时十分担忧 此时十分谨慎', '十分'), 3)
        points = '这一点十分重要 第一点十分重要 第二点十分清楚 第十一点十分具体 那一点十分明确'
        self.assertEqual(LINT.count_degree_word(points, '十分'), 5)

    def test_degree_adverb_still_reports_without_weakening_facts(self):
        issues, _, _ = LINT.evaluate(FRACTION + '记录十分清楚。操作十分谨慎。我们十分担忧。', 'tech')
        matches = [(w, m) for w, m in issues if w > 0 and "'十分'" in m]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0][0], 4)
        self.assertIn('× 3', matches[0][1])
        self.assertIn('不自动弱化', matches[0][1])

    def test_functional_forms_trigger_review_without_mandatory_rewriting(self):
        cases = [
            ('路标词', '首先核对合同。其次登记数量。最后保存原稿。', 3, '必要流程顺序'),
            ('对照句式', '这不是结论，而是记录。那不是猜测，而是证词。', 0, '静态次数不能判断拉踩'),
            ('顿号连排', '记录包括铜板、石块、竹筒、麻绳。', 4, '完整列项'),
            ('冒号列表', '步骤如下：一是核对编号。注意事项：二是登记数量。', 5, '编号引用'),
            ('四字套话', '春风化雨、润物无声。风调雨顺、国泰民安。实事求是、求真务实。', 6, '有功能的排比'),
            ('抽象名词化', '他的不安变成了一种难以言明的恐惧。', 5, '不强制转成动作'),
            ('总结式结尾', '总而言之，我们仍需保存原稿。', 8, '必要总结'),
            ('展望式收尾', '期待周五与大家相聚。', 8, '真实计划、祝愿和邀请'),
            ('段落开头', '\n\n'.join(['雨来了，河面上的船都停了下来，船头那盏灯还没有熄灭。'] * 3), 5, '有意复沓'),
            ('段内枚举', '请记住，一是核对姓名；二是核对数量。', 6, '引用关系'),
            ('礼貌框架', '首先感谢贵方及时复函。再次感谢贵方的帮助。', 6, '礼仪功能'),
        ]
        for tag, suffix, weight, protection in cases:
            with self.subTest(tag=tag):
                issues, status, _ = LINT.evaluate(FRACTION + '\n\n' + suffix, 'general')
                self.assertEqual(status, 'ok')
                hits = [(w, m) for w, m in issues if m.startswith('[' + tag + ']') and (w > 0 or weight == 0)]
                self.assertEqual(len(hits), 1, issues)
                self.assertEqual(hits[0][0], weight)
                self.assertIn(protection, hits[0][1])
                self.assertIn('保留', hits[0][1])
                for old in ('→ 重写其一', '→ 改成自然叙述', '→ 变换开头', '删一半', '删掉大部分'):
                    self.assertNotIn(old, hits[0][1])

    def test_genre_exemptions_describe_limited_historical_evidence(self):
        issues, status, _ = LINT.evaluate(FRACTION, 'tech')
        self.assertEqual(status, 'ok')
        message = next(m for _, m in issues if m.startswith('[genre]'))
        self.assertIn('历史设计样本', message)
        self.assertIn('不代表充分标定', message)

    def test_repetition_and_simile_advice_do_not_prescribe_quotas(self):
        repetition = ('她又走到门前，听见雨水敲着铁皮。她又走到窗前，听见风把树叶推开。'
                      '她又走到桌前，听见电话轻轻作响。她又走到床前，听见孩子梦里翻身。') * 2
        simile = ('远处的山像一只沉睡的兽，雪还压在它的背上。近处的桥像一条绷紧的弦，'
                  '老人在桥上停住，伸手扶了一下栏杆。他记得这条河涨水时的声音，也记得父亲把绳子'
                  '交到他手里时说过的话。那些话已经过去多年，如今只剩下几个字。他没有急着往前走，'
                  '等同伴越过自己，才低头看见鞋面上裂开的细纹。')
        messages = []
        for sample in (repetition, simile):
            issues, status, _ = LINT.evaluate(sample, 'fiction')
            self.assertEqual(status, 'ok')
            messages.extend(m for _, m in issues)
        joined = '\n'.join(messages)
        self.assertIn('不按比例插句', joined)
        self.assertIn('不为比例添情节', joined)
        self.assertIn('不设统一数量上限', joined)
        for old in ('每 3 个长句插入', '至多留 1 处', '没人说话。', '场景必改'):
            self.assertNotIn(old, joined)


if __name__ == '__main__':
    unittest.main()
