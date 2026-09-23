import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "AI Agent 全栈开发与商业落地教程",
  description: "从 0 到 1 打造可交付、高可用的企业级智能体系统",
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '教程正文', link: '/guide/01-mindset' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: '教程章节目录',
          items: [
            { text: '第一章：心法与认知篇', link: '/guide/01-mindset' },
            { text: '第二章：路线图篇 (14步)', link: '/guide/02-roadmap' },
            { text: '第三章：架构与理论篇', link: '/guide/03-core-theory' },
            { text: '第四章：关键技术底座篇', link: '/guide/04-tech-foundations' },
            { text: '第五章：现代编排框架篇', link: '/guide/05-frameworks' },
            { text: '第六章：企业实战案例篇', link: '/guide/06-enterprise-cases' },
            { text: '第七章：工程化与求职篇', link: '/guide/07-career-interview' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 AI Agent 实战教程'
    }
  }
})
