const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const manifest = require(path.join(root, "package.json"));
const grammar = JSON.parse(fs.readFileSync(path.join(root, "syntaxes", "ddn.tmLanguage.json"), "utf8"));
const theme = JSON.parse(fs.readFileSync(path.join(root, "themes", "ddonilang-readable-color-theme.json"), "utf8"));

const roleScopes = Object.values(manifest.contributes.semanticTokenScopes[0].scopes).flat();
const grammarText = JSON.stringify(grammar);
for (const scope of roleScopes) {
  assert.ok(grammarText.includes(scope), `semantic role has no TextMate scope: ${scope}`);
}
assert.strictEqual(grammar.patterns[0].include, "#comments");
assert.ok(grammar.patterns.findIndex((pattern) => pattern.include === "#strings") > 0);
assert.ok(grammar.repository.keywords.patterns[0].match.includes("(?<!"));
assert.ok(grammar.repository.keywords.patterns[0].match.includes("(?!"));
assert.ok(!grammarText.includes("에 따라"), "composite LSP45 phrase must remain unclassified");
assert.strictEqual(theme.semanticHighlighting, true);
assert.ok(theme.semanticTokenColors.function);
assert.ok(theme.tokenColors.some((entry) => entry.scope.includes("keyword.control.ddn")));
console.log("readability role parity: PASS");
