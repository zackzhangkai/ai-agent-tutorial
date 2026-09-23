import subprocess
import json
import os
import time

SPACE_ID = "7628511480259464150"
PARENT_NODE_TOKEN = "MK8uw282vi6PG0klo8NcF8t2nTb"
LARK_CLI = "/Users/zack/.local/bin/lark-cli"
WORKSPACE = "/Users/zack/workspace/Agent学习教程"

CHAPTERS = [
    {
        "title": "第一章：心法与认知篇 —— Agent 搭建的五大底层逻辑",
        "file": os.path.join(WORKSPACE, "docs/guide/01-mindset.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "1.jpeg"), "caption": "Agent智能体搭建心得（上）"},
            {"path": os.path.join(WORKSPACE, "2.jpeg"), "caption": "Agent智能体搭建心得（下）"}
        ]
    },
    {
        "title": "第二章：路线图篇 —— Agent 开发与就业 14 步全景进阶路线",
        "file": os.path.join(WORKSPACE, "docs/guide/02-roadmap.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "0.png"), "caption": "Agent开发就业全景路线图"}
        ]
    },
    {
        "title": "第三章：架构与核心理论篇 —— 经典 Agent 决策运行体系",
        "file": os.path.join(WORKSPACE, "docs/guide/03-core-theory.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "9.jpeg"), "caption": "经典Agent感知-规划-行动决策体系与大厂实践"},
            {"path": os.path.join(WORKSPACE, "3.jpeg"), "caption": "商用Agent架构设计与ReAct/深度搜索流程"}
        ]
    },
    {
        "title": "第四章：关键技术底座篇 —— Prompt、RAG、Tool Calling 与微调实战",
        "file": os.path.join(WORKSPACE, "docs/guide/04-tech-foundations.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "10.jpeg"), "caption": "OpenAI Function Calling 数据闭环与工具能力微调"},
            {"path": os.path.join(WORKSPACE, "6.jpeg"), "caption": "智能客服业务需求与轻量意图分类器"}
        ]
    },
    {
        "title": "第五章：现代编排框架与开源生态篇 —— Dify、LangGraph、Eino",
        "file": os.path.join(WORKSPACE, "docs/guide/05-frameworks.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "8.jpeg"), "caption": "10个经典开源自主Agent项目架构"},
            {"path": os.path.join(WORKSPACE, "5.jpeg"), "caption": "基于Dify构建智能体应用与知识库配置"}
        ]
    },
    {
        "title": "第六章：企业级实战案例拆解篇 —— 三大商业项目从 0 到 1 落地",
        "file": os.path.join(WORKSPACE, "docs/guide/06-enterprise-cases.md"),
        "images": [
            {"path": os.path.join(WORKSPACE, "4.jpeg"), "caption": "已交付商用智能客服系统端到端架构"},
            {"path": os.path.join(WORKSPACE, "11.jpeg"), "caption": "AI智能医疗问诊工作流与三级分类消歧体系"}
        ]
    },
    {
        "title": "第七章：进阶工程化与求职面试篇 —— 算法八股与项目通关",
        "file": os.path.join(WORKSPACE, "docs/guide/07-career-interview.md"),
        "images": []
    }
]

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error (code {result.returncode}): {result.stderr or result.stdout}")
        raise RuntimeError(f"Command failed: {result.stderr or result.stdout}")
    return result.stdout

def main():
    results = []
    for i, ch in enumerate(CHAPTERS, 1):
        print(f"\n==================== 处理第 {i} 章: {ch['title']} ====================")
        
        # 1. 创建子节点
        create_cmd = [
            LARK_CLI, "wiki", "+node-create",
            "--space-id", SPACE_ID,
            "--parent-node-token", PARENT_NODE_TOKEN,
            "--title", ch["title"],
            "--obj-type", "docx"
        ]
        out = run_cmd(create_cmd)
        node_info = json.loads(out)
        data = node_info.get("data", {})
        node_token = data.get("node_token")
        obj_token = data.get("obj_token")
        print(f"Created node_token: {node_token}, obj_token: {obj_token}")

        time.sleep(1)

        # 2. 写入 Markdown 内容
        print(f"写入文档正文内容: {ch['file']}")
        update_cmd = [
            LARK_CLI, "docs", "+update",
            "--doc", obj_token,
            "--command", "overwrite",
            "--doc-format", "markdown",
            "--content", f"@{ch['file']}"
        ]
        run_cmd(update_cmd)
        print("文档正文写入成功！")

        time.sleep(1)

        # 3. 插入配图
        for img in ch.get("images", []):
            if os.path.exists(img["path"]):
                print(f"正在插入配图: {os.path.basename(img['path'])} - {img['caption']}")
                insert_cmd = [
                    LARK_CLI, "docs", "+media-insert",
                    "--doc", obj_token,
                    "--file", img["path"],
                    "--caption", img["caption"]
                ]
                try:
                    run_cmd(insert_cmd)
                    print(f"图片 {os.path.basename(img['path'])} 插入成功！")
                except Exception as e:
                    print(f"图片插入失败（跳过继续）: {e}")
                time.sleep(1)

        results.append({
            "title": ch["title"],
            "node_token": node_token,
            "obj_token": obj_token,
            "url": f"https://my.feishu.cn/wiki/{node_token}"
        })

    print("\n\n==================== 同步完成报告 ====================")
    for r in results:
        print(f"- {r['title']}: {r['url']}")

if __name__ == "__main__":
    main()
