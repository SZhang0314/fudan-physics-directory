# 复旦大学 物理方向教师目录 (Fudan Physics Faculty Directory)

一个可搜索、可筛选的复旦大学物理方向教师名录，覆盖：

- **物理学系** (Department of Physics) — 凝聚态、光学、统计/生物物理、量子信息、天体物理等
- **现代物理研究所（核科学与技术系）** (Institute of Modern Physics) — 核物理、粒子物理、原子分子物理、核技术、计算物理、聚变科学与工程

共 **163** 位教师，其中 140 位为深度档案（含研究方向、代表性论文、个人主页）。

## 产物

| 文件 | 说明 |
|---|---|
| `index.html` | 自包含网页（内嵌 CSS/JS + 数据），双击即可打开，也可部署到 GitHub Pages |
| `data/faculty.json` | 结构化数据，唯一事实来源（one record per researcher） |
| `data/imp.json` | 现代物理研究所原始名册解析 |
| `data/batch_*.txt`, `data/enriched_*.json` | 深挖阶段的工作文件与中间结果 |
| `scripts/merge_imp.py` | 将 IMP 名册合并进 faculty.json |
| `scripts/merge_enriched.py` | 将深挖片段合并进 faculty.json 并提升置信度 |

## 数据字段

每条记录包含：`id, name, school, department, title, subject, research_directions,
focus_areas, summary, publications[], homepage, profile_url, email, sources[],
confidence, verified`。

- `confidence`: `coarse`（仅名册）或 `fine`（含深挖 + 已核验）
- `verified`: 是否通过权威主页核验
- `sources`: 实际使用的证据 URL，便于审计

## 两阶段检索方法

1. **粗检索 (Pass 1)**：抓取官方师资目录（物理学系「教职工名册」、现代物理研究所各方向列表），
   得到姓名、职称、研究方向、邮箱、主页链接。
2. **深挖 (Pass 2)**：逐个抓取教师个人主页，提取研究领域、子方向、代表性论文、个人主页；
   核验后提升为 `fine`。

## 重新生成

```bash
python scripts/merge_imp.py         # 合并 IMP 名册
python scripts/merge_enriched.py    # 合并深挖结果
python ../.config/opencode/skills/search_prof/scripts/build_site.py \
    --data data/faculty.json --out . --title "复旦大学 物理方向教师目录"
```

## 数据来源

- 物理学系师资队伍: https://phys.fudan.edu.cn/7476/list.htm
- 现代物理研究所教职工列表: https://imp.fudan.edu.cn/48903/list.htm
- 各教师个人主页（见每条记录的 `sources`）

## 免责声明

本目录仅收集公开的师资主页信息（已发表论文、公开邮箱、研究方向）。姓名唯一性以
「院系 + 研究方向」共同确认；若某条记录与实际情况有出入，欢迎核对 `sources` 后修正。
