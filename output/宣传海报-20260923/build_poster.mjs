import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire('/Users/zack/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/');
const { chromium } = require('playwright');
const sharp = require('sharp');
const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(dir, '../..');
const assets = {
  personal: '/Users/zack/Documents/Obsidian/01 个人核心档案/个人微信二维码',
  group: '/Users/zack/Documents/Obsidian/01 个人核心档案/AI技术交流群图片',
};
const images = Object.fromEntries(await Promise.all(Object.entries(assets).map(async ([key, value]) => [key, 'data:image/jpeg;base64,' + (await fs.readFile(value)).toString('base64')])));
const esc = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const route = [
  ['Python 与工程环境', '语法 / 函数 / OOP / 文件 IO / 异步编程<br>typing、Pydantic 校验；uv / poetry 依赖管理'],
  ['FastAPI 服务与模型接入', '前后端交互 / REST API / 路由与中间件<br>SSE 流式输出、CORS、错误兜底与效果验证'],
  ['Transformer 与 LLM API', 'Self-Attention / Encoder-Decoder / KV Cache<br>BPE 分词、Token 计量、生成参数与模型 SDK'],
  ['Prompt 与上下文控制', '角色、目标、约束、Few-shot、CoT<br>JSON 结构化输出、Pydantic、Prompt Cache'],
  ['RAG 知识检索增强', '文档解析 / 清洗 / 字符、语义与父子分块<br>Embedding、相似度、向量库、混合检索与重排'],
  ['Tool Calling 与 MCP', 'Function Calling / 工具 Schema / 本地执行闭环<br>MCP Server、Client-Server、工具与资源连接'],
  ['LangChain 与 LangGraph', 'PromptTemplate / ChatModel / OutputParser / LCEL<br>State、Node、Edge、条件分支与多 Agent 协作'],
  ['Agent Workflow 实战', 'Router 分流 / 多工具协同 / 并行调用<br>最大轮次、重试降级、熔断与人工确认'],
  ['AI Coding 开发与联调', 'Cursor / GitHub Copilot / Claude Code<br>代码 Review、单元测试、模糊测试与提示注入'],
  ['Skills 技能封装与复用', '封装代码、提示词、参考资源与执行脚本<br>按需渐进加载、跨 Agent 共享、复杂任务拆解'],
  ['开源架构与 Agent Harness', 'Hermes / PI Agent / OpenClaw / OpenManus<br>事件循环、Docker 沙箱、轨迹日志与评测基准'],
  ['企业项目与算法问答', '客服 / 医疗 / 金融研报等场景的架构设计<br>RAG 退化、幻觉、小模型分工、准确率与延迟'],
  ['简历与模拟面试', 'STAR 项目表达、真实量化成果与项目深挖<br>模拟技术面、系统设计面、综合面'],
  ['面试复盘与 Offer 选择', '问题总结、查缺补漏、薪资与岗位分析<br>业务场景、资源支持、团队技术栈与入职准备'],
];
const principles = [
  ['1.1', '找准问题', '一次性需求与高频流程'],
  ['1.2', '拆解任务', '单节点打磨与流程串联'],
  ['1.3', '善用工具', '平台选型与组件复用'],
  ['1.4', '迭代提示词', '测试集、Bad Case 与版本'],
  ['1.5', '从自用起步', '知识库、资讯与代码助手'],
];
const detail = (id, title, text) => `<div class="detail" data-coverage="${id}"><b>${title}</b><p>${text}</p></div>`;
const html = `<!doctype html><html lang="zh-CN"><head><meta charset="UTF-8"><title>AI Agent 学习全景 · Zack</title><style>
*{box-sizing:border-box}html,body{margin:0;padding:0}body{width:1200px;color:#182b41;background:#f5f3ec;font-family:"PingFang SC","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}p,h1,h2,h3{margin:0}.poster{width:1200px;padding:48px 58px 40px;position:relative;overflow:hidden}.masthead{display:flex;justify-content:space-between;align-items:center;padding-bottom:24px;border-bottom:1px solid #c9cec9;font-size:19px;letter-spacing:1.5px}.brand{font-weight:700}.brand i{display:inline-block;width:11px;height:11px;background:#2654df;border-radius:50%;margin-right:10px}.edition{color:#6a7580;font-size:16px}.hero{padding:40px 0 28px;position:relative}.hero:after{content:"";position:absolute;width:214px;height:214px;right:-31px;top:61px;border:1px solid #b9c6e6;border-radius:50%;box-shadow:0 0 0 27px #f5f3ec,0 0 0 28px #ccd5e7,0 0 0 56px #f5f3ec,0 0 0 57px #dee3eb;z-index:0}.hero>*{position:relative;z-index:1}.eyebrow{font-size:18px;font-weight:600;letter-spacing:3px;color:#2954cf;margin-bottom:13px}h1{font-size:102px;line-height:1.06;letter-spacing:-4px;font-weight:800}.headline{font-size:61px;line-height:1.35;letter-spacing:1px;font-weight:700;color:#2754da;margin:8px 0 17px}.subhead{font-size:23px;line-height:1.6;color:#536474}.stats{margin-top:30px;display:flex;align-items:center;gap:0;border-top:1px solid #c9cec9;border-bottom:1px solid #c9cec9;padding:19px 0}.stat{display:flex;align-items:baseline;gap:12px;padding:0 34px;border-right:1px solid #c9cec9}.stat:first-child{padding-left:0}.stat:last-child{border:0}.stat strong{font-size:37px;letter-spacing:-1px;color:#2654df}.stat span{font-size:20px}.sect{margin-top:34px}.sect-title{display:flex;align-items:center;gap:13px;margin-bottom:18px}.sect-title .num{font-size:17px;font-weight:700;letter-spacing:1px;background:#2754da;color:white;padding:6px 9px;border-radius:4px}.sect-title h2{font-size:31px;letter-spacing:1px;font-weight:700}.sect-title .note{margin-left:auto;font-size:16px;color:#647180}.principles{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid #c9d1d3;background:#fffef9;border-radius:12px;padding:23px 8px}.principle{padding:0 15px;border-right:1px solid #dbe0de}.principle:last-child{border:0}.principle strong{font-size:24px;display:block;color:#243e65;margin-bottom:10px}.principle p{font-size:18px;line-height:1.65;color:#65717a}.roadmap{background:#fffef9;border:1px solid #c9d1d3;border-radius:12px;display:grid;grid-template-columns:1fr 1fr;padding:6px 24px}.step{display:flex;gap:14px;min-height:111px;padding:18px 0;border-bottom:1px solid #e1e4e0}.step:nth-child(odd){padding-right:21px;border-right:1px solid #e1e4e0}.step:nth-child(even){padding-left:22px}.step:nth-last-child(-n+2){border-bottom:0}.stepno{font-size:17px;flex-shrink:0;color:#2754da;font-weight:700;width:29px;padding-top:5px}.step h3{font-size:24px;line-height:1.3;font-weight:700;margin-bottom:7px;color:#1e365a}.step p{font-size:17.7px;line-height:1.7;color:#526474;white-space:nowrap}.twocol{display:grid;grid-template-columns:1fr 1fr;gap:24px}.panel{border-top:3px solid #2754da;background:#eaf0f7;border-radius:0 0 12px 12px;padding:5px 24px 19px}.detail{padding:15px 0 13px;border-bottom:1px solid #cfd9e5}.detail:last-child{border:0;padding-bottom:0}.detail b{display:block;font-size:22px;line-height:1.4;color:#1d375a;margin-bottom:5px}.detail p{font-size:18.5px;line-height:1.75;color:#4c6074}.principle12{font-size:17.5px!important;line-height:1.8!important}.eco{display:grid;grid-template-columns:1fr 1fr;column-gap:32px;background:#fffef9;border:1px solid #c9d1d3;border-radius:12px;padding:7px 25px 19px}.eco .detail:nth-last-child(-n+2){border:0}.cases{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.case{background:#e9eee8;padding:25px 22px;border-radius:12px;border-top:3px solid #789482}.case .tag{font-size:14px;letter-spacing:2px;color:#687c6d;margin-bottom:11px}.case h3{font-size:25px;line-height:1.45;color:#263f32;margin-bottom:11px}.case p{font-size:19px;line-height:1.8;color:#536959}.jobs{display:grid;grid-template-columns:1fr 1fr;gap:0 32px;border-top:1px solid #c9d1d3;border-bottom:1px solid #c9d1d3;padding:4px 0 17px}.jobs .detail:nth-last-child(-n+2){border:0}.join{margin-top:38px;background:#17304f;margin-left:-58px;margin-right:-58px;padding:35px 58px 30px;color:#fff}.join-top{display:flex;justify-content:space-between;align-items:end;margin-bottom:25px}.join h2{font-size:35px;line-height:1.4;letter-spacing:1px}.join .join-note{font-size:18px;color:#c4cfdf;line-height:1.8;text-align:right}.qr-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}.qr-card{background:white;border-radius:13px;overflow:hidden;color:#182b41}.qr-label{padding:22px 24px 0;display:flex;align-items:center;justify-content:space-between}.qr-label h3{font-size:25px}.qr-label span{font-size:16px;color:#566c87}.qr-original{display:block;width:100%;height:756px;object-fit:contain;object-position:center;background:#fff}.qr-caption{text-align:center;border-top:1px solid #e5e9ed;font-size:19px;padding:15px 8px 19px;line-height:1.5}.qr-caption em{font-style:normal;color:#a75e24}.expiry{font-size:17px;line-height:1.7;color:#c4cfdf;text-align:center;margin-top:19px}.footer{display:flex;justify-content:space-between;margin-top:24px;font-size:15px;color:#78838a;letter-spacing:1px}
</style></head><body><main class="poster">
<div class="masthead"><div class="brand"><i></i>ZACK · AI 学习交流圈</div><div class="edition">学习资料 · 知识全景</div></div>
<header class="hero"><div class="eyebrow">从第一行代码，到完整的智能体应用</div><h1>AI Agent</h1><div class="headline">全栈开发与实战学习</div><p class="subhead">把知识串成体系，把想法做成项目。<br>认知入门 · 技术架构 · 商业案例 · 工程实践 · 求职进阶</p>
<div class="stats"><div class="stat"><strong>7</strong><span>大学习模块</span></div><div class="stat"><strong>14</strong><span>步进阶路线</span></div><div class="stat"><strong>3</strong><span>类项目案例</span></div></div></header>
<section class="sect" data-module="1"><div class="sect-title"><span class="num">01</span><h2>先建立正确的 Agent 认知</h2><span class="note">五大底层逻辑</span></div><div class="principles">${principles.map(([id,title,text])=>`<div class="principle" data-coverage="${id}"><strong>${title}</strong><p>${text}</p></div>`).join('')}</div></section>
<section class="sect" data-module="2" data-coverage="2.1 2.2"><div class="sect-title"><span class="num">02</span><h2>14 步开发与就业进阶路线</h2><span class="note">从基础到项目，按序学习</span></div><div class="roadmap">${route.map(([title,text],i)=>`<article class="step" data-step="${i+1}"><span class="stepno">${String(i+1).padStart(2,'0')}</span><div><h3>${title}</h3><p>${text}</p></div></article>`).join('')}</div></section>
<div class="twocol">
<section class="sect" data-module="3"><div class="sect-title"><span class="num">03</span><h2>架构与核心理论</h2></div><div class="panel">
${detail('3.1','感知 → 规划与记忆 → 行动','文本 / ASR / OCR / 事件输入；任务拆解、自我反思、动态路由；短期上下文、长期向量库与知识图谱；工具、代码与浏览器执行。')}
${detail('3.2','电商智能助手的完整决策链','从用户意图、订单与商品查询，到真实工具结果回传、答案整合和业务反馈。')}
${detail('3.3','规划范式与推理循环','ReAct：思考、行动、观察的循环；Deep Research：Think → Search → Summary。')}
${detail('3.4','工程设计：资料中的 12 项原则','<span class="principle12">代码版本化 / 显式依赖 / 配置外置 / 工具服务化 / 构建发布运行分离 / 无状态进程 / 端口与流式接口 / 图状态并发 / 快速启动与优雅退出 / 环境一致 / 全链路日志 / 独立管理任务</span>')}
</div></section>
<section class="sect" data-module="4"><div class="sect-title"><span class="num">04</span><h2>关键技术底座</h2></div><div class="panel">
${detail('4.1','结构化输出与 Prompt Cache','JSON Schema / Pydantic；静态提示词前置、动态内容后置；缓存命中、Token 成本与延迟。')}
${detail('4.2','工业级 RAG 检索流水线','清洗与分块 → Embedding → BM25 + 向量混合检索 → RRF 融合 → BGE / Cohere 重排；Chroma / Qdrant / Milvus，Top-K 与阈值配置。')}
${detail('4.3','Function Calling 原生执行闭环','定义工具 Schema → 模型生成调用参数 → 本地执行 → 回传工具结果 → 整合回答。')}
${detail('4.4','MCP 的工具与上下文连接','Host / Client / Server；JSON-RPC；Tools、Resources、Prompts；数据库、Git 与文件系统接入。')}
${detail('4.5','微调与传统分类模型融合','XTuner / LLaMA-Factory、ShareGPT / Function 数据格式；BERT、BiLSTM、CRF、NER 与意图分流。')}
</div></section>
</div>
<section class="sect" data-module="5"><div class="sect-title"><span class="num">05</span><h2>主流编排框架与开源生态</h2><span class="note">平台搭建 → 代码编排 → 源码阅读</span></div><div class="eco">
${detail('5.1','Dify / Coze：低代码应用搭建','知识库、插件与 OpenAPI 工具、Chatflow 条件 / 代码 / 迭代节点；日志监控与 Web / API 集成。')}
${detail('5.2','LangChain / LangGraph：状态图编排','共享状态、节点、条件边、循环与多 Agent 协同；工具路由、回环执行与完整代码示例。')}
${detail('5.3','Eino：Go 语言 Agent 框架','Model / Prompt / Tool / Retriever 组件抽象；图编排、高并发、限流、熔断与链路追踪。')}
${detail('5.4','AutoGPT / BabyAGI / SuperAGI / Qwen-Agent','多目标自动化；任务执行、创建与优先级循环；记忆、工具注册、约束与迭代上限。')}
</div></section>
<section class="sect" data-module="6"><div class="sect-title"><span class="num">06</span><h2>三类项目案例，连接真实业务问题</h2></div><div class="cases">
<article class="case" data-coverage="6.1"><div class="tag">CASE 01 · 企业服务</div><h3>高可用智能客服</h3><p>预处理与意图识别<br>NER 槽位抽取与 DST<br>多轮状态、指代与话题切换<br>RAG / 任务 / 澄清三路分流<br>安全过滤、人工接管与反馈</p></article>
<article class="case" data-coverage="6.2"><div class="tag">CASE 02 · 电商应用</div><h3>Dify 电商助手</h3><p>售后政策与 FAQ 梳理<br>知识库导入、切分与索引<br>混合检索与重排序配置<br>订单工具、Chatflow 编排<br>业务 Prompt 与回复约束</p></article>
<article class="case" data-coverage="6.3"><div class="tag">CASE 03 · 多模态应用</div><h3>医疗问诊流程案例</h3><p>语音 / 文本 / 图片输入<br>ASR、OCR 与医学知识图谱<br>场景 → 专科 → 语义消歧<br>患者画像与动态工作流<br>风险分流与人工兜底设计</p></article>
</div></section>
<section class="sect" data-module="7"><div class="sect-title"><span class="num">07</span><h2>工程化能力与求职进阶</h2></div><div class="jobs">
${detail('7.1','高频工程问题与容错策略','幻觉与事实引用、输出约束、Guardrails；长上下文退化、滚动摘要、动态剪枝；重复工具调用、最大轮次、异常重试与熔断。')}
${detail('7.2','评估体系与线上可观测性','离线评测 / 在线监控；意图准确率、工具 Precision / Recall、槽位 F1、任务完成率、TTFT / 全链路延迟、人工接管率；AgentBench / SWE-bench / GAIA。')}
${detail('7.3','STAR 项目表达与成果呈现','从业务背景、任务挑战、技术行动到真实结果；梳理架构选型、检索优化、成本与体验指标，形成可解释、可验证的项目经历。')}
${detail('7.4','模拟面试与高频问题拆解','为何拆成多节点 / 多 Agent？Function Calling 如何执行？为什么混合检索优于仅向量检索？覆盖项目深挖、系统设计与复盘。')}
</div></section>
<section class="join"><div class="join-top"><h2>一起学，一起把 Agent 做出来。</h2><div class="join-note">添加微信，交流学习资料<br>加入群聊，讨论问题与实战经验</div></div><div class="qr-grid">
<article class="qr-card"><div class="qr-label"><h3>添加 Zack</h3><span>个人微信</span></div><img class="qr-original" src="${images.personal}" alt="Zack 个人微信二维码原图"><div class="qr-caption">微信扫一扫 / 长按识别<br><em>备注「AI Agent」，方便交流</em></div></article>
<article class="qr-card"><div class="qr-label"><h3>AI 学习交流圈</h3><span>微信群聊</span></div><img class="qr-original" src="${images.group}" alt="AI 学习交流圈群二维码原图"><div class="qr-caption">微信扫一扫 / 长按识别<br><em>和同路人一起交流学习</em></div></article>
</div><p class="expiry">群二维码原图标注：9 月 30 日前有效。若已失效，可添加左侧个人微信联系。</p></section>
<footer class="footer"><span>ZACK · AI AGENT LEARNING</span><span>知识目录依据本地学习资料整理 · 2026.09</span></footer>
</main></body></html>`;

const output = path.join(dir, 'AI_Agent_全知识点双二维码宣传海报');
await fs.writeFile(output + '.html', html);
const browser = await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
try {
  const page = await browser.newPage({viewport:{width:1200,height:1000},deviceScaleFactor:2});
  await page.goto('file://' + output + '.html');
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));});
  const geometry = await page.evaluate(()=>({
    width:document.body.scrollWidth,height:document.body.scrollHeight,
    modules:[...document.querySelectorAll('[data-module]')].map(x=>x.dataset.module),
    steps:[...document.querySelectorAll('[data-step]')].map(x=>x.dataset.step),
    coverage:[...document.querySelectorAll('[data-coverage]')].flatMap(x=>x.dataset.coverage.split(' ')),
    images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight})),
    textOverflow:[...document.querySelectorAll('p,h1,h2,h3,.detail,.step')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent.slice(0,100)),
  }));
  const source = await fs.readFile(path.join(root,'AI_Agent_全栈开发与商业落地教程_完整版.md'),'utf8');
  const expected = [...source.matchAll(/^## (\d\.\d) /gm)].map(m=>m[1]);
  const missing = expected.filter(id=>!geometry.coverage.includes(id));
  if(missing.length || geometry.modules.length!==7 || geometry.steps.length!==14 || geometry.textOverflow.length || geometry.width!==1200 || geometry.images.some(x=>!x.loaded)) throw new Error(JSON.stringify({missing,...geometry}));
  await page.screenshot({path:output+'.png',fullPage:true});
  await sharp(output+'.png').jpeg({quality:94,chromaSubsampling:'4:4:4'}).toFile(output+'.jpg');
  const meta=await sharp(output+'.png').metadata();
  console.log(JSON.stringify({output:output+'.png',dimensions:[meta.width,meta.height],modules:geometry.modules.length,steps:geometry.steps.length,subsectionsCovered:expected.length,missing,textOverflow:geometry.textOverflow,sourceImages:geometry.images},null,2));
} finally {await browser.close();}
