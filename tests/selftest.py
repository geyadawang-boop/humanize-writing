# -*- coding: utf-8 -*-
"""humanize-writing 自测：验证 ai_smell_lint.py 的关键行为。

运行:
    python tests/selftest.py

退出码 0 = 全部通过；非 0 = 有断言失败（打印明细）。
覆盖点：
  1. 冻结ai_heavy样本按v0.43得33分，核对剩余独立信号；旧47分含已撤回的形式罚分
  2. 人味样本必须判"优秀"
  3. 末段"综上所述"必须被识别为总结式结尾（旧版检测位置错位，会漏报）
  4. 正常逻辑连接词"因此"结尾不得被误判为总结式结尾（旧版会误报）
  5. 文本过短必须判"无法判定"，绝不显示"优秀"
  6. 单换行分段必须被识别（Word 粘贴常见）
  7. 强 AI 词、英文 AI 词、顿号连排必须被捕获
  8. 纯英文稿进入英文模式并捕获英文 AI 词
  9. 常见小说表达必须被捕获（只提示核读，不等于质量结论）
  10. 短文本双向校准：短 AI 腔归一后必须不通过，短人味稿不受影响
  11. 对抗样本：真实“降 AI”洗稿文本（过厂商自带检测）v0.41 精确得 8 分，计分项仅为{顿号连排}；旧14分属历史规则
  12. 混合中英文本：中英各自都不到自己的门槛、但合计已够判时必须走混合模式，
      不得判“无法判定”（旧版 gate 用 and 连接两条门槛，此处会漏判）
  13. 文体门控：--genre tech 必须关闭结构类检查（句长/短句/路标词/顿号连排/
      总结式结尾/段落/段内枚举）并保留词汇检查，风险分低于 general；非法 --genre 退出码 2
  14. 新文体门控（law/email/speech/fiction）：4 篇真人语料按各自门控回归全优秀；
      law 豁免顿号连排/总结式结尾，speech 豁免路标词，fiction 豁免段落开头，
      email 零豁免与 general 等分且无 [genre] 说明行
  15. v0.20 新增检查：四字套话连缀（右边界，长列举串内嵌对不报）/段首序数
      （排除「一、」式编号与「第N条」）/展望式收尾（仅末 3 段）；探针正反双向
      命中，AI 对照语料命中新信号，真人语料与对抗样本零误伤
  16. v0.23 新增检查：文艺比喻（明喻 ≥2 处且 ≥1.0/300 字双门，真人单处不罚）/
      抽象名词化（族内首报）/段内枚举（前导标点门，tech/academic/official 豁免
      ——TECH_SPEC 即 ⑬ 设计样本）/礼貌框架（成对才罚）；探针正反双向，
      AI 对照语料命中新信号，真人语料与对抗样本零误伤
"""
import contextlib
import importlib.util
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "ai_smell_lint", ROOT / "scripts" / "ai_smell_lint.py"
)
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

SAMPLE_AI = (ROOT / "tests" / "samples" / "ai_heavy.md").read_text(encoding="utf-8")
SAMPLE_HUMAN = (ROOT / "tests" / "samples" / "human_like.md").read_text(encoding="utf-8")
SAMPLE_AI_SHORT = (ROOT / "tests" / "samples" / "ai_heavy_short.md").read_text(encoding="utf-8")
SAMPLE_HUMAN_SHORT = (ROOT / "tests" / "samples" / "human_like_short.md").read_text(encoding="utf-8")
# 对抗样本：AI 起草 → “降 AI”工具洗稿 → 通过该厂商自带检测的真实盲测标本（姓名/学号已脱敏）
# 历史 v0.7.1–v0.40 为14分（少短句6 + 顿号连排8）；v0.41取消少短句加分，当前锚点为8分。
SAMPLE_DEAI = (ROOT / "tests" / "samples" / "deai_processed.md").read_text(encoding="utf-8")

TAIL_SUMMARY = (
    "他先翻了两天手册，把常见故障挨个排了一遍，又换了三根探头，找隔壁工位借了一根屏蔽线，"
    "甚至把整台示波器搬到另一个房间试了试，折腾到周五下午才发现问题出在电磁炉上——那玩意儿一开，"
    "整个台面的底噪就抬起来了，波形自然飘得没法看，跟探头其实一点关系都没有。\n\n"
    "综上所述，只有把细节做到位，实验才能顺利推进。"
)

TAIL_YINCI = (
    "这块地我种了四年。第一年种黄瓜，全军覆没；第二年改种番茄，勉强活了七棵，还被虫子啃掉一半。"
    "今年我学乖了，先测土壤酸碱度，又挑了耐涝的品种，苗期还搭了简易的遮阳网，收成还是不算多，"
    "但比去年强了不少。因此我打算明年再试一次，顺便把排水沟挖深一些。"
)

ONE_LINE_PER_PARA = "\n".join(["这是第一段的内容，讲的是我在实验室里折腾设备的一件小事，前后花了三天时间。"] * 4)

# 技术规范式样本：句长均匀、无短句、路标词齐、顿号连排、综上所述收尾——
# general 模式必然误伤（审查 P4 边界案例），tech 门控后应只剩词汇罚分
TECH_SPEC = (
    "本系统采用模块化架构，主要由数据接入层、处理层、存储层、展示层四部分组成。"
    "数据接入层负责采集原始日志，首先对数据进行清洗，其次进行格式转换，最后写入消息队列。\n\n"
    "处理层消费队列消息：一是实时计算，二是离线分析，三是结果回传。"
    "该方案具有高效、稳定、可扩展、易维护、低成本的特点，能够全面提升系统性能。\n\n"
    "综上所述，本方案通过统一的数据链路与分层设计，为后续的功能迭代奠定坚实基础。"
)

# ⑭ 新文体合成误伤用例：法律意见书式行文（路标词 ×4 + 顿号连排 ×2 + 综上所述收尾），
# general 必然误伤；law 门控应豁免顿号连排/总结式结尾并保留路标词与 AI 词检查
LAW_SPEC = (
    "关于贵司与某房地产开发公司商品房买卖合同纠纷一案，本所律师查阅了合同文本、付款凭证及发票、"
    "双方往来函件、催告记录等材料，现就贵司关注的合同效力、违约责任及维权路径出具意见如下。\n\n"
    "首先，关于合同效力。双方签订的《商品房买卖合同》系双方真实意思表示，内容不违反法律、行政法规的"
    "强制性规定，依法成立并生效，双方均应按照约定全面履行各自的义务，任何一方不得擅自变更或者解除。\n\n"
    "其次，关于逾期交房的违约责任。开发商未在合同约定的期限内交付房屋，已经构成违约，贵司有权要求其"
    "按照合同约定支付违约金；经催告后三个月内仍未交付的，贵司有权解除合同，并一并主张相应的损失赔偿。\n\n"
    "再次，关于诉讼时效。主债权诉讼时效期间为三年，自约定交房期限届满之日起算，贵司此前发送催告函的"
    "行为构成时效中断，时效期间自催告送达之日起重新计算，请注意留存送达凭证。\n\n"
    "最后，关于证据固定。建议贵司妥善保管合同文本、付款凭证及发票、双方往来函件、催告函及送达凭证等"
    "原件材料，必要时办理证据保全公证。\n\n"
    "综上所述，贵司可以先行与开发商协商解决方案；协商不成的，可以依法提起诉讼，通过法律途径维护自身"
    "合法权益。如有进一步问题，欢迎随时与本所联系。"
)

# ⑭ 演讲稿式行文（路标词 首先/其次/最后 ×3），speech 门控应豁免路标词
SPEECH_SPEC = (
    "各位老师、各位同学，大家好。今天站在这里，我不想先讲道理，先讲一件小事。\n\n"
    "开学前一晚，我在操场走了一圈。宿舍楼的灯一格一格亮起来，有人在天台练歌，有人在楼下倒计时，"
    "还有个男生蹲在台阶上给家里打电话，说妈我到了，一切都好。那一刻我意识到，新的学期是真的来了。\n\n"
    "首先，希望大家把课表当地图，而不是当清单。走一走没去过的教室、实验室和操场看台，"
    "认识几个上课之外的朋友，食堂里、球场上、社团里都算。\n\n"
    "其次，希望大家这学期给一件小事留位置。它可以是一篇读书笔记，也可以是每天二十个俯卧撑，"
    "期末回头看，它会替你作证，这一年你没有糊弄自己。\n\n"
    "最后，把一句话送给大家：慢慢来，比较快。我的话讲完了，谢谢大家。"
)

# ⑭ 小说片段式行文（"林晚的"起头段落 ×3，对应 p[:3] 键），fiction 门控应豁免段落开头
FICTION_SPEC = (
    "林晚的伞还在滴水，她把它挂在门后，地毯上洇出一小片深色的印子。"
    "玄关的灯没开，她摸黑换鞋，听见厨房有水声，锅盖被顶起来又落下，一下一下，像谁在数拍子。\n\n"
    "林晚的胃里空空的，可她一点也不饿。她走到窗前，把窗户推开一条缝，雨声一下子涌进来，"
    "把屋里的安静衬得更实了。茶几上摆着两副碗筷，一副动过，一副还冒着热气。\n\n"
    "林晚的钥匙在口袋里攥出了一道印子。她想了想，把到嘴边的话又咽了回去，"
    "最后只挤出一句，你吃过饭没有。\n\n"
    "陈默从厨房探出头来，围裙上沾着油点。他说明早六点的车，硬座，二十六个小时。"
    "他说这话的时候没看她，锅铲在锅里翻了两下，油星子跳起来又落回去。"
    "窗外的雨还在下，路灯把水洼照成一块一块碎掉的镜子。"
    "她数了数，茶几旁边的烟灰缸里已经有七个烟头，而他进门到现在，不过半个小时。"
)

# ⑮/⑯ v0.20 与 v0.23 新增检查探针：正例必须命中，反例必须不命中（右边界排除长列举串内嵌对、
# 「一、」式编号不算路标起段、展望窗口只看末 3 段；v0.23 反例分别验证 count 门/
# 前导标点门/成对门，探针文本按 tests/corpus_ai_calib 标定的模式层指纹构造）
QUAD_PAIR_POS = (
    "新学期第一次班会上，班长希望同学们凝心聚力、拼搏进取，勤奋学习、勇于探索，锤炼品格、强健体魄，"
    "用一学期的坚持换期末的好收成。会后大家把口号写在黑板右侧，值日表贴在门后，"
    "教室后面的绿植也换了两盆新的，连讲台上的粉笔盒都摆整齐了。"
)
QUAD_PAIR_NEG = (
    "本次年度评估涉及数据科学、人工智能与计算模拟三个方向，覆盖分子设计、高通量筛选、智能催化、"
    "微纳制造、减污降碳等六个领域，全部原始数据、工艺参数、中试规模记录均已归档备查，"
    "后续复查可直接调阅，评估报告下周一提交科研处，纸质版一式两份。"
)
ORD_POS = (
    "上学期我们组在流程上吃过三次亏，这学期把规矩定成下面三条，请大家互相提醒执行。\n\n"
    "首先，每次实验前提前十分钟到场，把仪器预热、探头检查一遍再开始动手。\n\n"
    "其次，参数改动必须当场记进本子，事后补记的数据一律当作不可靠处理。\n\n"
    "最后，离开实验室前把台面收拾干净，废液和手套分开丢进指定的桶里。"
)
ORD_NEG = (
    "整改清单共三条，本周内逐项落实，周五下午由值班组长逐条验收。\n\n"
    "一、消防通道不得堆放纸箱杂物，发现一处当天清理，并记录在值班本上由组长复核。\n\n"
    "二、配电箱前一米范围内不得堆放物品，警示线脱落应当天补贴，并在周例会上通报。\n\n"
    "三、下班前检查水电门窗并签字，最后离开的人负责锁门，钥匙交回值班室登记。"
)
OUTLOOK_POS = (
    "项目组这一年从三个人做到十个人，服务器从一台扩到四台，线上故障率降了一半还多，"
    "客服响应时间从两天缩到三个小时，工单积压从每周四百件降到五十件以内，"
    "这些都是大家一个个周末熬出来的。\n\n"
    "相信在大家的共同努力下，我们一定能够把产品做得更好。"
)
OUTLOOK_NEG = (
    "相信在大家的共同努力下，我们一定能够按时交付，所以先把丑话说在前面，别到时候互相埋怨。\n\n"
    "第一版上线时间定在四月二十号，往前倒排，三月十号前必须冻结需求，之后只修故障不加功能。\n\n"
    "测试环境这周先搭起来，数据库的备份脚本也要一并跑通，别等到上线前临时抱佛脚。\n\n"
    "有困难提前说，别憋着，资源能协调的由我来协调，工期上我们不玩虚的，说到做到。"
)
SIMILE_POS = (
    "周五加班到十点，写字楼里只剩我们这一层还亮着灯，键盘声像下雨一样密密地落了一片。"
    "走出大堂的时候，保安已经换了一班，夜风把衬衫吹得贴在背上，整个人就像一块拧干又晾硬的毛巾。"
    "回到家楼下，便利店的灯还开着，我买了瓶冰水站在门口喝完，才觉得这一天总算过去了。"
)
SIMILE_NEG = (
    "听证会开了一上午，双方的证词对不上，法官反复确认付款的具体日期。"
    "轮到我方陈述时，我把三张转账凭证按时间摆开，指出第二笔款项的到账日比合同约定晚了四十天，"
    "对方的代理人对着投影沉默了几秒，说回去再核对一次。散会后我在台阶上站了一会儿，"
    "觉得这案子像一根卡在缝里的钉子，硬拔会伤到墙，得想办法慢慢旋出来。"
)
NOMINAL_POS = (
    "散伙饭吃完，大家在校门口拍了一张合影就散了。回到空了一半的宿舍，"
    "我把四年的东西一样一样往箱子里装，装到一半停下来坐了很久。阳台上的绿萝还是她走之前浇过水的，"
    "心里变成了一种钝钝的难过，说不出是为了什么，只觉得明天开始就不用再定七点的闹钟了。"
)
NOMINAL_NEG = (
    "检查了三遍才发现是接线柱松了，拧紧之后示波器上的波形立刻稳了下来。"
    "我把这次的处理过程写进值班的交接本，特别注明先查接触、再看探头、最后才怀疑仪器本身，"
    "免得下一个人再绕一圈。组长看后在页脚补了一句，说明周组会拿这个当案例讲五分钟。"
)
ENUM_POS = (
    "这次搬家我给自己定了三条规矩，写在手机备忘录里贴在冰箱上。"
    "一是所有纸箱按房间编号，二是当天拆封的箱子当天清空不隔夜，三是超过半年没用的东西直接送人，"
    "不许再搬进新家。搬完清点，四十多个箱子没有一件落下的，新客厅第二天就能坐下来吃饭。"
)
ENUM_NEG = (
    "评审会上有人问起选型依据，我说唯一的判断标准是稳不稳，这套基础组件团队用了两年没换过，"
    "几次故障复盘的记录都能翻到。至于备选的新框架，不是不好，而是迁移成本太高，"
    "不如把这笔预算花在监控告警上，把线上故障的响应时间再压一压。"
)
POLITE_POS = (
    "王老师您好，先把这次课题结题的材料清单发给您。"
    "首先感谢您一路以来对课题组的指导，中期检查和结题材料都多亏您把关。"
    "附件里的三份表格已按科研处模板填好，其中经费执行表有两处口径我不太确定，已在批注里标黄。"
    "再次感谢您抽时间审阅，盼您周四前把意见发回来，我按反馈修改后统一提交。"
)
POLITE_NEG = (
    "李姐，随信附上这次出差报销的发票原件和行程单，共十一张，其中高铁票两张、住宿票四张，"
    "金额合计两千三百六十元，与系统里填的数目一一核对过，没有出入，多退少补的部分按财务流程下月一并结算。"
    "再次感谢你在我出差那几天帮忙盯了组里的周报和两组数据，回来请你喝咖啡。"
)
NEW_TAGS = ("[四字套话]", "[段首序数]", "[展望式收尾]",
            "[文艺比喻]", "[抽象名词化]", "[段内枚举]", "[礼貌框架]")

# ⑭ 真人语料回归（与 tests/corpus/SOURCES.md 对应）：按各自门控必须判优秀
CORPUS_REAL = [
    ("law", "law_gongbao_hongxiufeng.md"),
    ("email", "email_liangdishu.md"),
    ("speech", "speech_wen_yiduo_zuihou.md"),
    ("fiction", "fiction_kong_yiji.md"),
]


def main():
    fails = []

    issues, status, score = lint.evaluate(SAMPLE_AI)
    # v0.43撤回段落6分与锚点8分：同一原稿47→33；不调整阈值来保留旧分类。
    expected_weighted = sorted([(4, "[AI 词]")] * 4 + [(9, "[路标词]"), (8, "[总结式结尾]")])
    actual_weighted = sorted((w, m.split("]", 1)[0] + "]") for w, m in issues if w)
    if status != "ok" or score != 33 or actual_weighted != expected_weighted:
        fails.append("① 冻结样本按v0.43应得33分并保留4个词表、路标词及总结式结尾信号，实得 score=%s status=%s weighted=%s" % (score, status, actual_weighted))

    issues, status, score = lint.evaluate(SAMPLE_HUMAN)
    if status != "ok" or score >= lint.GOOD_LINE:
        fails.append("② 人味样本应判优秀，实得 score=%s status=%s" % (score, status))

    issues, status, _ = lint.evaluate(TAIL_SUMMARY)
    if not any("总结式结尾" in m for _, m in issues):
        fails.append("③ 末段'综上所述'未被识别为总结式结尾（位置检测失效）")

    issues, status, _ = lint.evaluate(TAIL_YINCI)
    if any("总结式结尾" in m for _, m in issues):
        fails.append("④ 正常'因此'结尾被误判为总结式结尾")

    for name, text in (("空文本", ""), ("六字", "今天天气不错。"), ("短句", "他走了。" * 8)):
        issues, status, score = lint.evaluate(text)
        if status != "short" or lint.label_of(score, status) != "无法判定":
            fails.append("⑤ %s 应判无法判定，实得 label=%s" % (name, lint.label_of(score, status)))

    paras = lint.paragraphs(ONE_LINE_PER_PARA)
    if len(paras) != 4:
        fails.append("⑥ 单换行分段未生效，识别到 %d 段（应为 4）" % len(paras))

    probe = "赋能这个词加上抓手这个词，还有闭环和底层逻辑，全都堆在一句话里。"
    issues, _, _ = lint.evaluate(probe * 4)
    hits = [m for _, m in issues if "AI 词" in m]
    if len(hits) < 4:
        fails.append("⑦ 强 AI 词未充分捕获，命中 %d 个" % len(hits))

    probe_en = "We need to delve into the tapestry and leverage robust seamless solutions. " * 3
    pad = (
        "这是一段用来凑够中文字数的填充文本，内容本身没有什么特别的意义，"
        "主要目的是让短文本判定不至于提前返回，从而能够走到英文词表检测那一步。"
    )
    issues, status, _ = lint.evaluate(probe_en + pad * 2)
    if status != "ok":
        fails.append("⑦ 中英混排样本过短（status=%s），测试无效" % status)
    elif not any("英文 AI 词" in m for _, m in issues):
        fails.append("⑦ 英文 AI 词未捕获")

    probe_dunhao = "我们需要高效、可扩展、可持续、创新的技术方案来解决这个问题，并且在落地过程中保持敏捷、稳健、透明、可控的执行节奏，确保每一步都可以被追溯、被复核、被审计。"
    issues, _, _ = lint.evaluate(probe_dunhao * 2)
    if not any("顿号连排" in m for _, m in issues):
        fails.append("⑦ 顿号连排未捕获")

    en_text = (
        "Remote work is not going away. The hard part is not the software. "
        "We need to delve into the tapestry and leverage robust seamless solutions. "
    ) * 12
    issues, status, score = lint.evaluate(en_text, language="en")
    if status != "ok":
        fails.append("⑧ 纯英文稿未进入英文模式（status=%s）" % status)
    elif not any("英文 AI 词" in m for _, m in issues):
        fails.append("⑧ 英文模式下未捕获 AI 词")
    elif score <= lint.PASS_LINE:
        fails.append("⑧ 英文重 AI 味稿应判不通过，实得 %d" % score)

    novel_text = (
        "她抬眸看向他，眼底闪过一丝慌乱。他面无表情地回视，唇角微微勾起一个弧度。"
        "半晌，她缓缓开口，声音微微发颤。他心里涌上一股暖意，下意识地往前一步。"
        "窗外的月色皎洁，晚风习习，灯火璀璨。\n\n"
        "他张了张嘴，终究没说出话来。这一刻五味杂陈，心脏猛地一缩。"
        "她别过脸去，指尖泛白，身子一僵。岁月静好，大概就是这个样子。"
    )
    issues, status, score = lint.evaluate(novel_text)
    if status != "ok":
        fails.append("⑨ 网文样本过短（status=%s）" % status)
    elif not any(w == 5 and "常见小说表达" in m for w, m in issues):
        fails.append("⑨ 常见小说表达未按原权重捕获")

    issues, status, score = lint.evaluate(SAMPLE_AI_SHORT)
    if status != "ok" or score <= lint.PASS_LINE:
        fails.append("⑩ 短文本 AI 腔归一化后应判不通过，实得 score=%s status=%s" % (score, status))
    if not any("短文本" in m for _, m in issues):
        fails.append("⑩ 短文本归一化未在输出中标注")

    issues, status, score = lint.evaluate(SAMPLE_HUMAN_SHORT)
    if status != "ok" or score >= lint.GOOD_LINE:
        fails.append("⑩ 短文本人味稿应判优秀，实得 score=%s status=%s" % (score, status))

    issues, status, score = lint.evaluate(SAMPLE_DEAI)
    deai_deduct = [m for w, m in issues if w]
    if status != "ok" or score != 8:
        fails.append("⑪ 对抗样本按v0.41应精确得 8 分，实得 score=%s status=%s" % (score, status))
    if len(deai_deduct) != 1 or not any("顿号连排" in m for m in deai_deduct):
        fails.append("⑪ 对抗样本计分项应为{顿号连排}共 1 项，实得 %s" % deai_deduct)

    # ⑫ 混合中英文本：中文 51 字（<100）、英文 92 词（<100），合计 143 信息单位 ≥ MIXED_MIN_UNITS
    mixed_cn = (
        "昨天下午我把那台旧示波器搬到窗边，想看看底噪到底从哪来。探头换了三根，屏蔽线也借了一根，"
        "折腾两个钟头才反应过来是隔壁电磁炉在作怪，一开火波形就飘。"
    )
    mixed_en = (
        "The whole afternoon felt wasted until the real cause showed up. "
        "It was not the probe, and it was not the grounding either. "
        "I need to delve into this and leverage robust seamless solutions going forward. "
        "The rule going forward is simple: test one variable at a time, and write down "
        "what actually changed before touching anything else in the setup."
    )
    mixed_probe = mixed_cn + " " + mixed_en
    mixed_cn_n = lint.chinese_len(mixed_cn)
    mixed_en_n = len(re.findall(r"[A-Za-z][A-Za-z'-]*", mixed_en))
    issues, status, score = lint.evaluate(mixed_probe, language="mixed")
    if status != "ok":
        fails.append(
            "⑫ 混合中英文本（中%d字+英%d词，合计 %d）应判可判定，实得 status=%s label=%s"
            % (mixed_cn_n, mixed_en_n, mixed_cn_n + mixed_en_n, status, lint.label_of(score, status))
        )
    else:
        if not any("混合模式" in m for _, m in issues):
            fails.append("⑫ 混合模式标注缺失")
        if not any("英文 AI 词" in m for _, m in issues):
            fails.append("⑫ 混合模式下英文词表未生效（'delve/leverage/robust/seamless' 应命中）")

    # ⑬ 文体门控：tech 关闭结构类检查、保留词汇检查；非法 --genre 退出码 2
    struct_tags = ("[句长]", "[短句]", "[路标词]", "[顿号连排]", "[冒号列表]", "[总结式结尾]", "[段落]", "[段内枚举]")
    gen_issues, gen_status, gen_score = lint.evaluate(TECH_SPEC)
    tech_issues, tech_status, tech_score = lint.evaluate(TECH_SPEC, genre="tech")
    if gen_status != "ok":
        fails.append("⑬ 技术规范样本 general 模式应可判定，实得 status=%s" % gen_status)
    else:
        gen_struct = [m for w, m in gen_issues if w and m.startswith(struct_tags)]
        if not gen_struct:
            fails.append("⑬ general 模式未对技术规范产生任何结构类罚分（回归基线失效，应误伤）")
    tech_struct = [m for w, m in tech_issues if w and m.startswith(struct_tags)]
    if tech_struct:
        fails.append("⑬ tech 文体仍产生结构类罚分: %s" % tech_struct)
    if not any(m.startswith("[genre]") for _, m in tech_issues):
        fails.append("⑬ tech 文体缺 [genre] 门控说明行")
    if not any("[AI 词]" in m and w for w, m in tech_issues):
        fails.append("⑬ tech 文体应保留词汇检查（'全面提升/奠定坚实基础' 应命中）")
    if tech_status != "ok" or tech_score >= gen_score:
        fails.append("⑬ tech 模式风险分应低于 general，实得 tech=%d general=%d status=%s"
                     % (tech_score, gen_score, tech_status))
    err_buf = io.StringIO()
    with contextlib.redirect_stderr(err_buf):
        rc_bogus = lint.main(["--genre", "bogus"])
    if rc_bogus != 2 or "未知 --genre" not in err_buf.getvalue():
        fails.append("⑬ 非法 --genre 应返回 2 并在 stderr 提示，实得 rc=%s" % rc_bogus)
    err_buf2 = io.StringIO()
    with contextlib.redirect_stderr(err_buf2):
        rc_missing = lint.main(["--genre"])
    if rc_missing != 2 or "--genre 需要一个值" not in err_buf2.getvalue():
        fails.append("⑬ --genre 缺值应返回 2 并在 stderr 提示（不得静默读 stdin），实得 rc=%s" % rc_missing)

    # ⑭ 新文体门控：真实语料回归 + 合成误伤用例（law/email/speech/fiction）
    for genre, name in CORPUS_REAL:
        text = (ROOT / "tests" / "corpus" / name).read_text(encoding="utf-8")
        issues, status, score = lint.evaluate(text, genre=genre)
        if status != "ok" or score >= lint.GOOD_LINE:
            fails.append("⑭ 真人语料 %s 按 %s 门控应判优秀，实得 score=%s status=%s"
                         % (name, genre, score, status))

    gen_issues, gen_status, gen_score = lint.evaluate(LAW_SPEC)
    law_issues, law_status, law_score = lint.evaluate(LAW_SPEC, genre="law")
    if gen_status != "ok" or law_status != "ok":
        fails.append("⑭ LAW_SPEC 过短（general=%s law=%s），测试无效" % (gen_status, law_status))
    else:
        for tag in ("[顿号连排]", "[总结式结尾]"):
            if not any(m.startswith(tag) and w for w, m in gen_issues):
                fails.append("⑭ LAW_SPEC general 模式应命中 %s（回归基线失效）" % tag)
            if any(m.startswith(tag) and w for w, m in law_issues):
                fails.append("⑭ law 门控未豁免 %s: %s" % (
                    tag, [m for w, m in law_issues if w and m.startswith(tag)]))
        if not any(m.startswith("[genre] law") for _, m in law_issues):
            fails.append("⑭ law 门控缺 [genre] 说明行")
        if not (any(m.startswith("[路标词]") and w for w, m in law_issues)
                and any("[AI 词]" in m and w for w, m in law_issues)):
            fails.append("⑭ law 门控应保留路标词与 AI 词检查")
        if law_score >= gen_score:
            fails.append("⑭ law 模式风险分应低于 general，实得 law=%d general=%d"
                         % (law_score, gen_score))
        em_issues, em_status, em_score = lint.evaluate(LAW_SPEC, genre="email")
        if em_status != "ok" or em_score != gen_score:
            fails.append("⑭ email 零豁免应与 general 等分，实得 email=%d general=%d status=%s"
                         % (em_score, gen_score, em_status))
        if any(m.startswith("[genre]") for _, m in em_issues):
            fails.append("⑭ email 零豁免不应有 [genre] 说明行")

    gen_issues, gen_status, gen_score = lint.evaluate(SPEECH_SPEC)
    sp_issues, sp_status, sp_score = lint.evaluate(SPEECH_SPEC, genre="speech")
    if gen_status != "ok" or sp_status != "ok":
        fails.append("⑭ SPEECH_SPEC 过短（general=%s speech=%s），测试无效" % (gen_status, sp_status))
    else:
        if not any(m.startswith("[路标词]") and w for w, m in gen_issues):
            fails.append("⑭ SPEECH_SPEC general 模式应命中 [路标词]（回归基线失效）")
        if any(m.startswith("[路标词]") and w for w, m in sp_issues):
            fails.append("⑭ speech 门控未豁免 [路标词]")
        if not any(m.startswith("[genre] speech") for _, m in sp_issues):
            fails.append("⑭ speech 门控缺 [genre] 说明行")
        if sp_score >= gen_score:
            fails.append("⑭ speech 模式风险分应低于 general，实得 speech=%d general=%d"
                         % (sp_score, gen_score))

    gen_issues, gen_status, gen_score = lint.evaluate(FICTION_SPEC)
    fi_issues, fi_status, fi_score = lint.evaluate(FICTION_SPEC, genre="fiction")
    if gen_status != "ok" or fi_status != "ok":
        fails.append("⑭ FICTION_SPEC 过短（general=%s fiction=%s），测试无效" % (gen_status, fi_status))
    else:
        if not any(m.startswith("[段落开头]") and w for w, m in gen_issues):
            fails.append("⑭ FICTION_SPEC general 模式应命中 [段落开头]（回归基线失效）")
        if any(m.startswith("[段落开头]") and w for w, m in fi_issues):
            fails.append("⑭ fiction 门控未豁免 [段落开头]")
        if not any(m.startswith("[genre] fiction") for _, m in fi_issues):
            fails.append("⑭ fiction 门控缺 [genre] 说明行")
        if fi_score >= gen_score:
            fails.append("⑭ fiction 模式风险分应低于 general，实得 fiction=%d general=%d"
                         % (fi_score, gen_score))

    # ⑮ v0.20 新增检查：探针正反双向 + AI 对照语料命中 + 真人语料/对抗样本零误伤
    for pname, text, tag, expect in (
        ("四字套话+排比串", QUAD_PAIR_POS, "[四字套话]", True),
        ("四字套话-长列举串", QUAD_PAIR_NEG, "[四字套话]", False),
        ("段首序数+路标起段", ORD_POS, "[段首序数]", True),
        ("段首序数-「一、」编号", ORD_NEG, "[段首序数]", False),
        ("展望收尾+末段", OUTLOOK_POS, "[展望式收尾]", True),
        ("展望收尾-仅前段", OUTLOOK_NEG, "[展望式收尾]", False),
        ("文艺比喻-两处明喻", SIMILE_POS, "[文艺比喻]", True),
        ("文艺比喻-仅一处", SIMILE_NEG, "[文艺比喻]", False),
        ("抽象名词化-一种包装", NOMINAL_POS, "[抽象名词化]", True),
        ("抽象名词化-动作落地", NOMINAL_NEG, "[抽象名词化]", False),
        ("段内枚举-一是二是", ENUM_POS, "[段内枚举]", True),
        ("段内枚举-前导非标点", ENUM_NEG, "[段内枚举]", False),
        ("礼貌框架-成对客套", POLITE_POS, "[礼貌框架]", True),
        ("礼貌框架-仅再次感谢", POLITE_NEG, "[礼貌框架]", False),
    ):
        issues, status, _ = lint.evaluate(text)
        hit = any(m.startswith(tag) and w for w, m in issues)
        if status != "ok" or hit != expect:
            fails.append("⑮ 探针 %s 应命中=%s，实得 status=%s 命中=%s" % (pname, expect, status, hit))

    d_ca = ROOT / "tests" / "corpus_ai"
    ca_em_issues, ca_em_status, ca_em_score = lint.evaluate(
        (d_ca / "ai_email_reply.md").read_text(encoding="utf-8"), genre="email")
    if ca_em_status != "ok" or not all(
            any(m.startswith(t) and w for w, m in ca_em_issues) for t in ("[段首序数]", "[展望式收尾]", "[段内枚举]")):
        fails.append("⑮ ai_email_reply 应命中 [段首序数]+[展望式收尾]+[段内枚举]（status=%s）" % ca_em_status)
    if any(m.startswith("[四字套话]") and w for w, m in ca_em_issues):
        fails.append("⑮ ai_email_reply 不应命中 [四字套话]")
    ca_sp_issues, ca_sp_status, ca_sp_score = lint.evaluate(
        (d_ca / "ai_speech_ceremony.md").read_text(encoding="utf-8"), genre="speech")
    if ca_sp_status != "ok" or not all(
            any(m.startswith(t) and w for w, m in ca_sp_issues) for t in ("[四字套话]", "[展望式收尾]", "[段内枚举]")):
        fails.append("⑮ ai_speech_ceremony 应命中 [四字套话]+[展望式收尾]+[段内枚举]（status=%s）" % ca_sp_status)
    ca_law_issues, ca_law_status, _ = lint.evaluate(
        (d_ca / "ai_law_memo.md").read_text(encoding="utf-8"), genre="law")
    if ca_law_status == "ok":
        hit_new = [t for t in NEW_TAGS if any(m.startswith(t) and w for w, m in ca_law_issues)]
        if hit_new:
            fails.append("⑮ ai_law_memo 不应命中新检查（已知盲区应保持稳定）: %s" % hit_new)
    for genre, name in CORPUS_REAL:
        issues, _, _ = lint.evaluate(
            (ROOT / "tests" / "corpus" / name).read_text(encoding="utf-8"), genre=genre)
        hit_new = [t for t in NEW_TAGS if any(m.startswith(t) and w for w, m in issues)]
        if hit_new:
            fails.append("⑮ 真人语料 %s 误伤新检查: %s" % (name, hit_new))
    deai_issues, _, _ = lint.evaluate(SAMPLE_DEAI)
    hit_new = [t for t in NEW_TAGS if any(m.startswith(t) and w for w, m in deai_issues)]
    if hit_new:
        fails.append("⑮ 对抗样本误伤新检查: %s" % hit_new)

    if fails:
        print("自测失败 %d 项：" % len(fails))
        for f in fails:
            print("  ✗ " + f)
        return 1

    print("自测全部通过 ✓")
    print("  冻结 ai_heavy 样本 score=%d（v0.43应 =33；旧47含段落6+锚点8，不调整25/40阈值）" % lint.evaluate(SAMPLE_AI)[2])
    print("  人味样本 score=%d（应 <%d）" % (lint.evaluate(SAMPLE_HUMAN)[2], lint.GOOD_LINE))
    print("  短文本 AI 腔 score=%d（应 >%d）" % (lint.evaluate(SAMPLE_AI_SHORT)[2], lint.PASS_LINE))
    print("  短文本人味稿 score=%d（应 <%d）" % (lint.evaluate(SAMPLE_HUMAN_SHORT)[2], lint.GOOD_LINE))
    print("  对抗样本 score=%d（v0.41应 =8）" % lint.evaluate(SAMPLE_DEAI)[2])
    print("  技术规范 tech 门控 score=%d（general=%d，tech 应更低）"
          % (lint.evaluate(TECH_SPEC, genre="tech")[2], lint.evaluate(TECH_SPEC)[2]))
    print("  历史语料门控回归：所收 %d 篇均未超过提示阈值；法律意见书 law 门控 score=%d（general=%d，law 应更低）"
          % (len(CORPUS_REAL), lint.evaluate(LAW_SPEC, genre="law")[2], lint.evaluate(LAW_SPEC)[2]))
    print("  新增检查回归：ai_email_reply(email)=%d、ai_speech_ceremony(speech)=%d（新信号均命中）"
          % (ca_em_score, ca_sp_score))
    print("  v0.23 探针 8 组正反双向通过；所收反例的未触发断言覆盖 %d 个新标签，不代表总体零误报"
          % len(NEW_TAGS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
