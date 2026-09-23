import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    title: "AI Agent 全栈开发与商业落地教程",
    description: "从 0 到 1 打造可交付、高可用的企业级智能体系统（商业交付版）",
    head: [
      ['link', { rel: 'icon', href: '/favicon.ico' }],
      ['style', {}, `
        /* 彻底解决 VitePress 默认段落样式对 Mermaid 图内文字的挤压遮挡 */
        .vp-doc .mermaid {
          display: flex;
          justify-content: center;
          margin: 28px 0;
          overflow-x: auto;
        }
        .vp-doc .mermaid svg {
          max-width: 100%;
          height: auto;
          overflow: visible !important;
        }
        .vp-doc .mermaid svg foreignObject {
          overflow: visible !important;
        }
        .vp-doc .mermaid svg foreignObject div {
          overflow: visible !important;
        }
        .vp-doc .mermaid svg foreignObject p,
        .vp-doc .mermaid svg .nodeLabel p,
        .vp-doc .mermaid svg .edgeLabel p,
        .vp-doc .mermaid svg .cluster-label p {
          margin: 0 !important;
          padding: 0 !important;
          line-height: 1.35 !important;
        }
        .vp-doc .mermaid svg .label {
          line-height: 1.35 !important;
        }
        /* 宣传海报推荐容器样式 */
        .poster-recommend-card {
          margin: 32px 0;
          padding: 24px;
          border-radius: 16px;
          background: linear-gradient(135deg, rgba(59, 130, 246, 0.05), rgba(147, 51, 234, 0.05));
          border: 1px solid var(--vp-c-divider);
          text-align: center;
        }
        .poster-recommend-card h3 {
          margin-top: 0 !important;
          margin-bottom: 8px !important;
          font-size: 1.3rem;
          font-weight: 700;
          color: var(--vp-c-brand-1);
        }
        .poster-recommend-card p {
          margin: 4px 0 16px 0 !important;
          color: var(--vp-c-text-2);
          font-size: 0.95rem;
        }
        .poster-image-wrapper {
          display: flex;
          justify-content: center;
          margin-top: 16px;
        }
        .poster-image-wrapper img {
          max-width: 680px;
          width: 100%;
          border-radius: 12px;
          box-shadow: 0 12px 36px rgba(0, 0, 0, 0.12);
          border: 1px solid var(--vp-c-divider);
          transition: transform 0.25s ease, box-shadow 0.25s ease;
        }
        .poster-image-wrapper img:hover {
          transform: translateY(-4px);
          box-shadow: 0 16px 44px rgba(0, 0, 0, 0.18);
        }
      `]
    ],
    markdown: {
      lineNumbers: true
    },
    mermaid: {
      theme: 'neutral',
      securityLevel: 'loose',
      flowchart: {
        htmlLabels: true,
        padding: 15
      }
    },
    themeConfig: {
      nav: [
        { text: '首页', link: '/' },
        { text: '教程正文', link: '/guide/01-mindset' },
        { text: '附录速查', link: '/guide/09-appendix' }
      ],
      sidebar: {
        '/guide/': [
          {
            text: '系统章节大纲',
            items: [
              { text: '第一章：心法与认知篇', link: '/guide/01-mindset' },
              { text: '第二章：路线图篇 (14步全景)', link: '/guide/02-roadmap' },
              { text: '第三章：架构与核心理论篇', link: '/guide/03-core-theory' },
              { text: '第四章：关键技术底座篇', link: '/guide/04-tech-foundations' },
              { text: '第五章：工业级混合 RAG 管道篇', link: '/guide/05-rag-pipeline' },
              { text: '第六章：现代编排框架篇', link: '/guide/06-frameworks' },
              { text: '第七章：企业商业实战案例篇', link: '/guide/07-enterprise-cases' },
              { text: '第八章：生产高可用与求职面试篇', link: '/guide/08-production-career' },
              { text: '附录：工程命令速查与术语表', link: '/guide/09-appendix' }
            ]
          }
        ]
      },
      socialLinks: [
        { icon: 'github', link: 'https://github.com/zackzhangkai/ai-agent-tutorial' }
      ],
      footer: {
        message: '商业实战出版级教程 | 严禁未授权翻印传播',
        copyright: 'Copyright © 2026 AI Agent 实战教程'
      }
    }
  })
)
