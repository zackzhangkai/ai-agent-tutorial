import fs from 'fs';
import path from 'path';

function fixMermaidSyntax(content) {
  return content.replace(/```mermaid\n([\s\S]*?)```/g, (fullMatch, code) => {
    let fixedCode = code;

    // 1. 修复 subgraph 中的未引号括号：subgraph Name[Title (Desc)] -> subgraph Name["Title (Desc)"]
    fixedCode = fixedCode.replace(/subgraph\s+([a-zA-Z0-9_-]+)\[([^"\n]+?\([^"\n]+?\)[^"\n]*?)\]/g, 'subgraph $1["$2"]');

    // 2. 修复普通节点的中括号未引号括号：Node[Title (Desc)] -> Node["Title (Desc)"]
    // 匹配如: ID[文本\n(文本)]
    fixedCode = fixedCode.replace(/([a-zA-Z0-9_-]+)\[([^"\n]+?\([^"\n]*?\)[^"\n]*?)\]/g, '$1["$2"]');

    // 3. 针对多行或有换行符的 brackets
    fixedCode = fixedCode.replace(/([a-zA-Z0-9_-]+)\[\s*([^"][^\]]*?\([^\]]*?\)[^\]]*?)\s*\]/g, (m, id, text) => {
      if (text.startsWith('"') && text.endsWith('"')) return m;
      return `${id}["${text.trim()}"]`;
    });

    // 3.5 针对圆柱体数据库语法: ID[(文本)] -> ID[("文本")]
    fixedCode = fixedCode.replace(/([a-zA-Z0-9_-]+)\[\(\s*([^"][^)]*?)\s*\)\]/g, (m, id, text) => {
      if (text.startsWith('"') && text.endsWith('"')) return m;
      return `${id}[("${text.trim()}")]`;
    });

    // 4. 修复双向箭头 <--> 如果在 flowchart 引起问题，替换为双向标准或明确连线
    // 在 flowchart TD 中，A <--> B -> A <--> B 或是合法语法，但两端必须有空格
    fixedCode = fixedCode.replace(/<-->/g, ' <--> ');

    return '```mermaid\n' + fixedCode + '\n```';
  });
}

const docsDir = './docs/guide';
const files = fs.readdirSync(docsDir).filter(f => f.endsWith('.md')).concat(['../index.md']);

files.forEach(f => {
  const filePath = path.join(docsDir, f);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf-8');
  const fixed = fixMermaidSyntax(content);
  fs.writeFileSync(filePath, fixed, 'utf-8');
});

console.log('Finished fixing mermaid syntax!');
