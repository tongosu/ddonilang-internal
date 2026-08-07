import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const publishRoot = path.join(repoRoot, "publish");
const i18nRoot = path.join(publishRoot, "i18n");
const checkOnly = process.argv.includes("--check");
const mismatches = [];

const locales = [
  {
    code: "ko",
    name: "한국어",
    title: "또니랑",
    summary: "한국어로 프로그램·시뮬레이션·교과 실험을 만들고 재현하는 언어와 도구입니다.",
    quick: "1분 첫 실행",
    check: "출력에서 23, 15, 8을 확인하세요.",
    status: "현재 상태",
    docs: "주요 문서",
    translation: "한국어 기준 안내",
  },
  {
    code: "en",
    name: "English",
    title: "Ddonilang",
    summary: "A Korean-first language and toolchain for reproducible programs, simulations, and learning experiments.",
    quick: "One-minute first run",
    check: "Confirm that the output contains 23, 15, and 8.",
    status: "Current status",
    docs: "Main documents",
    translation: "Starter translation; Human review open",
  },
  {
    code: "ja",
    name: "日本語",
    title: "トニラン (Ddonilang)",
    summary: "韓国語を中心に、再現可能なプログラム・シミュレーション・学習実験を作る言語とツールです。",
    quick: "1分で最初の実行",
    check: "出力に 23、15、8 が含まれることを確認してください。",
    status: "現在の状態",
    docs: "主な文書",
    translation: "スターター翻訳・Human review open",
  },
  {
    code: "tr",
    name: "Türkçe",
    title: "Ddonilang",
    summary: "Yeniden üretilebilir programlar, simülasyonlar ve öğrenme deneyleri için Korece merkezli bir dil ve araç takımıdır.",
    quick: "Bir dakikalık ilk çalıştırma",
    check: "Çıktıda 23, 15 ve 8 değerlerini doğrulayın.",
    status: "Güncel durum",
    docs: "Ana belgeler",
    translation: "Başlangıç çevirisi; Human review open",
  },
  {
    code: "mn",
    name: "Монгол",
    title: "Ddonilang",
    summary: "Дахин давтагдах програм, симуляци, сургалтын туршилтад зориулсан солонгос хэлд төвлөрсөн хэл ба хэрэгсэл.",
    quick: "Нэг минутын анхны ажиллуулалт",
    check: "Гаралтад 23, 15, 8 байгааг шалгана уу.",
    status: "Одоогийн төлөв",
    docs: "Үндсэн баримтууд",
    translation: "Starter орчуулга; Human review open",
  },
  {
    code: "ay",
    name: "Aymara",
    title: "Ddonilang",
    summary: "Programas, simulaciones ukat yatiqaña yant'awinaka mayamp lurasiñapataki coreano aruta qallta herramienta.",
    quick: "Maya minuto qallta",
    check: "Resultado ukan 23, 15 ukat 8 uñakipam.",
    status: "Jichha estado",
    docs: "Jach'a qillqatanaka",
    translation: "Starter localization; Human review open",
  },
  {
    code: "eu",
    name: "Euskara",
    title: "Ddonilang",
    summary: "Programa, simulazio eta ikasketa-esperimentu erreproduzigarrietarako koreeran oinarritutako hizkuntza eta tresnak.",
    quick: "Minutu bateko lehen exekuzioa",
    check: "Egiaztatu irteeran 23, 15 eta 8 agertzen direla.",
    status: "Uneko egoera",
    docs: "Dokumentu nagusiak",
    translation: "Hasierako itzulpena; Human review open",
  },
  {
    code: "kn",
    name: "ಕನ್ನಡ",
    title: "Ddonilang",
    summary: "ಪುನರುತ್ಪಾದಿಸಬಹುದಾದ programs, simulations ಮತ್ತು learning experiments ಗಾಗಿ Korean-first ಭಾಷೆ ಮತ್ತು tools.",
    quick: "ಒಂದು ನಿಮಿಷದ ಮೊದಲ run",
    check: "Output ನಲ್ಲಿ 23, 15 ಮತ್ತು 8 ಇವೆ ಎಂದು ಪರಿಶೀಲಿಸಿ.",
    status: "ಪ್ರಸ್ತುತ status",
    docs: "ಮುಖ್ಯ documents",
    translation: "Starter translation; Human review open",
  },
  {
    code: "ne",
    name: "नेपाली",
    title: "Ddonilang",
    summary: "पुनरुत्पादनयोग्य program, simulation र learning experiment का लागि Korean-first भाषा र tools।",
    quick: "एक मिनेटको पहिलो run",
    check: "Output मा 23, 15 र 8 भएको पुष्टि गर्नुहोस्।",
    status: "हालको status",
    docs: "मुख्य documents",
    translation: "Starter translation; Human review open",
  },
  {
    code: "qu",
    name: "Runasimi",
    title: "Ddonilang",
    summary: "Programakuna, simulacionkuna, yachay yant'aykunata kutichiyta atichiq coreano simipi qallariq rimaymi.",
    quick: "Huk minuto qallariy",
    check: "Lluqsisqapi 23, 15, 8 kasqanta qhaway.",
    status: "Kunan estado",
    docs: "Hatun qillqakuna",
    translation: "Starter localization; Human review open",
  },
  {
    code: "sym3",
    name: "sym3",
    title: "ddonilang",
    summary: "ko-first deterministic language + toolchain :: programs | simulations | learning_experiments",
    quick: "first_run@1min",
    check: "assert output = [23, 15, 8]",
    status: "status_now",
    docs: "docs_main",
    translation: "compact starter; Human review open",
  },
  {
    code: "ta",
    name: "தமிழ்",
    title: "Ddonilang",
    summary: "மீண்டும் உருவாக்கக்கூடிய programs, simulations மற்றும் learning experiments க்கான Korean-first மொழி மற்றும் tools.",
    quick: "ஒரு நிமிட முதல் run",
    check: "Output இல் 23, 15, 8 இருப்பதை உறுதிப்படுத்தவும்.",
    status: "தற்போதைய status",
    docs: "முக்கிய documents",
    translation: "Starter translation; Human review open",
  },
  {
    code: "te",
    name: "తెలుగు",
    title: "Ddonilang",
    summary: "పునరుత్పాదక programs, simulations మరియు learning experiments కోసం Korean-first భాష మరియు tools.",
    quick: "ఒక నిమిషం మొదటి run",
    check: "Output లో 23, 15, 8 ఉన్నాయని నిర్ధారించండి.",
    status: "ప్రస్తుత status",
    docs: "ముఖ్య documents",
    translation: "Starter translation; Human review open",
  },
  {
    code: "zh",
    name: "中文",
    title: "Ddonilang",
    summary: "一个以韩语为中心、用于可复现程序、模拟和学习实验的语言与工具链。",
    quick: "一分钟首次运行",
    check: "确认输出包含 23、15 和 8。",
    status: "当前状态",
    docs: "主要文档",
    translation: "起始翻译；Human review open",
  },
  {
    code: "es",
    name: "Español",
    title: "Ddonilang",
    summary: "Un lenguaje y conjunto de herramientas centrado en coreano para programas, simulaciones y experimentos reproducibles.",
    quick: "Primera ejecución en un minuto",
    check: "Confirma que la salida contiene 23, 15 y 8.",
    status: "Estado actual",
    docs: "Documentos principales",
    translation: "Traducción inicial; Human review open",
  },
  {
    code: "fr",
    name: "Français",
    title: "Ddonilang",
    summary: "Un langage et des outils centrés sur le coréen pour des programmes, simulations et expériences reproductibles.",
    quick: "Première exécution en une minute",
    check: "Vérifiez que la sortie contient 23, 15 et 8.",
    status: "État actuel",
    docs: "Documents principaux",
    translation: "Traduction initiale ; Human review open",
  },
  {
    code: "de",
    name: "Deutsch",
    title: "Ddonilang",
    summary: "Eine koreanisch ausgerichtete Sprache und Werkzeugkette für reproduzierbare Programme, Simulationen und Lernexperimente.",
    quick: "Erster Lauf in einer Minute",
    check: "Prüfen Sie, dass die Ausgabe 23, 15 und 8 enthält.",
    status: "Aktueller Status",
    docs: "Hauptdokumente",
    translation: "Starter-Übersetzung; Human review open",
  },
];

const legacyRootReadmes = new Set([
  "ay",
  "en",
  "eu",
  "ja",
  "kn",
  "mn",
  "ne",
  "qu",
  "sym3",
  "ta",
  "te",
  "tr",
]);

function write(relative, text) {
  const target = path.join(repoRoot, relative);
  const expected = text.replace(/\r\n/g, "\n");
  if (checkOnly) {
    const actual = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : null;
    if (actual !== expected) {
      mismatches.push(relative);
    }
    return;
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, expected, "utf8");
}

function readme(locale) {
  return `# ${locale.title} (${locale.name})

> ${locale.summary}

Translation status: **${locale.translation}**

## ${locale.quick}

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

${locale.check}

## ${locale.status}

- Public Language SPEC: **v0.5.0 / docs-first current**
- GitHub development trunk: **protected main**
- Public CI: code tests + public golden + SPEC seal + first example
- Full browser product + Human review: **OPEN by feature**
- Internal SSOT and public SPEC use separate version lineages.

## ${locale.docs}

- [Quick start](QUICKSTART.md)
- [Korean project introduction](../../../README.md)
- [Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
- [Public Language SPEC](../../spec/CURRENT.md)
- [All languages](../INDEX.md)

## Boundary

This starter translation helps navigation. It does not define DDN language semantics or promote
docs-first features to implemented product support. Keep DDN code, commands, paths, schema names,
and error codes canonical.
`;
}

function quickstart(locale) {
  return `# ${locale.quick} — ${locale.title}

> ${locale.translation}

## 1. Requirements

- Rust + Cargo
- Git
- Optional for Seamgrim workspace: Python 3

## 2. Build the CLI

~~~sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
~~~

## 3. Run the first DDN example

~~~sh
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- run publish/examples/00_first_result.ddn
~~~

${locale.check}

## 4. Optional Seamgrim workspace

~~~sh
python solutions/seamgrim_ui_mvp/tools/ddn_exec_server.py
~~~

Open: http://localhost:8787/

The workspace contains multiple examples, but not every docs-first language surface is implemented
in the default browser product. Check the [product support matrix](../../PRODUCT_SUPPORT_CURRENT.md).

## 5. Next

- [Localized introduction](README.md)
- [Korean learning path](../../LEARNING_PATH.md)
- [Public Language SPEC](../../spec/CURRENT.md)
`;
}

function devStructure(locale) {
  const korean = locale.code === "ko";
  const heading = korean ? "공개 개발 구조" : "Public development structure";
  const boundary = korean ? "검증 경계" : "Verification boundary";
  return `# ${heading} — ${locale.title}

> ${locale.translation}

| Layer | Path | Responsibility |
| --- | --- | --- |
| deterministic engine | \`core/\` | committed world-state transitions |
| language | \`lang/\` | grammar, parser, canonicalization |
| runtime and tool | \`tool/\` | execution front door and WASM API |
| CLI | \`tools/teul-cli/\` | command-line execution and public checks |
| numeric and proof | \`numeric/\`, \`symbolic/\`, \`proof/\` | bounded math and proof kernels |
| Seamgrim | \`solutions/seamgrim_ui_mvp/\` | browser workspace and view layer |
| public documents | \`publish/\` | guides and fixed public SPEC lineage |

## ${boundary}

- GitHub public CI verifies public code tests, selected golden tests, the public SPEC seal, and the
  first CLI example.
- It does not prove full browser behavior, Human review, private SSOT gates, or every docs-first
  surface.
- Runtime truth belongs to committed DDN state and records. A renderer must not invent hidden
  semantics from CSS, metadata, project titles, or file order.
- Python and JavaScript may orchestrate tools and UI, but test-only lowering is not language
  implementation evidence.

[Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md) ·
[Public Language SPEC](../../spec/CURRENT.md)
`;
}

function downloads(locale) {
  const korean = locale.code === "ko";
  const heading = korean ? "다운로드" : "Downloads";
  return `# ${heading} — ${locale.title}

> ${locale.translation}

## Current distribution boundary

- A stable end-user binary release is not claimed by this document.
- Until a verified GitHub Release is published, build and run from source using
  [QUICKSTART.md](QUICKSTART.md).
- Do not treat planned platform names or archive examples as released products.

## Source build

~~~sh
cargo build --manifest-path tools/teul-cli/Cargo.toml
cargo run -q --manifest-path tools/teul-cli/Cargo.toml -- --help
~~~

## Future release requirements

A public binary release should provide an OS/architecture label, a version, SHA-256 checksums,
license and notice files, and verification notes. Repository source and release binaries have
separate publication gates.

[Product support matrix](../../PRODUCT_SUPPORT_CURRENT.md)
`;
}

function legacyStub(locale) {
  return `# ${locale.title} — moved

The maintained ${locale.name} starter documents are now under:

- [publish/i18n/${locale.code}/README.md](i18n/${locale.code}/README.md)
- [publish/i18n/${locale.code}/QUICKSTART.md](i18n/${locale.code}/QUICKSTART.md)

This compatibility pointer remains so older external links do not break.
`;
}

for (const locale of locales) {
  write(`publish/i18n/${locale.code}/README.md`, readme(locale));
  write(`publish/i18n/${locale.code}/QUICKSTART.md`, quickstart(locale));
  write(`publish/i18n/${locale.code}/DEV_STRUCTURE.md`, devStructure(locale));
  write(`publish/i18n/${locale.code}/DOWNLOADS.md`, downloads(locale));
  if (legacyRootReadmes.has(locale.code)) {
    write(`publish/README_${locale.code}.md`, legacyStub(locale));
  }
}

const rows = locales
  .map(
    (locale) =>
      `| ${locale.code} | ${locale.name} | [README](./${locale.code}/README.md) | ${locale.translation} |`,
  )
  .join("\n");

write(
  "publish/i18n/INDEX.md",
  `# 또니랑 다국어 시작 문서

다국어 문서의 정본 위치는 \`publish/i18n/<언어 코드>/\`입니다.

| 코드 | 언어·표기 | 시작 | 상태 |
| --- | --- | --- | --- |
${rows}

## 포함 문서

각 언어 폴더에는 다음 문서가 있습니다.

- \`README.md\`: 현재 프로젝트 소개와 상태 경계
- \`QUICKSTART.md\`: 첫 실행
- \`DEV_STRUCTURE.md\`: 공개 개발 구조 starter
- \`DOWNLOADS.md\`: 배포 경계
- \`RELEASE_NOTES_20260211.md\`: 역사적 릴리스 기록

## 번역 경계

- 한국어 안내와 공개 SPEC이 기준입니다.
- \`starter / Human review open\`은 사람이 전문 검토한 완성 번역이 아닙니다.
- DDN 코드·명령·경로·schema·오류 코드는 번역하지 않습니다.
- 번역본은 언어 의미나 제품 지원 상태를 독자적으로 바꾸지 않습니다.

[한국어 GitHub 소개로 돌아가기](../../README.md)
`,
);

if (checkOnly && mismatches.length > 0) {
  throw new Error(`generated public documents differ:\n${mismatches.join("\n")}`);
}

console.log(
  checkOnly
    ? `PUBLIC I18N CHECK: PASS (${locales.length} locales)`
    : `PUBLIC I18N GENERATE: PASS (${locales.length} locales)`,
);
