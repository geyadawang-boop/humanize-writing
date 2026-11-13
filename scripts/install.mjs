#!/usr/bin/env node
/**
 * humanize-writing 安装器：把技能文件复制到目标 skills 目录，不改环境变量与配置。
 * 用法：npx github:geyadawang-boop/humanize-writing --target <技能目录> [--force]
 */
import { cpSync, existsSync, readdirSync, rmSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SKIP = new Set(['.git', 'node_modules', '__pycache__', '.trae-cn', '.claude']);

function usage(code) {
  const text = [
    '用法：npx github:geyadawang-boop/humanize-writing --target <技能目录> [--force]',
    '',
    '示例：',
    '  npx github:geyadawang-boop/humanize-writing --target ~/.claude/skills/humanize-writing',
    '  npx github:geyadawang-boop/humanize-writing --target ./skills/humanize-writing --force',
    '',
    '默认目标：~/.claude/skills/humanize-writing',
    '--force：目标目录非空时覆盖。',
  ].join('\n');
  (code ? console.error : console.log)(text);
  process.exit(code);
}

function parseArgs(argv) {
  let target = join(homedir(), '.claude', 'skills', 'humanize-writing');
  let force = false;
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--target' || arg === '-t') {
      if (!argv[i + 1]) usage(2);
      target = argv[i + 1];
      i += 1;
    } else if (arg === '--force' || arg === '-f') {
      force = true;
    } else if (arg === '--help' || arg === '-h') {
      usage(0);
    } else {
      console.error('未知参数：' + arg);
      usage(2);
    }
  }
  const expanded = target.replace(/^~(?=$|[\\/])/, homedir());
  return { target: resolve(expanded), force };
}

const { target, force } = parseArgs(process.argv.slice(2));

if (target === ROOT || target.startsWith(ROOT + sep)) {
  console.error('目标目录不能是技能源目录或其子目录：' + target);
  process.exit(2);
}

if (existsSync(target) && readdirSync(target).length > 0) {
  if (!force) {
    console.error('目标目录非空：' + target + '\n确认覆盖请加 --force。');
    process.exit(1);
  }
  rmSync(target, { recursive: true, force: true });
}

cpSync(ROOT, target, {
  recursive: true,
  filter: (src) => {
    const name = src.split(/[\\/]/).pop();
    if (SKIP.has(name)) return false;
    return !name.endsWith('.pyc');
  },
});

console.log('已安装到 ' + target);
console.log('验证：python -B "' + join(target, 'tests', 'selftest.py') + '"');
