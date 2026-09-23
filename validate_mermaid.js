import fs from 'fs';
import path from 'path';

// 读取 docs/guide/ 下的所有 markdown
const docsDir = './docs/guide';
const files = fs.readdirSync(docsDir).filter(f => f.endsWith('.md')).concat(['../index.md']);

let totalDiagrams = 0;
let errors = [];

files.forEach(f => {
  const filePath = path.join(docsDir, f);
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf-8');
  const regex = /```mermaid\n([\s\S]*?)```/g;
  let match;
  let index = 1;
  while ((match = regex.exec(content)) !== null) {
    totalDiagrams++;
    const code = match[1].trim();
    // 检查常见的 Mermaid 破坏性语法：
    // 1. 中括号内包含小括号未加双引号，如 [文本 (额外信息)]
    const unquotedParens = /\[[^"\n]*?\([^"\n]*?\)[^"\n]*?\]/g;
    let m2;
    while ((m2 = unquotedParens.exec(code)) !== null) {
      errors.push({
        file: f,
        diagram: index,
        issue: `Unquoted parentheses in bracket: ${m2[0]}`
      });
    }

    // 2. 双引号未闭合或非法嵌套
    index++;
  }
});

console.log(`Checked ${totalDiagrams} diagrams.`);
if (errors.length > 0) {
  console.log(`Found ${errors.length} syntax issues:`);
  errors.forEach(e => console.log(`  [${e.file} #${e.diagram}] ${e.issue}`));
} else {
  console.log('No unquoted parentheses found!');
}
