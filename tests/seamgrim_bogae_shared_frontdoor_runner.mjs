#!/usr/bin/env node

import {
  DDN_SOURCE_MODE_CURRENT,
  DDN_SOURCE_MODE_LEGACY_MIGRATION,
  prepareDdnSource,
} from "../solutions/seamgrim_ui_mvp/ui/runtime/ddn_preprocess.js";
import { WasmVmHandle } from "../solutions/seamgrim_ui_mvp/ui/runtime/wasm_vm_runtime.js";

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function mockClient(observed) {
  return {
    wasmModule: {
      wasm_execution_envelope_json(source) {
        observed.envelopeSource = source;
        return JSON.stringify({ execution_mode_decision: { authority: "parsed_program" } });
      },
    },
    updateLogic(source) {
      observed.updateSource = source;
    },
    updateLogicWithSourceProfile(source, profile) {
      observed.updateSource = source;
      observed.profile = profile;
    },
    parseWarningsParsed() {
      return [];
    },
    configuredMadi() {
      return 0;
    },
    getStateParsed() {
      return { ok: true };
    },
  };
}

async function currentRawSourceCase() {
  const source = "#이름(test)\r\n만약 값 >= 3 이라면 {\r\n  값 보여주기.\r\n}.\r\n";
  const prepared = prepareDdnSource(source, { mode: DDN_SOURCE_MODE_CURRENT });
  assert(prepared.bodyText === source, "current preparation changed source bytes");
  assert(prepared.sourceBytesPreserved === true, "current source provenance not preserved");

  const observed = {};
  const loader = {
    async ensure(bootstrap) {
      observed.bootstrap = bootstrap;
      return mockClient(observed);
    },
  };
  const handle = new WasmVmHandle({
    loader,
    defaultSourceText: source,
    sourceProfileIdentity: "v1-core-v25",
  });
  await handle.updateLogic(source);
  assert(observed.bootstrap === "1 보여주기.", "current profile did not use inert bootstrap");
  assert(observed.updateSource === source, "WASM current frontdoor did not receive raw source");
  assert(observed.envelopeSource === source, "execution envelope did not receive raw source");
  assert(observed.profile === "v1-core-v25", "source profile identity changed");
  assert(handle.lastBodyText === source, "current handle retained rewritten source");
  const debug = handle.getDebugInfo();
  assert(debug.sourceMode === DDN_SOURCE_MODE_CURRENT, "current source mode missing");
  assert(debug.sourceBytesPreserved === true, "current debug provenance mismatch");
}

async function explicitLegacyMigrationCase() {
  const source = "(매마디)마다 {\n  값 보여주기.\n}.\n";
  const prepared = prepareDdnSource(source, { mode: DDN_SOURCE_MODE_LEGACY_MIGRATION });
  assert(prepared.bodyText !== source, "legacy migration did not transform retired source");
  assert(prepared.bodyText.includes("매마디:움직씨"), "legacy migration result missing current hook");

  const observed = {};
  const loader = {
    async ensure(body) {
      observed.bootstrap = body;
      return mockClient(observed);
    },
  };
  const handle = new WasmVmHandle({
    loader,
    defaultSourceText: source,
    sourceMode: DDN_SOURCE_MODE_LEGACY_MIGRATION,
  });
  await handle.updateLogic(source);
  assert(observed.bootstrap !== source, "legacy source reached VM without explicit migration");
  assert(observed.updateSource !== source, "legacy update retained retired source unexpectedly");
  assert(handle.getDebugInfo().sourceMode === DDN_SOURCE_MODE_LEGACY_MIGRATION,
    "legacy migration mode was not recorded");
}

function unsupportedModeCase() {
  let error = null;
  try {
    prepareDdnSource("1 보여주기.", { mode: "auto" });
  } catch (caught) {
    error = caught;
  }
  assert(error?.code === "E_DDN_SOURCE_MODE_UNSUPPORTED", "unknown source mode did not fail closed");
}

await currentRawSourceCase();
await explicitLegacyMigrationCase();
unsupportedModeCase();

console.log("seamgrim_bogae_shared_frontdoor: ok");
