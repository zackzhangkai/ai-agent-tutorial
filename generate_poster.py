import subprocess
import os

with open('avatar_b64.txt', 'r') as f:
    avatar_b64 = f.read().strip()
with open('qr_b64.txt', 'r') as f:
    qr_b64 = f.read().strip()

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>AI Agent 引流获客海报</title>
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}
  body {{
    width: 1080px;
    height: 1920px;
    background: #080C16;
    color: #FFFFFF;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 64px 56px 48px 56px;
  }}

  /* Ambient Glows */
  .bg-glow-top {{
    position: absolute;
    top: -160px;
    left: 50%;
    transform: translateX(-50%);
    width: 900px;
    height: 750px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, rgba(8, 12, 22, 0) 70%);
    pointer-events: none;
  }}
  .bg-glow-orange {{
    position: absolute;
    bottom: 220px;
    right: -100px;
    width: 650px;
    height: 650px;
    background: radial-gradient(circle, rgba(249, 115, 22, 0.20) 0%, rgba(8, 12, 22, 0) 70%);
    pointer-events: none;
  }}
  .bg-glow-purple {{
    position: absolute;
    top: 480px;
    left: -150px;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, rgba(8, 12, 22, 0) 70%);
    pointer-events: none;
  }}

  /* Grid overlay */
  .grid-pattern {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255, 255, 255, 0.08) 1.2px, transparent 1.2px);
    background-size: 34px 34px;
    pointer-events: none;
  }}

  /* Header Section */
  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    z-index: 2;
  }}
  .author-badge {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.14);
    backdrop-filter: blur(16px);
    padding: 10px 24px 10px 12px;
    border-radius: 50px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  }}
  .avatar-img {{
    width: 70px;
    height: 70px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #38BDF8;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.5);
  }}
  .author-info {{
    display: flex;
    flex-direction: column;
  }}
  .author-name {{
    font-size: 24px;
    font-weight: 700;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .author-tag {{
    font-size: 16px;
    color: #94A3B8;
  }}
  .top-pill {{
    background: linear-gradient(135deg, rgba(249, 115, 22, 0.25), rgba(239, 68, 68, 0.25));
    border: 1px solid rgba(249, 115, 22, 0.5);
    color: #FB923C;
    font-size: 18px;
    font-weight: 700;
    padding: 12px 24px;
    border-radius: 30px;
    letter-spacing: 1px;
    box-shadow: 0 0 20px rgba(249, 115, 22, 0.2);
  }}

  /* Hero Main Title */
  .hero-section {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 10px 0;
  }}
  .tag-release {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(90deg, #0EA5E9, #6366F1);
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 800;
    padding: 8px 24px;
    border-radius: 20px;
    letter-spacing: 2px;
    box-shadow: 0 4px 25px rgba(14, 165, 233, 0.45);
    margin-bottom: 22px;
  }}
  .main-title {{
    font-size: 62px;
    font-weight: 900;
    line-height: 1.18;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #FFFFFF 15%, #E2E8F0 50%, #38BDF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
  }}
  .title-highlight {{
    background: linear-gradient(135deg, #FF7A00 0%, #FFB800 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .subtitle {{
    font-size: 22px;
    color: #94A3B8;
    font-weight: 400;
    letter-spacing: 1px;
  }}

  /* Feature Grid */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
    position: relative;
    z-index: 2;
  }}
  .feature-card {{
    background: rgba(18, 26, 43, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 22px;
    padding: 24px 24px;
    backdrop-filter: blur(18px);
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  }}
  .card-top {{
    display: flex;
    align-items: center;
    gap: 14px;
  }}
  .card-icon {{
    font-size: 30px;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.12);
  }}
  .card-title {{
    font-size: 21px;
    font-weight: 700;
    color: #F8FAFC;
  }}
  .card-desc {{
    font-size: 15.5px;
    line-height: 1.5;
    color: #94A3B8;
  }}
  .highlight-tag {{
    color: #38BDF8;
    font-weight: 600;
  }}

  /* Bottom Conversion Card */
  .cta-container {{
    background: linear-gradient(135deg, rgba(26, 36, 56, 0.92) 0%, rgba(13, 20, 36, 0.98) 100%);
    border: 2.5px solid #F97316;
    border-radius: 30px;
    padding: 30px 36px;
    box-shadow: 0 0 45px rgba(249, 115, 22, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 30px;
    position: relative;
    z-index: 2;
  }}
  .cta-left {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .cta-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    align-self: flex-start;
    background: linear-gradient(90deg, #F97316, #EA580C);
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 800;
    padding: 6px 18px;
    border-radius: 30px;
    letter-spacing: 1px;
    box-shadow: 0 2px 12px rgba(249, 115, 22, 0.4);
  }}
  .cta-instruction {{
    font-size: 26px;
    font-weight: 800;
    line-height: 1.35;
    color: #FFFFFF;
    letter-spacing: 0.5px;
  }}
  .cta-keyword {{
    color: #FEF08A;
    background: rgba(234, 179, 8, 0.22);
    padding: 2px 12px;
    border-radius: 8px;
    border: 1.5px solid rgba(250, 204, 21, 0.6);
    display: inline-block;
    margin: 4px 0;
    font-size: 28px;
  }}
  .cta-tips {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .tip-item {{
    font-size: 15.5px;
    color: #CBD5E1;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .tip-dot {{
    width: 7px;
    height: 7px;
    background: #38BDF8;
    border-radius: 50%;
    box-shadow: 0 0 8px #38BDF8;
    flex-shrink: 0;
  }}

  /* QR Box */
  .qr-box {{
    background: #FFFFFF;
    border-radius: 22px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6);
    flex-shrink: 0;
  }}
  .qr-img {{
    width: 215px;
    height: 215px;
    border-radius: 14px;
    display: block;
  }}
  .qr-label {{
    font-size: 14.5px;
    font-weight: 700;
    color: #334155;
    letter-spacing: 0.5px;
  }}

  /* Footer */
  .footer-note {{
    text-align: center;
    font-size: 14.5px;
    color: #64748B;
    position: relative;
    z-index: 2;
  }}
</style>
</head>
<body>
  <div class="bg-glow-top"></div>
  <div class="bg-glow-orange"></div>
  <div class="bg-glow-purple"></div>
  <div class="grid-pattern"></div>

  <!-- Header -->
  <div class="header">
    <div class="author-badge">
      <img class="avatar-img" src="data:image/jpeg;base64,{avatar_b64}" alt="Zack">
      <div class="author-info">
        <div class="author-name">Zack <span style="color:#38BDF8;font-size:18px;">✓</span></div>
        <div class="author-tag">AI Agent 全栈践行者 · 资深架构师</div>
      </div>
    </div>
    <div class="top-pill">🎁 独家资料 · 免费获取</div>
  </div>

  <!-- Hero Section -->
  <div class="hero-section">
    <div class="tag-release">⚡️ 2026 工业级交付指南</div>
    <h1 class="main-title">AI Agent 全栈开发<br><span class="title-highlight">商业落地与求职宝典</span></h1>
    <p class="subtitle">14步就业成长树 · 关键技术底座 · 3大商用案例源码 · 算法八股梳理</p>
  </div>

  <!-- Value Highlights (6 Cards) -->
  <div class="cards-grid">
    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">🗺️</div>
        <div class="card-title">14 步就业进阶全景路线</div>
      </div>
      <div class="card-desc">涵盖 Python/FastAPI、Transformer、RAG、Tool Calling、LangGraph 状态图与 AI Coding 实战。</div>
    </div>

    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">🧠</div>
        <div class="card-title">经典 Agent 决策体系</div>
      </div>
      <div class="card-desc">深入拆解 <span class="highlight-tag">感知-规划-行动</span> 三元组、短期与长期记忆机制、ReAct 循环与 12-Factor Agents 原则。</div>
    </div>

    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">⚙️</div>
        <div class="card-title">关键技术底座全量源码</div>
      </div>
      <div class="card-desc">Prompt Cache 降本 80%、混合 RAG、OpenAI Function Calling 原生 Python 闭环与轻量 BERT 分类器。</div>
    </div>

    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">🏢</div>
        <div class="card-title">3 大企业级商用案例</div>
      </div>
      <div class="card-desc">千万级智能客服已交付系统架构（DST+三路分流）、Dify 电商助手、医疗智能多模态问诊三级消歧系统。</div>
    </div>

    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">🎯</div>
        <div class="card-title">算法八股与求职面试</div>
      </div>
      <div class="card-desc">防死循环熔断器代码、科学评测指标体系、STAR 法则高分简历包装模板与大厂真题高分回答标准。</div>
    </div>

    <div class="feature-card">
      <div class="card-top">
        <div class="card-icon">📑</div>
        <div class="card-title">飞书在线知识库专属权限</div>
      </div>
      <div class="card-desc">随时在手机/电脑阅读体系化文档，内嵌全套高清架构原图与代码示例，持续同步更新！</div>
    </div>
  </div>

  <!-- Bottom CTA Conversion Box -->
  <div class="cta-container">
    <div class="cta-left">
      <div class="cta-badge">🔥 核心资料免费领</div>
      <div class="cta-instruction">
        加我的微信即可获取这些资料<br>
        备注 <span class="cta-keyword">AI Agent</span> 即可
      </div>
      <div class="cta-tips">
        <div class="tip-item"><span class="tip-dot"></span> 扫码添加好友后，立即发送专属飞书知识库链接</div>
        <div class="tip-item"><span class="tip-dot"></span> 赠送全套 Python 源码、案例架构图与面试真题解析</div>
      </div>
    </div>

    <div class="qr-box">
      <img class="qr-img" src="data:image/jpeg;base64,{qr_b64}" alt="微信二维码">
      <div class="qr-label">长按或扫一扫添加微信</div>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer-note">
    持续输出高质量 AI Agent 实战内容 · 让我们一起走在智能体技术最前沿
  </div>
</body>
</html>
"""

with open('poster.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("poster.html updated successfully!")
