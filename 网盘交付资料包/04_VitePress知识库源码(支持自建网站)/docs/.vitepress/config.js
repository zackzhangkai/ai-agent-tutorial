import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "AI Agent 全栈开发与商业落地教程",
  description: "从 0 到 1 打造可交付、高可用的企业级智能体系统（商业交付版）",
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  markdown: {
    lineNumbers: true
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
      { icon: 'github', link: 'https://github.com/zackzhangkai' }
    ],
    footer: {
      message: '商业实战出版级教程 | 严禁未授权翻印传播',
      copyright: 'Copyright © 2026 AI Agent 实战教程'
    }
  }
})
