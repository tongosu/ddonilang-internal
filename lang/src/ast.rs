// lang/src/ast.rs
use ddonirang_core::Fixed64;
use std::collections::HashMap;

use crate::delivery::MessageTransfer;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Span {
    pub start: usize,
    pub end: usize,
}
impl Span {
    pub fn new(start: usize, end: usize) -> Self {
        Self { start, end }
    }
    pub fn merge(&self, other: &Span) -> Span {
        Span {
            start: self.start.min(other.start),
            end: self.end.max(other.end),
        }
    }
}

pub type NodeId = u64;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SourceEpoch {
    PreV25,
    V25,
}

#[derive(Debug, Clone)]
pub struct CanonProgram {
    pub id: NodeId,
    pub source_epoch: SourceEpoch,
    pub items: Vec<TopLevelItem>,
    /// Imperative source-program statements. They deliberately remain outside
    /// callable definitions, so root `<-` never manufactures a callable or a
    /// DefinitionIdentity.
    pub root_stmts: Vec<Stmt>,
    pub origin: OriginMap,
}

/// DDL Wave 1 is a non-executable public-surface document.  It deliberately
/// stays separate from `CanonProgram`: a DDL projection has no runtime body.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DdlDocument {
    pub extension: DdlExtension,
    pub source_span: Span,
    pub sections: Vec<LanguageSection>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DdlExtension {
    Ddl,
    Olgim,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LanguageSection {
    pub language_profile_identity: String,
    pub header_span: Span,
    pub content_span: Span,
    pub projection: ImmutablePublicValueProjection,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ImmutablePublicValueProjection {
    /// Stable registry-owned identity; localized spelling is never identity.
    pub definition_identity: String,
    pub type_identity: String,
    pub localized_name: String,
    pub localized_type: String,
    pub declaration_span: Span,
    pub omitted_payload: OmittedPayload,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OmittedPayload {
    ValueInitializer,
}

#[derive(Debug, Clone)]
pub struct OriginMap {
    pub file_path: String,
    pub source: String,
    pub node_spans: HashMap<NodeId, Span>,
}

#[derive(Debug, Clone)]
pub enum TopLevelItem {
    SeedDef(SeedDef),
}

#[derive(Debug, Clone)]
pub struct SeedDef {
    pub id: NodeId,
    pub span: Span,
    pub canonical_name: String,
    pub seed_kind: SeedKind,
    pub params: Vec<ParamPin>,
    /// The explicitly pinned result type for the RD-406 named, single-
    /// expression callable surface. `None` keeps the established seed forms
    /// unchanged.
    pub result_type: Option<TypeRef>,
    pub body: Option<Body>,
    pub modifiers: Vec<Modifier>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SeedKind {
    Imeumssi,
    Umjikssi,
    ValueFunc,
    Gallaessi,
    Relationssi,
    Sam,
    Heureumssi,
    Ieumssi,
    Semssi,
    Named(String),
}

#[derive(Debug, Clone)]
pub struct ParamPin {
    /// Existing public parameter-pin identity. Call-site resolution and
    /// signature display remain bound to this name.
    pub id: NodeId,
    pub span: Span,
    pub pin_name: String,
    /// Existing local lexical binder, kept separate from the public pin even
    /// when both authored spellings are identical.
    pub binder_id: NodeId,
    pub binder_name: String,
    pub binder_span: Span,
    /// Retains exact authored full/short provenance after the short spelling
    /// is expanded into the same typed public-pin/local-binder contract.
    pub surface: ParamPinSurface,
    pub type_ref: TypeRef,
    pub default_value: Option<Expr>,
    pub optional: bool,
    pub josa_list: Vec<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ParamPinSurface {
    Short,
    FullSameSpelling,
    FullDistinctSpelling,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TypeRef {
    Named(String),
    Applied {
        name: String,
        args: Vec<TypeRef>,
    },
    Function {
        params: Vec<TypeRef>,
        result: Box<TypeRef>,
    },
    Infer,
}

#[derive(Debug, Clone)]
pub struct Body {
    pub id: NodeId,
    pub span: Span,
    pub stmts: Vec<Stmt>,
}

/// One exact branch declared by a `고름씨`.  The declaration order is source
/// provenance only; dispatch always uses the owner-qualified branch identity.
#[derive(Debug, Clone)]
pub struct SumBranchDecl {
    pub id: NodeId,
    pub span: Span,
    pub name: String,
    pub payload: Option<SumBranchPayload>,
}

#[derive(Debug, Clone)]
pub struct SumBranchPayload {
    pub binder: String,
    pub binder_span: Span,
    pub type_ref: TypeRef,
}

/// A statement-only arm of `값에 따라 { ... }`.
#[derive(Debug, Clone)]
pub struct SumMatchArm {
    pub id: NodeId,
    pub span: Span,
    pub owner: String,
    pub branch: String,
    pub binder: Option<String>,
    pub body: Body,
}

/// `(<이름>: <식>, ...) 보임.`이 선언한 공개 관찰 필드.
///
/// 순서는 곧 사용자 계약이므로 map으로 바꾸지 않는다. `name_span`은
/// 작성 도구가 순번 기반 ID 없이 DDN 이름 자체를 가리키는 데 사용한다.
#[derive(Debug, Clone)]
pub struct PublicObservationField {
    pub id: NodeId,
    pub span: Span,
    pub name: String,
    pub name_span: Span,
    pub value: Expr,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MetaBlockKind {
    Setting,
    Bogae,
    Seulgi,
    /// view-only 연출 블록 (Manim식 보개마당). state_hash 제외.
    /// entries[0] = { } 안의 원본 텍스트 그대로(opaque).
    BogeaMadang,
    /// AGE5 짜임 블록 최소 수용용 opaque 블록.
    /// entries[0] = { } 안의 원본 텍스트 그대로(opaque).
    Jjaim,
}

#[derive(Debug, Clone)]
pub enum Stmt {
    /// A closed, source-level sum declaration.  It is deliberately separate
    /// from ordinary definitions and from callable/choice declarations.
    SumDefinition {
        id: NodeId,
        span: Span,
        mood: Mood,
        name: String,
        branches: Vec<SumBranchDecl>,
    },
    /// Statement-only typed sum dispatch.  There is intentionally no
    /// expression-valued counterpart in this product vertical.
    SumMatch {
        id: NodeId,
        span: Span,
        mood: Mood,
        subject: Expr,
        arms: Vec<SumMatchArm>,
        default_body: Option<Body>,
    },
    DeclBlock {
        id: NodeId,
        span: Span,
        mood: Mood,
        kind: DeclKind,
        items: Vec<DeclItem>,
    },
    Definition {
        id: NodeId,
        span: Span,
        mood: Mood,
        name: String,
        type_ref: TypeRef,
        value: Expr,
    },
    Mutate {
        id: NodeId,
        span: Span,
        mood: Mood,
        target: Expr,
        value: Expr,
        deferred: bool,
        deferred_span: Option<Span>,
    },
    /// A produced value written to an already-addressed writable place.
    /// This is deliberately not a reverse spelling of `Mutate`: `producer ->
    /// destination` preserves the producer/result role through canon and runtime.
    ResultFlow {
        id: NodeId,
        span: Span,
        mood: Mood,
        producer: Expr,
        destination: Expr,
    },
    Expr {
        id: NodeId,
        span: Span,
        mood: Mood,
        expr: Expr,
    },
    Receive {
        id: NodeId,
        span: Span,
        mood: Mood,
        /// Exact W1-C1 sender identity predicate. None means ANY_SENDER.
        sender: Option<Expr>,
        kind: Option<String>,
        binding: Option<String>,
        /// Present only for the exact `(이름:형)를 받으면` surface. This is
        /// a payload type predicate, not a historical alert-kind alias.
        payload_type: Option<String>,
        condition: Option<Expr>,
        body: Body,
    },
    Send {
        id: NodeId,
        span: Span,
        mood: Mood,
        transfer: MessageTransfer,
        sender: Option<Expr>,
        payload: Expr,
        receiver: Expr,
    },
    Show {
        id: NodeId,
        span: Span,
        mood: Mood,
        expr: Expr,
    },
    Inspect {
        id: NodeId,
        span: Span,
        mood: Mood,
        expr: Expr,
    },
    PublicObservation {
        id: NodeId,
        span: Span,
        mood: Mood,
        fields: Vec<PublicObservationField>,
    },
    MetaBlock {
        id: NodeId,
        span: Span,
        mood: Mood,
        kind: MetaBlockKind,
        entries: Vec<String>,
    },
    Pragma {
        id: NodeId,
        span: Span,
        name: String,
        args: String,
    },
    Return {
        id: NodeId,
        span: Span,
        mood: Mood,
        value: Expr,
    },
    If {
        id: NodeId,
        span: Span,
        mood: Mood,
        condition: Expr,
        then_body: Body,
        else_body: Option<Body>,
    },
    Try {
        id: NodeId,
        span: Span,
        mood: Mood,
        action: Expr,
        body: Body,
    },
    Choose {
        id: NodeId,
        span: Span,
        mood: Mood,
        branches: Vec<ChooseBranch>,
        else_body: Body,
    },
    Repeat {
        id: NodeId,
        span: Span,
        mood: Mood,
        body: Body,
    },
    While {
        id: NodeId,
        span: Span,
        mood: Mood,
        condition: Expr,
        body: Body,
    },
    ForEach {
        id: NodeId,
        span: Span,
        mood: Mood,
        item: String,
        item_type: Option<TypeRef>,
        iterable: Expr,
        body: Body,
    },
    Quantifier {
        id: NodeId,
        span: Span,
        mood: Mood,
        kind: QuantifierKind,
        variable: String,
        domain: TypeRef,
        body: Body,
    },
    Break {
        id: NodeId,
        span: Span,
        mood: Mood,
    },
    ContinueLoop {
        id: NodeId,
        span: Span,
        mood: Mood,
    },
    Contract {
        id: NodeId,
        span: Span,
        mood: Mood,
        kind: ContractKind,
        mode: ContractMode,
        condition: Expr,
        then_body: Option<Body>,
        else_body: Body,
    },
    Guard {
        id: NodeId,
        span: Span,
        mood: Mood,
        condition: Expr,
        body: Body,
    },
    BeatBlock {
        id: NodeId,
        span: Span,
        mood: Mood,
        body: Body,
    },
    Hook {
        id: NodeId,
        span: Span,
        mood: Mood,
        kind: HookKind,
        body: Body,
    },
    HookWhenBecomes {
        id: NodeId,
        span: Span,
        mood: Mood,
        condition: Expr,
        body: Body,
    },
    HookWhile {
        id: NodeId,
        span: Span,
        mood: Mood,
        condition: Expr,
        body: Body,
    },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DeclKind {
    Gureut,
    Butbak,
}

#[derive(Debug, Clone)]
pub struct DeclItem {
    pub id: NodeId,
    pub span: Span,
    pub name: String,
    pub kind: DeclKind,
    pub type_ref: TypeRef,
    pub value: Option<Expr>,
}

#[derive(Debug, Clone)]
pub struct Expr {
    pub id: NodeId,
    pub span: Span,
    pub kind: ExprKind,
}

/// The semantic content axis of a `ViewValue` (RD-125).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ViewContentKind {
    Table,
    Chart,
    Scene,
}

/// The semantic spatial axis of a `ViewValue` and `SceneValue` (RD-125).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SpatialProfile {
    TextGrid,
    Plane2,
    Space3,
}

/// A scene-backed view takes its profile from the typed scene role.  This is
/// an exact typed dependency, not source-text or argument-order inference.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ViewSpatialBinding {
    Fixed(SpatialProfile),
    SceneRole,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SceneElementKind {
    Circle,
    Polygon,
    Text,
    Face,
    Camera,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SceneElementProfile {
    Plane2,
    Space3,
    Plane2OrSpace3,
    Camera,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BogaeRelationKind {
    Primary,
    Overlay,
    Side,
    Detail,
}

/// Physical, internal AST tags for the already-approved View/Scene/Bogae
/// semantic values.  These tags add no public identity and no Core IR.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BogaeTypedValueKind {
    SceneElement {
        element: SceneElementKind,
        profile: SceneElementProfile,
    },
    Scene {
        profile: SpatialProfile,
    },
    View {
        content: ViewContentKind,
        spatial: ViewSpatialBinding,
    },
    Relation {
        relation: BogaeRelationKind,
    },
    Composition,
}

/// Typed value carrier produced only for an exact standard provider name.
/// Roles are stored in canonical provider order; ordered geometry and
/// relation collections remain ordered inside their child expressions.
#[derive(Debug, Clone)]
pub struct BogaeTypedValue {
    pub provider: String,
    pub kind: BogaeTypedValueKind,
    pub roles: Vec<ArgBinding>,
}

#[derive(Debug, Clone)]
pub enum ExprKind {
    Literal(Literal),
    Var(String),
    FieldAccess {
        target: Box<Expr>,
        field: String,
        /// `A.B`에서 마지막 `B`의 정확한 UTF-8 byte 범위.
        field_span: Span,
    },
    SeedLiteral {
        param: String,
        body: Box<Expr>,
    },
    Call {
        args: Vec<ArgBinding>,
        func: String,
    },
    BogaeValue(BogaeTypedValue),
    /// `Owner.$branch` or `Owner.$branch(pin=value)`.  This is not field
    /// access and not a callable; its owner and branch remain exact typed
    /// identities through canonicalization and execution.
    SumBranchValue {
        owner: String,
        branch: String,
        payload_name: Option<String>,
        payload: Option<Box<Expr>>,
    },
    /// `차림[...]` is a source-level collection constructor, not a call or
    /// postfix selection.  Its elements retain their authored order.
    CollectionConstructor {
        elements: Vec<Expr>,
    },
    /// An indexed writable place. This is only valid as `Stmt::Mutate`'s
    /// target and is deliberately distinct from postfix selection values.
    SelectionPlace {
        target: Box<Expr>,
        index: Box<Expr>,
    },
    Infix {
        left: Box<Expr>,
        op: String,
        right: Box<Expr>,
    },
    Suffix {
        value: Box<Expr>,
        at: AtSuffix,
    },
    Thunk(Body),
    Eval {
        thunk: Box<Expr>,
        mode: ThunkEvalMode,
    },
    Pipe {
        stages: Vec<Expr>,
    },
    FlowValue,
    Pack {
        fields: Vec<(String, Expr)>,
    },
    Assertion(Assertion),
    StateMachine(StateMachine),
    Formula(Formula),
    Template(Template),
    TemplateRender {
        template: Template,
        inject: Vec<(String, Expr)>,
    },
    FormulaEval {
        formula: Formula,
        inject: Vec<(String, Expr)>,
    },
    Nuance {
        level: String,
        expr: Box<Expr>,
    },
}

#[derive(Debug, Clone)]
pub struct ArgBinding {
    pub id: NodeId,
    pub span: Span,
    pub expr: Expr,
    pub josa: Option<String>,
    pub resolved_pin: Option<String>,
    pub binding_reason: BindingReason,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum AtSuffix {
    Unit(String),
    Asset(String),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BindingReason {
    Dictionary,
    Positional,
    UserFixed,
    FlowInjected,
    ContextItemInjected,
    Ambiguous { candidates: Vec<String> },
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ThunkEvalMode {
    Value,
    Bool,
    Not,
    Do,
    Pipe,
}

#[derive(Debug, Clone)]
pub struct ChooseBranch {
    pub condition: Expr,
    pub body: Body,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ContractKind {
    Pre,
    Post,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ContractMode {
    Abort,
    Alert,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum QuantifierKind {
    ForAll,
    Exists,
    ExistsUnique,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum HookKind {
    Start,
    End,
    EveryMadi,
    EveryNMadi(u64),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Mood {
    Declarative,
    Imperative,
    Suggestive,
    Interrogative,
    Exclamative,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Literal {
    Int(i64),
    Fixed64(Fixed64),
    String(String),
    Bool(bool),
    Atom(String),
    Regex(RegexLiteral),
    Resource(String),
    None,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegexLiteral {
    pub pattern: String,
    pub flags: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Template {
    pub raw: String,
    pub parts: Vec<TemplatePart>,
    pub tag: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FormulaDialect {
    Ascii,
    Ascii1,
    Latex,
    Other(String),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Formula {
    pub raw: String,
    pub dialect: FormulaDialect,
    pub explicit_tag: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StateMachine {
    pub states: Vec<String>,
    pub initial: String,
    pub transitions: Vec<StateTransition>,
    pub on_transition_checks: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Assertion {
    pub body_source: String,
    pub canon: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StateTransition {
    pub from: String,
    pub to: String,
    pub guard_name: Option<String>,
    pub action_name: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TemplatePart {
    Text(String),
    Placeholder(TemplatePlaceholder),
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TemplatePlaceholder {
    pub path: Vec<String>,
    pub format: Option<TemplateFormat>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TemplateFormat {
    pub raw: String,
    pub width: Option<usize>,
    pub zero_pad: bool,
    pub precision: Option<u8>,
    pub unit: Option<String>,
}

#[derive(Debug, Clone)]
pub struct Modifier {
    pub id: NodeId,
    pub span: Span,
}

impl Expr {
    pub fn new(id: NodeId, span: Span, kind: ExprKind) -> Self {
        Self { id, span, kind }
    }
}
