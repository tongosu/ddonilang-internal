import { buildControlSpecsFromDdn } from "./control_parser.js";

export class SliderPanel {
  constructor({ container, statusEl, onCommit } = {}) {
    this.container = container;
    this.statusEl = statusEl;
    this.onCommit = typeof onCommit === "function" ? onCommit : () => {};
    this.specs = [];
    this.values = {};
    this.axisKeys = [];
    this.defaultAxisKey = "";
    this.defaultXAxisKey = "";
    this.warnings = [];
  }

  parseFromDdn(
    ddnText,
    {
      preserveValues = false,
      maegimControlJson = "",
      visibleControlNames = [],
      controlLabels = {},
    } = {},
  ) {
    const parsed = buildControlSpecsFromDdn(ddnText, { maegimControlJson });
    const visibleNames = Array.isArray(visibleControlNames)
      ? visibleControlNames.map((name) => String(name ?? "").trim()).filter(Boolean)
      : [];
    const visibleNameSet = new Set(visibleNames);
    const labelMap = controlLabels && typeof controlLabels === "object" ? controlLabels : {};
    const sourceSpecs = Array.isArray(parsed.specs) ? parsed.specs : [];
    const filteredSpecs = visibleNameSet.size
      ? sourceSpecs.filter((spec) => visibleNameSet.has(String(spec?.name ?? "").trim()))
      : sourceSpecs;
    const orderedSpecs = visibleNameSet.size
      ? [...filteredSpecs].sort((left, right) => (
          visibleNames.indexOf(String(left?.name ?? "").trim())
          - visibleNames.indexOf(String(right?.name ?? "").trim())
        ))
      : filteredSpecs;
    const nextSpecs = orderedSpecs.map((spec) => ({
      ...spec,
      displayLabel: String(labelMap?.[spec.name] ?? spec.name ?? "").trim() || String(spec.name ?? ""),
    }));
    const nextValues = {};
    nextSpecs.forEach((spec) => {
      const prev = Number(this.values?.[spec.name]);
      if (preserveValues && Number.isFinite(prev)) {
        nextValues[spec.name] = prev;
        return;
      }
      nextValues[spec.name] = Number(spec.value);
    });

    this.specs = nextSpecs;
    this.values = nextValues;
    this.axisKeys = Array.isArray(parsed.axisKeys) ? parsed.axisKeys : [];
    this.defaultAxisKey = String(parsed.defaultAxisKey ?? "").trim();
    this.defaultXAxisKey = String(parsed.defaultXAxisKey ?? "").trim();
    this.warnings = Array.isArray(parsed.warnings) ? parsed.warnings : [];

    if (this.statusEl) {
      const warningSuffix = this.warnings.length ? ` · 구식 범위주석 ${this.warnings.length}건` : "";
      if (parsed.source === "maegim_control_json" || parsed.source === "maegim_inline") {
        this.statusEl.textContent = `매김 조절: ${this.specs.length}개${warningSuffix}`;
      } else {
        this.statusEl.textContent = `매김 조절: -${warningSuffix}`;
      }
    }
    this.render();
    return {
      specs: [...this.specs],
      values: { ...this.values },
      axisKeys: [...this.axisKeys],
      defaultAxisKey: this.defaultAxisKey,
      defaultXAxisKey: this.defaultXAxisKey,
      source: parsed.source,
      warnings: [...this.warnings],
    };
  }

  render() {
    if (!this.container) return;
    this.container.innerHTML = "";

    if (!this.specs.length) {
      const empty = document.createElement("div");
      empty.className = "hint";
      empty.textContent = "조절 가능한 매김이 없습니다.";
      this.container.appendChild(empty);
      return;
    }

    this.specs.forEach((spec) => {
      const row = document.createElement("div");
      row.className = "slider-row";
      row.dataset.controlName = String(spec.name ?? "");

      const label = document.createElement("label");
      label.className = "slider-label";
      const displayLabel = String(spec.displayLabel ?? spec.name ?? "").trim() || String(spec.name ?? "");
      const controlId = `seamgrim-control-${String(spec.name ?? "control").replace(/[^A-Za-z0-9_가-힣-]/gu, "-")}`;
      label.htmlFor = `${controlId}-range`;
      label.textContent = `${displayLabel}${spec.unit ? ` (${spec.unit})` : ""}`;

      const range = document.createElement("input");
      range.type = "range";
      range.id = `${controlId}-range`;
      range.dataset.controlName = String(spec.name ?? "");
      range.setAttribute("aria-label", `${displayLabel} 조절`);
      range.min = String(spec.min);
      range.max = String(spec.max);
      range.step = String(spec.step);
      range.value = String(this.values[spec.name]);

      const number = document.createElement("input");
      number.type = "number";
      number.id = `${controlId}-number`;
      number.dataset.controlName = String(spec.name ?? "");
      number.setAttribute("aria-label", `${displayLabel} 값`);
      number.min = String(spec.min);
      number.max = String(spec.max);
      number.step = String(spec.step);
      number.value = String(this.values[spec.name]);

      const updateLocal = (nextValue) => {
        const numeric = Number(nextValue);
        if (!Number.isFinite(numeric)) return;
        this.values[spec.name] = numeric;
      };

      const commit = (nextValue) => {
        updateLocal(nextValue);
        this.onCommit(this.getValues());
      };

      range.addEventListener("input", () => {
        number.value = range.value;
        updateLocal(range.value);
      });
      range.addEventListener("change", () => {
        commit(range.value);
      });

      number.addEventListener("input", () => {
        range.value = number.value;
        updateLocal(number.value);
      });
      number.addEventListener("change", () => {
        commit(number.value);
      });

      row.appendChild(label);
      row.appendChild(range);
      row.appendChild(number);
      this.container.appendChild(row);
    });
  }

  getValues() {
    return { ...this.values };
  }

  setValues(nextValues = {}) {
    this.values = { ...this.values, ...nextValues };
    this.render();
  }

  getAxisKeys() {
    return [...this.axisKeys];
  }

  getDefaultAxisKey() {
    return this.defaultAxisKey;
  }

  getDefaultXAxisKey() {
    return this.defaultXAxisKey;
  }

  getSpecs() {
    return [...this.specs];
  }

  getWarnings() {
    return [...this.warnings];
  }
}
