import fs from "node:fs";
import vm from "node:vm";

const input = process.argv[2] ?? "dist/std_statistical_studio.html";
const html = fs.readFileSync(input, "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];

if (!scripts.length) {
  throw new Error(`Inline script not found in ${input}`);
}

new vm.Script(scripts.at(-1)[1], { filename: input });
console.log("INLINE_SCRIPT_SYNTAX_PASS", scripts.at(-1)[1].length);
