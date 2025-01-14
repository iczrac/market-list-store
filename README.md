# Market List

这是一个用于获取和统一处理市场股票列表数据的工具。项目利用多个数据源获取股票基础信息，并进行统一处理，为后续的数据研究提供基础支持。

## 功能特点

- 支持从多个数据源获取股票列表数据
  - 东方财富(em)
  - 富途(futu)
  - 新浪(sina)
- 统一处理和整合不同来源的数据
- 定期更新数据，保持信息时效性
- 提供标准化的数据格式，方便后续研究使用

## 项目结构

```
market-list/
├── us-stock-market/         # 美股市场数据
│   └── rawdata/            # 原始数据文件
│       ├── em-us-marketlist-*.csv    # 东方财富美股列表
│       ├── futu-us-marketlist-*.csv  # 富途美股列表
│       └── sina-us-marketlist-*.csv  # 新浪美股列表
```

## 数据源说明

1. 东方财富(em)
   - 数据来源：通过akshare接口获取
   - 文件格式：CSV
   - 更新频率：每日

2. 富途(futu)
   - 数据来源：通过futu-api获取
   - 文件格式：CSV
   - 更新频率：每日

3. 新浪(sina)
   - 数据来源：通过akshare接口获取
   - 文件格式：CSV
   - 更新频率：每日

## 依赖说明

- Python 3.8+
- akshare：用于获取东方财富和新浪数据
- 8n8：用于数据处理和整合
- futu-api：用于获取富途数据

## 使用方法

1. 安装依赖
```bash
pip install akshare
pip install futu-api
pip install 8n8
```

2. 运行数据更新
```bash
python update_market_list.py
```

## 数据字段说明

每个数据源的原始数据字段可能不同，但经过处理后会统一为以下格式：

- symbol: 股票代码
- name: 股票名称
- exchange: 交易所
- industry: 行业分类
- market_cap: 市值
- price: 当前价格
- volume: 成交量

## 注意事项

1. 需要确保有足够的网络连接来获取数据
2. 建议定期运行更新以保持数据时效性
3. 不同数据源的数据可能存在差异，建议根据实际需求选择合适的数据源

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 许可证

MIT License