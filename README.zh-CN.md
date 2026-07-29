# 循证医学科研写作

**Evidence-First Medical Writing**

<img src="assets/logo.png" alt="循证医学科研写作图标" width="144">

[English README](README.md)

这是一个由 Yi 发布和维护的双语 Codex skill，用于以研究可信度和证据边界为先，规划、诊断、修改和检查医学科研论文。

发布者及维护者：**Yi**  
联系邮箱：[duyinapoleon@gmail.com](mailto:duyinapoleon@gmail.com)

本项目为独立产品，不隶属于、不代表、未获得任何作者、出版社、期刊、机构、平台或其他第三方的授权、认可或背书。

方法来源说明：本工作流基于多来源医学科研写作与编辑实践，提炼可迁移的方法原则、工作流与检查表。公开仓库不指向任何具体第三方来源或贡献者。

仓库地址：<https://github.com/duyi-neurooph/evidence-first-medical-writing>

## 主要能力

- 建立研究任务卡、PICO-T、核心命题和 IMRaD 大纲；
- 检查研究问题、设计、终点、分析、结果与结论是否一致；
- 在语言润色前发现研究诚信和报告风险；
- 修改题目、摘要、正文各章节、图表、投稿信和审稿回复；
- 支持随机研究、观察性研究、诊断、预测、系统综述/Meta、病例类和短文等常见类型；
- 按 `P0 可信度阻断项`、`P1 研究逻辑`、`P2 结构与自明性`、`P3 语言与格式` 分级输出问题。

## 安全边界

本 skill 不得：

- 编造数据、方法、注册、伦理批准、引文或审稿决定；
- 为追求显著性而改变终点、阈值、分析集或结论；
- 把相关性升级为因果，或把无统计学显著性写成等效；
- 隐瞒阴性主要结果、局限、偏离、错误或不确定性；
- 冒充真实个人或复现可识别的个人文风；
- 在没有可核验许可时宣称授权、背书、隶属或官方身份；
- 暴露患者信息、保密手稿、私人通信或身份映射。

它用于辅助写作和研究推理，不能替代临床判断、统计签字、伦理审查、法律意见或目标期刊的最新要求。

## 使用

1. 下载本仓库的最新 release；
2. 按你的 Codex 环境所支持的流程安装 skill 或 skills-only plugin；
3. 调用 `$evidence-first-medical-writing`，或要求进行“证据优先的医学论文诊断”。

克隆仓库：

```bash
git clone https://github.com/duyi-neurooph/evidence-first-medical-writing.git
```

运行入口：

```text
skills/evidence-first-medical-writing/SKILL.md
```

示例：

```text
使用 $evidence-first-medical-writing，先诊断这篇论文最重要的三个
可信度或主线一致性问题，再处理语言。
```

```text
为这项观察性研究设计题目、结构式摘要信息框架和 IMRaD 大纲。
不要虚构缺失结果，统一标记为待作者补充。
```

```text
改写这份审稿回复，分别写清立场、采取的行动、结果、对结论的影响
以及稿件中的修改位置。
```

请勿在公开 GitHub issue 中粘贴保密手稿、可识别健康信息、未发表数据或私人审稿通信。

## 目录结构

```text
.
├── .codex-plugin/plugin.json
├── .github/
├── assets/
├── skills/evidence-first-medical-writing/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── LICENSE.md
├── NOTICE.md
├── PRIVACY.md
├── SUPPORT.md
└── TERMS.md
```

## 许可

本仓库采用 [PolyForm Noncommercial License 1.0.0](LICENSE.md)，以“源码可见”的方式发布。仅可在该许可证定义的许可目的范围内使用、修改和再分发。

本项目可免费获取，但不宣称为开源软件或自由软件。使用、修改或再分发前请阅读许可证全文。商业使用需要另行取得 Yi 的书面许可。

再分发全部或部分项目时，必须一并提供许可证全文或官方 URL，并保留项目提供的每一行 `Required Notice:`。

## 贡献、支持与权利异议

提交 pull request 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。使用与安全报告方式见 [SUPPORT.md](SUPPORT.md)、[SECURITY.md](SECURITY.md)、[PRIVACY.md](PRIVACY.md)及 [TERMS.md](TERMS.md)。

如果你认为仓库内容影响了你享有的权利，请使用 **Rights concern** issue 模板，或以 `Rights Concern` 为邮件主题联系 [duyinapoleon@gmail.com](mailto:duyinapoleon@gmail.com)。不要在公开 issue 中提交保密证据。

## 版本

当前版本：`0.3.0`。

Copyright © 2026 Yi。详见 [NOTICE.md](NOTICE.md)。
