import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire('/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/');
const { chromium } = require('playwright');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outputDir = path.resolve(__dirname, '小红书图文配图_9张');

const cards = [
  // 卡片 1: 主封面 (明亮、清爽、实体书出版质感)
  {
    filename: '01_主图封面_AI_Agent全栈实战手册.png',
    pageIndex: '01 / 09',
    badge: '📚 2026 企业交付级实战手册',
    title: 'AI Agent 全栈开发<br>与商业落地工程实操',
    subtitle: '从 0 到 1 打造可交付、高可用的企业级智能体系统',
    desc: '系统化打通：核心心法 · 14步成长路线 · 技术底座 · 框架选型 · 商业案例 · 面试通关',
    contentHtml: `
      <div class="cover-hero">
        <div class="stat-pills">
          <div class="pill"><strong>7.5 万字</strong> 详尽精撰</div>
          <div class="pill"><strong>14 步</strong> 就业进阶</div>
          <div class="pill"><strong>3 大</strong> 商业实战</div>
          <div class="pill"><strong>全套</strong> 架构高清图</div>
        </div>

        <div class="grid-2x2">
          <div class="clean-card">
            <div class="cc-header">
              <span class="cc-emoji">🧠</span>
              <span class="cc-title">架构认知与心法</span>
            </div>
            <div class="cc-text">5大底层逻辑，精准区分高频业务与一次性需求，化整为零单节点打磨，标准化 MCP 资产</div>
          </div>

          <div class="clean-card">
            <div class="cc-header">
              <span class="cc-emoji">🗺️</span>
              <span class="cc-title">14 步全景进阶</span>
            </div>
            <div class="cc-text">从 Python 服务化、Transformer、Prompt Cache、混合 RAG 到 LangGraph 与 Eino</div>
          </div>

          <div class="clean-card">
            <div class="cc-header">
              <span class="cc-emoji">🏢</span>
              <span class="cc-title">三大企业商业案例</span>
            </div>
            <div class="cc-text">日均 10 万次高可用客服、Dify 电商售后工作流、医疗多模态智能问诊系统从 0 到 1 复盘</div>
          </div>

          <div class="clean-card">
            <div class="cc-header">
              <span class="cc-emoji">🎯</span>
              <span class="cc-title">大厂面试与真题</span>
            </div>
            <div class="cc-text">幻觉控制、长文本防爆、死循环熔断、RAGAS 评测矩阵，配套 STAR 简历与面试题库</div>
          </div>
        </div>

        <div class="gift-banner">
          <div class="gb-icon">🎁</div>
          <div class="gb-content">
            <div class="gb-title">全套交付物清单</div>
            <div class="gb-sub">高清精排 PDF 手册 + 离线网页版 + 未加密 Markdown 原稿 + 文档站源码</div>
          </div>
          <div class="gb-tag">网盘秒发</div>
        </div>
      </div>
    `
  },

  // 卡片 2: 交付清单
  {
    filename: '02_全套交付清单一览.png',
    pageIndex: '02 / 09',
    badge: '📦 拍下即发 · 交付清单',
    title: '全套资料包含什么？',
    subtitle: '整齐规范归纳 · 满足从阅读、笔记到二次开发的全部需求',
    desc: '下单后自动发送百度网盘 / 夸克网盘链接，永久保存，多端支持',
    contentHtml: `
      <div class="list-wrapper">
        <div class="clean-row">
          <div class="cr-idx">01</div>
          <div class="cr-icon">📘</div>
          <div class="cr-main">
            <div class="cr-title">实操手册 PDF 精排版</div>
            <div class="cr-desc">包含全套层级目录与书签跳转，适配手机、iPad、Kindle 与电脑随时随地阅读。</div>
          </div>
        </div>

        <div class="clean-row">
          <div class="cr-idx">02</div>
          <div class="cr-icon">🌐</div>
          <div class="cr-main">
            <div class="cr-title">离线单文件 HTML 版</div>
            <div class="cr-desc">无需安装任何运行环境，双击浏览器即开即看，排版清晰，代码支持一键高亮复制。</div>
          </div>
        </div>

        <div class="clean-row">
          <div class="cr-idx">03</div>
          <div class="cr-icon">📝</div>
          <div class="cr-main">
            <div class="cr-title">完整 Markdown 未加密全本原稿</div>
            <div class="cr-desc">提供全本及 7 大独立分章源文件，方便导入飞书、语雀、Notion 构建个人知识库。</div>
          </div>
        </div>

        <div class="clean-row">
          <div class="cr-idx">04</div>
          <div class="cr-icon">📊</div>
          <div class="cr-main">
            <div class="cr-title">核心架构与流程高清大图合集</div>
            <div class="cr-desc">包含日均10万高可用拓扑、状态机流转、ReAct推理环、Dify工作流等无水印原图。</div>
          </div>
        </div>

        <div class="clean-row">
          <div class="cr-idx">05</div>
          <div class="cr-icon">💻</div>
          <div class="cr-main">
            <div class="cr-title">VitePress 交互式文档站整套源码</div>
            <div class="cr-desc">包含完整前端工程，一条命令即可在本地启动专属的现代知识库，支持一键部署。</div>
          </div>
        </div>
      </div>
    `
  },

  // 卡片 3: 第1~2章
  {
    filename: '03_第1至2章_心法认知与进阶路线.png',
    pageIndex: '03 / 09',
    badge: '🌱 阶段一 · 认知与路线',
    title: '心法认知与 14 步成长路线',
    subtitle: '建立清晰的工程思维，少走 90% 的弯路',
    desc: '从“单步长指令误区”走向企业级工作流，循序渐进掌握技能全貌',
    contentHtml: `
      <div class="two-section-layout">
        <div class="block-card">
          <div class="bc-head">
            <span class="bc-tag blue">第 1 章</span>
            <span class="bc-name">心法与认知篇：Agent 搭建五大底层逻辑</span>
          </div>
          <div class="point-grid">
            <div class="pg-item">
              <span class="bullet">1</span>
              <div><strong>区分问题属性：</strong>一次性发散任务用单次对话，高频重复流程才做 Agent 工作流。</div>
            </div>
            <div class="pg-item">
              <span class="bullet">2</span>
              <div><strong>化整为零原则：</strong>拒绝千字巨型 Prompt，单节点独立打磨与调试，串联成高可靠工作流。</div>
            </div>
            <div class="pg-item">
              <span class="bullet">3</span>
              <div><strong>善用平台工具：</strong>不做重复轮子，沉淀标准化 MCP 组件与 API 资产。</div>
            </div>
            <div class="pg-item">
              <span class="bullet">4</span>
              <div><strong>提示词闭环迭代：</strong>用 Bad Case 测试集驱动版本演进，而非靠灵感碰运气。</div>
            </div>
            <div class="pg-item">
              <span class="bullet">5</span>
              <div><strong>先以自用为主：</strong>从个人知识库与日常效率工具起步，建立持续正反馈。</div>
            </div>
          </div>
        </div>

        <div class="block-card">
          <div class="bc-head">
            <span class="bc-tag green">第 2 章</span>
            <span class="bc-name">路线图篇：Agent 全栈开发 14 步路线</span>
          </div>
          <div class="chip-container">
            <div class="step-chip"><span class="sc-num">01-03</span> Python 服务化、FastAPI、Transformer 底层机制</div>
            <div class="step-chip"><span class="sc-num">04-06</span> Prompt Cache 缓存优化、工业混合 RAG、Tool Calling 闭环</div>
            <div class="step-chip"><span class="sc-num">07-09</span> LangGraph 状态图、高并发 Go 框架 Eino、企业级 Workflow</div>
            <div class="step-chip"><span class="sc-num">10-14</span> AI Coding 协同、高可用容灾、算法八股、STAR 简历通关</div>
          </div>
        </div>
      </div>
    `
  },

  // 卡片 4: 第3章
  {
    filename: '04_第3章_架构与核心理论.png',
    pageIndex: '04 / 09',
    badge: '⚙️ 阶段二 · 核心架构',
    title: '经典 Agent 决策运行体系',
    subtitle: '解密智能体的大脑运转、记忆协同与规划范式',
    desc: '三元组经典机制、工业决策链与企业级 12-Factor 设计哲学',
    contentHtml: `
      <div class="arch-clean-box">
        <div class="triad-flow">
          <div class="tf-step">
            <div class="tf-badge">感知 Perception</div>
            <div class="tf-text">文本、ASR 语音、OCR 视觉输入与业务上下文抽取</div>
          </div>
          <div class="tf-arrow">→</div>
          <div class="tf-step active">
            <div class="tf-badge">规划 Planning</div>
            <div class="tf-text">任务拆解、ReAct 循环、反思纠错、短期与长期记忆协同</div>
          </div>
          <div class="tf-arrow">→</div>
          <div class="tf-step">
            <div class="tf-badge">行动 Action</div>
            <div class="tf-text">Tool Calling、接口请求、沙箱代码运行与结果交付</div>
          </div>
        </div>

        <div class="card-column">
          <div class="sub-item-card">
            <div class="sic-head">
              <span class="sic-icon">🛍️</span>
              <span class="sic-title">典型工业探索：电商助手决策链</span>
            </div>
            <div class="sic-body">从用户模糊意图识别、槽位抽取、商品与订单 API 串联，到真实结果反思校验与业务回传闭环。</div>
          </div>

          <div class="sub-item-card">
            <div class="sic-head">
              <span class="sic-icon">🔄</span>
              <span class="sic-title">主流规划算法机制</span>
            </div>
            <div class="sic-body">
              <strong>ReAct（思考-行动-观察循环）：</strong>解决大模型行动盲目性与信息断层。<br>
              <strong>Deep Research（深度搜索与总结）：</strong>多轮广度与深度动态探索。
            </div>
          </div>

          <div class="sub-item-card">
            <div class="sic-head">
              <span class="sic-icon">📏</span>
              <span class="sic-title">12-Factor Agents 设计原则</span>
            </div>
            <div class="sic-body">显式依赖声明、配置完全外置、状态机并发控制、优雅启停、全链路日志监控与死循环熔断保护。</div>
          </div>
        </div>
      </div>
    `
  },

  // 卡片 5: 第4章
  {
    filename: '05_第4章_关键技术底座.png',
    pageIndex: '05 / 09',
    badge: '🛠️ 阶段三 · 技术底座',
    title: 'Prompt、RAG、Tool Calling 与微调',
    subtitle: '决定 Agent 生产可用性与性价比的四大技术支柱',
    desc: '从 Token 成本极致优化，到高精度检索与本地工具安全调用闭环',
    contentHtml: `
      <div class="grid-2x2-clean">
        <div class="clean-tech-card">
          <div class="ctc-top">
            <span class="ctc-tag">01</span>
            <span class="ctc-title">Prompt 进阶与 Cache 优化</span>
          </div>
          <div class="ctc-content">
            • <strong>JSON Schema 强校验：</strong>确保输出确定性与下游服务直接消费<br>
            • <strong>Prompt Cache：</strong>静态前置+动态后置，实现 50%~80% 成本骤降与 70% 延迟优化
          </div>
        </div>

        <div class="clean-tech-card">
          <div class="ctc-top">
            <span class="ctc-tag">02</span>
            <span class="ctc-title">工业级混合 RAG 检索流水线</span>
          </div>
          <div class="ctc-content">
            • <strong>分块策略：</strong>字符切分 vs 语义切分 vs 父子层级块索引<br>
            • <strong>混合召回：</strong>BM25 关键词 + 向量相似度密集检索<br>
            • <strong>重排序：</strong>RRF 倒数融合与 BGE / Cohere Rerank 高精重排
          </div>
        </div>

        <div class="clean-tech-card">
          <div class="ctc-top">
            <span class="ctc-tag">03</span>
            <span class="ctc-title">Tool Calling 原生执行闭环</span>
          </div>
          <div class="ctc-content">
            • <strong>执行闭环：</strong>参数自动抽取、本地安全沙箱执行、异常重试<br>
            • <strong>MCP 协议：</strong>Anthropic 标准协议，跨数据库、Git 与文件系统互联
          </div>
        </div>

        <div class="clean-tech-card">
          <div class="ctc-top">
            <span class="ctc-tag">04</span>
            <span class="ctc-title">模型微调与分类网关融合</span>
          </div>
          <div class="ctc-content">
            • <strong>工具调用微调：</strong>开源模型 LoRA / SFT 专项微调<br>
            • <strong>轻量 BERT 网关：</strong>毫秒级低成本意图识别与安全拦截，为大模型降载
          </div>
        </div>
      </div>
    `
  },

  // 卡片 6: 第5章
  {
    filename: '06_第5章_现代编排框架篇.png',
    pageIndex: '06 / 09',
    badge: '🧩 阶段四 · 编排框架',
    title: 'Dify、LangGraph 与字节 Eino',
    subtitle: '全面覆盖主流零代码与代码级工业框架选型',
    desc: '从可视化拖拽到高并发 Go 核心服务，告别盲目选型',
    contentHtml: `
      <div class="frame-column">
        <div class="frame-box">
          <div class="fb-header">
            <span class="fb-badge dify">Dify</span>
            <span class="fb-title">零代码 / 低代码工业交付基座</span>
            <span class="fb-note">适合快速交付 & 知识库搭建</span>
          </div>
          <div class="fb-desc">
            实操企业级知识库向量化配置、可视化工作流复杂节点编排、多分支路由控制，以及将 Agent 发布为独立 API 供前后端系统集成。
          </div>
        </div>

        <div class="frame-box">
          <div class="fb-header">
            <span class="fb-badge lg">LangGraph</span>
            <span class="fb-title">代码级首选：图状态机架构</span>
            <span class="fb-note">适合复杂企业级状态流转</span>
          </div>
          <div class="fb-desc">
            基于 StateGraph 构建多轮状态转移，深入 State 状态共享机制、Node 节点函数、条件边（Conditional Edge）、持久化 Checkpoint 与人工介入审核（Human-in-the-loop）。
          </div>
        </div>

        <div class="frame-box">
          <div class="fb-header">
            <span class="fb-badge eino">字节跳动 Eino</span>
            <span class="fb-title">高并发 Go 语言大模型框架</span>
            <span class="fb-note">适合大厂高吞吐核心服务端</span>
          </div>
          <div class="fb-desc">
            字节跳动开源的工业级 Go 框架，深度拆解组件化模式、全异步流式计算、图编排调度与高并发内存极致优化。
          </div>
        </div>

        <div class="frame-box">
          <div class="fb-header">
            <span class="fb-badge auto">开源自主 Agent</span>
            <span class="fb-title">经典自主智能体解密</span>
            <span class="fb-note">AutoGPT / BabyAGI 架构分析</span>
          </div>
          <div class="fb-desc">
            剖析自主 Agent 的任务队列动态迭代、执行轨迹日志记录、长期向量记忆库与自我反思机制。
          </div>
        </div>
      </div>
    `
  },

  // 卡片 7: 第6章
  {
    filename: '07_第6章_三大企业商业实战案例.png',
    pageIndex: '07 / 09',
    badge: '🏢 阶段五 · 商业实战',
    title: '三大企业级已交付实战案例',
    subtitle: '拒绝玩具 Demo · 还原真实生产环境落地全貌',
    desc: '从架构设计、性能调优到高可用容灾，复盘真实交付细节',
    contentHtml: `
      <div class="case-column">
        <div class="case-card">
          <div class="cc-badge orange">商业交付案例 01</div>
          <div class="cc-title">日均 10 万次会话高可用智能客服系统</div>
          <div class="cc-points">
            <div>• <strong>双层意图网关：</strong>轻量 BERT 意图过滤（毫秒级拦截 60% 基础咨询）+ 大模型 Agent 处理长尾诉求</div>
            <div>• <strong>三级容灾降级：</strong>模型超时自动回退到知识库精准匹配，再降级为人工排队，保证服务永不宕机</div>
            <div>• <strong>性能与高可用：</strong>冷启动连接池预热，动态请求重试熔断，P99 响应延迟降低 65%</div>
          </div>
        </div>

        <div class="case-card">
          <div class="cc-badge blue">商业交付案例 02</div>
          <div class="cc-title">基于 Dify 搭建电商售后与工单 AI 助手</div>
          <div class="cc-points">
            <div>• <strong>复杂业务逻辑：</strong>打通订单查询、运费险规则判定、退货审核全流程自动化</div>
            <div>• <strong>多系统联动：</strong>Tool Calling 直连 ERP 数据库与主流快递物流接口</div>
            <div>• <strong>安全隔离机制：</strong>客户敏感信息自动脱敏过滤，接口鉴权与操作权限细粒度管控</div>
          </div>
        </div>

        <div class="case-card">
          <div class="cc-badge green">商业交付案例 03</div>
          <div class="cc-title">医疗多模态智能问诊与三级分诊系统</div>
          <div class="cc-points">
            <div>• <strong>多模态解析：</strong>结合病历 OCR 抽取、化验单数值解析与患者主诉文本</div>
            <div>• <strong>三级语义消歧：</strong>动态反问补充缺失病史，避免信息不足导致的误导性回答</div>
            <div>• <strong>安全与合规：</strong>医疗禁忌词与危机识别重定向，严格注入就诊免责声明</div>
          </div>
        </div>
      </div>
    `
  },

  // 卡片 8: 第7章
  {
    filename: '08_第7章_算法八股与求职面试.png',
    pageIndex: '08 / 09',
    badge: '🎯 阶段六 · 求职通关',
    title: '工业级算法八股与求职面试',
    subtitle: '高频核心考点梳理 · 助你在面试与技术交流中脱颖而出',
    desc: '从系统稳定性八股到科学评测指标，配套 STAR 简历与真题精解',
    contentHtml: `
      <div class="interview-column">
        <div class="white-box">
          <div class="wb-head">
            <span class="wb-icon">🛡️</span>
            <span class="wb-title">核心高频工程八股梳理</span>
          </div>
          <div class="wb-list">
            <div>• <strong>幻觉抑制方案：</strong>严密 Grounding 知识库锚定、Prompt Few-Shot 引导、置信度阈值过滤</div>
            <div>• <strong>长文本防爆窗：</strong>滑动窗口截断、LLM 渐进式摘要记忆、上下文选择性剪枝策略</div>
            <div>• <strong>死循环熔断：</strong>最大调用轮次上限（Max Steps）、相似参数高频调用拦截检测</div>
          </div>
        </div>

        <div class="white-box">
          <div class="wb-head">
            <span class="wb-icon">📈</span>
            <span class="wb-title">科学评估体系与监控矩阵</span>
          </div>
          <div class="wb-list">
            <div>• <strong>离线评估：</strong>采用 RAGAS 框架，深度评测忠实度（Faithfulness）、答案相关性、上下文精准率与召回率</div>
            <div>• <strong>在线监控：</strong>用户显式反馈（点赞/点踩率）、工具调用成功率、P90/P99 延迟监控指标</div>
          </div>
        </div>

        <div class="white-box">
          <div class="wb-head">
            <span class="wb-icon">💼</span>
            <span class="wb-title">STAR 法则简历包装与面试真题</span>
          </div>
          <div class="wb-list">
            <div>• <strong>STAR 项目包装：</strong>手把手将 Agent 落地拆解为情境-任务-行动-量化成果，直击大厂面试官关注点</div>
            <div>• <strong>大厂高频真题题库：</strong>覆盖意图路由、状态机容错、高并发降级等全流程经典问题与标准回答模板</div>
          </div>
        </div>
      </div>
    `
  },

  // 卡片 9: 下单说明与网盘发货
  {
    filename: '09_下单须知与网盘发货说明.png',
    pageIndex: '09 / 09',
    badge: '⚡ 自动发货 · 贴心售后',
    title: '下单须知与网盘发货说明',
    subtitle: '拍下系统自动秒发 · 百度网盘 / 夸克网盘',
    desc: '资料已规整分门别类，下载即学，永久有效',
    contentHtml: `
      <div class="delivery-wrapper">
        <div class="main-notice-box">
          <div class="mnb-icon">🚀</div>
          <div class="mnb-title">拍下自动秒发网盘链接</div>
          <div class="mnb-sub">支持【百度网盘】与【夸克网盘】高速下载链接</div>
        </div>

        <div class="two-by-two">
          <div class="feature-item">
            <div class="fi-title">📱 多端设备随时随地学习</div>
            <div class="fi-desc">PDF 与离线 HTML 版支持在手机、iPad、Mac 与 Windows 随时离线阅读与查阅代码。</div>
          </div>

          <div class="feature-item">
            <div class="fi-title">🔄 转存后资料永久有效</div>
            <div class="fi-desc">拍下后一键转存至个人网盘永久保存，不用担心链接失效，资料持续享有更新。</div>
          </div>

          <div class="feature-item">
            <div class="fi-title">📂 目录规整分类井然有序</div>
            <div class="fi-desc">拒绝碎片散乱文件，PDF手册、分章MD文档、高清原图、工程源码均已标准化命名。</div>
          </div>

          <div class="feature-item">
            <div class="fi-title">💬 贴心学习与交流支持</div>
            <div class="fi-desc">在下载、打开文件或部署过程中遇到任何疑问，随时可以在小红书私信联系协助。</div>
          </div>
        </div>

        <div class="cta-strip">
          <div class="cs-text">💡 立即拍下，开启你的 AI Agent 商业级落地之旅！</div>
        </div>
      </div>
    `
  }
];

function generateHtml(card) {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  body {
    width: 1080px;
    height: 1440px;
    background: #F8FAFC;
    color: #0F172A;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 64px 68px 50px;
  }

  /* 柔和清爽的背景装饰 (浅蓝/灰白微光，无任何赛博发光) */
  .bg-subtle-top {
    position: absolute;
    top: -120px;
    right: -80px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(219, 234, 254, 0.6) 0%, rgba(248, 250, 252, 0) 70%);
    pointer-events: none;
  }
  .bg-subtle-bottom {
    position: absolute;
    bottom: -100px;
    left: -80px;
    width: 450px;
    height: 450px;
    background: radial-gradient(circle, rgba(241, 245, 249, 0.8) 0%, rgba(248, 250, 252, 0) 70%);
    pointer-events: none;
  }

  /* 顶部状态栏 */
  .top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 10;
  }
  .top-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1D4ED8;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }
  .top-page {
    font-size: 20px;
    font-weight: 800;
    color: #64748B;
    background: #FFFFFF;
    padding: 6px 18px;
    border-radius: 999px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }

  /* 标题区域 */
  .header {
    margin-top: 24px;
    position: relative;
    z-index: 10;
  }
  .header h1 {
    font-size: 50px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.22;
    letter-spacing: -0.5px;
  }
  .header .sub {
    font-size: 25px;
    font-weight: 700;
    color: #2563EB;
    margin-top: 10px;
  }
  .header .desc {
    font-size: 20px;
    color: #64748B;
    margin-top: 8px;
    line-height: 1.5;
  }

  /* 卡片主内容区 */
  .card-body {
    flex: 1;
    margin-top: 26px;
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  /* 底部页脚 */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #E2E8F0;
    padding-top: 20px;
    font-size: 18px;
    color: #64748B;
    font-weight: 500;
    position: relative;
    z-index: 10;
  }
  .footer-left {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #334155;
    font-weight: 600;
  }
  .footer-dot {
    width: 9px;
    height: 9px;
    background: #10B981;
    border-radius: 50%;
  }

  /* ================= 通用清爽组件样式 ================= */

  /* 卡片1: 主图封面 */
  .cover-hero {
    display: flex;
    flex-direction: column;
    gap: 22px;
  }
  .stat-pills {
    display: flex;
    gap: 12px;
  }
  .pill {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    color: #334155;
    padding: 10px 18px;
    border-radius: 12px;
    font-size: 19px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  }
  .pill strong {
    color: #2563EB;
    font-weight: 800;
  }
  .grid-2x2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .clean-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px 22px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  }
  .cc-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }
  .cc-emoji {
    font-size: 28px;
  }
  .cc-title {
    font-size: 22px;
    font-weight: 700;
    color: #0F172A;
  }
  .cc-text {
    font-size: 17.5px;
    color: #475569;
    line-height: 1.55;
  }
  .gift-banner {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .gb-icon {
    font-size: 36px;
  }
  .gb-content {
    flex: 1;
  }
  .gb-title {
    font-size: 20px;
    font-weight: 800;
    color: #1E3A8A;
    margin-bottom: 4px;
  }
  .gb-sub {
    font-size: 17.5px;
    color: #3B82F6;
    font-weight: 600;
  }
  .gb-tag {
    background: #2563EB;
    color: #FFFFFF;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 17px;
    font-weight: 700;
  }

  /* 卡片2: 清单 */
  .list-wrapper {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .clean-row {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  }
  .cr-idx {
    font-size: 20px;
    font-weight: 900;
    color: #2563EB;
    background: #EFF6FF;
    padding: 6px 12px;
    border-radius: 8px;
  }
  .cr-icon {
    font-size: 32px;
  }
  .cr-main {
    flex: 1;
  }
  .cr-title {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 5px;
  }
  .cr-desc {
    font-size: 17.5px;
    color: #475569;
    line-height: 1.5;
  }

  /* 卡片3: 第1~2章 */
  .two-section-layout {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .block-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 24px 26px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  }
  .bc-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 12px;
  }
  .bc-tag {
    color: #FFFFFF;
    padding: 4px 12px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 800;
  }
  .bc-tag.blue { background: #2563EB; }
  .bc-tag.green { background: #059669; }
  .bc-name {
    font-size: 23px;
    font-weight: 800;
    color: #0F172A;
  }
  .point-grid {
    display: flex;
    flex-direction: column;
    gap: 11px;
  }
  .pg-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 18px;
    color: #334155;
    line-height: 1.55;
  }
  .pg-item .bullet {
    background: #EFF6FF;
    color: #2563EB;
    font-weight: 800;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .pg-item strong {
    color: #0F172A;
  }
  .chip-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .step-chip {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 18px;
    color: #1E293B;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .sc-num {
    background: #DCFCE7;
    color: #15803D;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 14px;
  }

  /* 卡片4: 第3章 */
  .arch-clean-box {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .triad-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border: 1px solid #BFDBFE;
    border-radius: 18px;
    padding: 22px 20px;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.06);
  }
  .tf-step {
    flex: 1;
    text-align: center;
    background: #F8FAFC;
    border-radius: 12px;
    padding: 14px 12px;
    border: 1px solid #E2E8F0;
  }
  .tf-step.active {
    background: #EFF6FF;
    border-color: #93C5FD;
  }
  .tf-badge {
    font-size: 19px;
    font-weight: 800;
    color: #1D4ED8;
    margin-bottom: 6px;
  }
  .tf-text {
    font-size: 15px;
    color: #475569;
    line-height: 1.4;
  }
  .tf-arrow {
    font-size: 24px;
    color: #3B82F6;
    font-weight: 800;
    padding: 0 8px;
  }
  .card-column {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .sub-item-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  }
  .sic-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
  }
  .sic-icon {
    font-size: 22px;
  }
  .sic-title {
    font-size: 21px;
    font-weight: 800;
    color: #0F172A;
  }
  .sic-body {
    font-size: 17.5px;
    color: #475569;
    line-height: 1.55;
  }

  /* 卡片5: 第4章 */
  .grid-2x2-clean {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
  }
  .clean-tech-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 22px 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .ctc-top {
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 8px;
  }
  .ctc-tag {
    background: #EFF6FF;
    color: #2563EB;
    font-size: 15px;
    font-weight: 900;
    padding: 3px 8px;
    border-radius: 6px;
  }
  .ctc-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
  }
  .ctc-content {
    font-size: 17px;
    color: #475569;
    line-height: 1.6;
  }

  /* 卡片6: 第5章 */
  .frame-column {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .frame-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  }
  .fb-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
  }
  .fb-badge {
    color: #FFFFFF;
    font-size: 15px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 6px;
  }
  .fb-badge.dify { background: #2563EB; }
  .fb-badge.lg { background: #4F46E5; }
  .fb-badge.eino { background: #059669; }
  .fb-badge.auto { background: #D97706; }
  .fb-title {
    font-size: 21px;
    font-weight: 800;
    color: #0F172A;
  }
  .fb-note {
    font-size: 15px;
    color: #64748B;
    margin-left: auto;
  }
  .fb-desc {
    font-size: 17.5px;
    color: #475569;
    line-height: 1.55;
  }

  /* 卡片7: 第6章 */
  .case-column {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .case-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
  }
  .cc-badge {
    display: inline-block;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 6px;
    margin-bottom: 8px;
  }
  .cc-badge.orange { background: #D97706; }
  .cc-badge.blue { background: #2563EB; }
  .cc-badge.green { background: #059669; }
  .cc-title {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 10px;
  }
  .cc-points {
    display: flex;
    flex-direction: column;
    gap: 6px;
    font-size: 17.5px;
    color: #475569;
    line-height: 1.55;
  }

  /* 卡片8: 第7章 */
  .interview-column {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .white-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
  }
  .wb-head {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 8px;
  }
  .wb-icon {
    font-size: 24px;
  }
  .wb-title {
    font-size: 21px;
    font-weight: 800;
    color: #0F172A;
  }
  .wb-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 17.5px;
    color: #475569;
    line-height: 1.55;
  }

  /* 卡片9: 下单说明 */
  .delivery-wrapper {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .main-notice-box {
    background: #EFF6FF;
    border: 2px solid #BFDBFE;
    border-radius: 20px;
    padding: 28px 24px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);
  }
  .mnb-icon {
    font-size: 44px;
    margin-bottom: 6px;
  }
  .mnb-title {
    font-size: 32px;
    font-weight: 900;
    color: #1E3A8A;
    margin-bottom: 6px;
  }
  .mnb-sub {
    font-size: 21px;
    color: #2563EB;
    font-weight: 700;
  }
  .two-by-two {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .feature-item {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 20px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
  }
  .fi-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 6px;
  }
  .fi-desc {
    font-size: 16.5px;
    color: #475569;
    line-height: 1.5;
  }
  .cta-strip {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
  }
  .cs-text {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
  }
</style>
</head>
<body>
  <div class="bg-subtle-top"></div>
  <div class="bg-subtle-bottom"></div>

  <div class="top-bar">
    <div class="top-badge">${card.badge}</div>
    <div class="top-page">${card.pageIndex}</div>
  </div>

  <div class="header">
    <h1>${card.title}</h1>
    <div class="sub">${card.subtitle}</div>
    <div class="desc">${card.desc}</div>
  </div>

  <div class="card-body">
    ${card.contentHtml}
  </div>

  <div class="footer">
    <div class="footer-left">
      <span class="footer-dot"></span>
      <span>AI Agent 全栈开发与商业落地工程实操手册</span>
    </div>
    <div class="footer-right">
      <span>百度网盘 / 夸克网盘 极速秒发</span>
    </div>
  </div>
</body>
</html>`;
}

async function main() {
  console.log('🚀 正在启动 Google Chrome 渲染 9 张清爽明亮风小红书卡片...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1440 },
    deviceScaleFactor: 2 // 2倍超采样渲染
  });

  const page = await context.newPage();

  for (let i = 0; i < cards.length; i++) {
    const card = cards[i];
    const html = generateHtml(card);
    const htmlPath = path.join(outputDir, `temp_clean_${i + 1}.html`);
    const imgPath = path.join(outputDir, card.filename);

    await fs.writeFile(htmlPath, html, 'utf-8');
    await page.goto('file://' + htmlPath, { waitUntil: 'load' });
    await page.screenshot({ path: imgPath, type: 'png' });
    await fs.unlink(htmlPath);

    console.log(`✅ [${i + 1}/9] 成功生成清爽版: ${card.filename}`);
  }

  await browser.close();
  console.log('\n🎉 全部 9 张清爽明亮版小红书展示图已生成完成！');
}

main().catch(err => {
  console.error('❌ 生成失败:', err);
  process.exit(1);
});
