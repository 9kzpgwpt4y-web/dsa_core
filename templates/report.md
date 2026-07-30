# 📈 深度量化决策摘要：{{ stock_name }} ({{ stock_code }})
**生成时间**: {{ report_time }} | **趋势状态**: {{ trend_status }}

---

### 📊 核心估值基准
* **总市值**: {{ market_cap }} 亿元
* **当前市盈率 (PE)**: {{ pe_ratio }} | **市净率 (PB)**: {{ pb_ratio }}
* **业绩增速预期**: {{ growth_rate }}%

### 🧠 AI 大脑核心结论
> **{{ conclusion }}**

### 🎯 1-2周波段操作计划
* **入场区间**: {{ entry_price }}
* **防守底线 (止损)**: {{ stop_loss }}
* **目标阻力位 (止盈)**: {{ target_price }}

### ⚠️ 风险排查清单
{% for risk in risks %}
- [ ] {{ risk }}
{% endfor %}