<required_reading>
Read `${SKILL_DIR}/references/systemverilog-idioms.md` before starting the review. This is the authoritative reference for all idiomatic SystemVerilog patterns.

</required_reading>

<process>

<step_1>

**Type & Package Review**

Examine each file's type usage, packages, and parameterization:

**Types**:

- Is `logic` used instead of `wire`/`reg`?
- Are FSM states defined as `typedef enum logic [N:0]`?
- Are structured data types using `typedef struct packed`?
- Are type suffixes correct (`_e` for enums, `_t` for structs/typedefs, `_pkg` for packages)?
- Are parameters typed (`parameter int`, not bare `parameter`)?
- Is `$clog2()` used for bit-width calculations?

**Packages**:

- Are shared types, constants, and functions in packages?
- Are `` `define `` macros used where `localparam` or `parameter` would suffice?
- Are `` `include `` directives used where `import` would be cleaner?
- Are there duplicate type definitions across files?

For each finding, record:

- **File:line** - exact location
- **What** - the specific issue
- **Why** - what goes wrong (synthesis mismatch, maintenance burden, tool warnings)
- **Idiomatic alternative** - concrete code showing the fix

</step_1>

<step_2>

**Always-Block & FSM Review**

Examine every always block and FSM in each design file:

**Always blocks**:

- Is `always_ff` used for sequential logic (not `always @(posedge clk)`)?
- Is `always_comb` used for combinational logic (not `always @(*)`)?
- Is `always_latch` used for intentional latches?
- Are assignments correct: `<=` in `always_ff`, `=` in `always_comb`?
- Do `always_comb` blocks have default assignments preventing latches?

**Case statements**:

- Is `unique case` used (not bare `case`)?
- Is `priority case` used where priority encoding is intended?
- Are all cases covered or is there a `default`?
- Is `unique0 case` used where no-match is intentional?

**FSMs**:

- Is a two-always or one-always pattern used (flag three-always)?
- Are states `typedef enum logic [N:0]`?
- Is `unique case` used for state decoding?
- Are FSM outputs registered where timing requires it?

**Signal assignment**:

- Any blocking in sequential context or non-blocking in combinational context? (P0)
- Width mismatches in assignments? Unsized literals?
- Signed/unsigned mixing without explicit cast?

</step_2>

<step_3>

**Structural & Style Review**

Examine module declarations, instantiation, and naming:

**Module declarations**:

- Are ports ANSI-style (declared in the module header)?
- Are port directions and types explicit (`input logic`, not just `input`)?
- Is the parameter list clean (using `parameter` and `localparam` correctly)?

**Instantiation**:

- Are port connections named (`.port(signal)`), not positional?
- Are implicit named connections (`.port`) used where signal names match?
- Are unconnected outputs explicit (`.port()`)?
- Are instances prefixed with `u_`?

**Generate blocks**:

- Are all generate blocks labeled (`: gen_name`)?
- Are `generate`/`endgenerate` keywords omitted (optional in SystemVerilog)?
- Are `genvar` declarations inside the `for` scope?

**Naming**:

- Do signals use `snake_case`?
- Do parameters/localparams use `UPPER_SNAKE_CASE`?
- Are clocks named `clk` / `clk_<domain>`?
- Are resets named `rst_n` (active-low)?
- Are active-low signals marked with `_n`?
- Do enum types use `_e`, structs `_t`, interfaces `_if`, packages `_pkg`?
- Are generate blocks prefixed with `gen_`?

</step_3>

<step_4>

**Synthesizability Review**

Check for constructs that cause synthesis issues:

**Latches** (most critical):

- Scan every `always_comb` for incomplete assignments
- Check every `if` without `else` in combinational context
- Check every `case` without `default` in combinational context
- Verify default assignments at block top

**Width and signedness**:

- Are literals sized (`8'd1`, not `1`)?
- Are `'0` and `'1` used for width-agnostic fill?
- Are signed/unsigned casts explicit where needed?
- Are there truncation warnings waiting to happen?

**Tool compatibility (Vivado + Quartus)**:

- Are interfaces used at top-level ports (may need flattening)?
- Are SystemVerilog features within the synthesizable subset?
- No `initial` blocks in synthesizable code?
- No `#delay` in synthesizable code?
- No `real`, dynamic arrays, or class types in synthesizable code?

**Resource inference**:

- Are memories structured for block RAM inference (synchronous read, registered output)?
- Are shift registers recognizable for SRL inference?
- Are DSP-eligible arithmetic operations structured for DSP block inference?

</step_4>

<step_5>

**Findings Report**

Synthesize all findings into a single prioritized report:

**Priority definitions**:

- **P0 (Critical)**: Will cause incorrect hardware, simulation/synthesis mismatch, or elaboration failure
- **P1 (Important)**: Reduces quality, wastes resources, or creates maintenance burden
- **P2 (Style)**: Improves readability, follows convention, modernizes from Verilog-2001

**Summary table**:

| Priority | File:Line | Finding | Category | Idiomatic Fix |
| -------- | --------- | ------- | -------- | ------------- |
| P0       | ...       | ...     | ...      | ...           |
| P1       | ...       | ...     | ...      | ...           |
| P2       | ...       | ...     | ...      | ...           |

**Categories**: Type, Always, FSM, Case, Port, Naming, Generate, Synthesizability, Legacy

**For each P0 finding**, include the complete idiomatic code replacement, not just a description.

**Overall assessment**:

| Aspect                 | Status         | Notes |
| ---------------------- | -------------- | ----- |
| Type discipline        | Yes/No/Partial | ...   |
| Always-block usage     | Yes/No/Partial | ...   |
| Assignment correctness | Yes/No/Partial | ...   |
| Latch-free             | Yes/No/Partial | ...   |
| Naming consistency     | Yes/No/Partial | ...   |
| Synthesizable          | Yes/No/Partial | ...   |
| Legacy patterns        | None/Some/Many | ...   |

</step_5>

</process>

<success_criteria>
The review is complete when:

- [ ] Every file's type usage checked (logic vs wire/reg, enums, structs, packages)
- [ ] Every always block reviewed for correct type (ff/comb/latch) and assignment style
- [ ] Every FSM reviewed for coding style and state type
- [ ] Every case statement checked for unique/priority qualification
- [ ] Every instantiation checked for named connections
- [ ] Naming conventions audited across all files
- [ ] Latch analysis performed on all combinational blocks
- [ ] Legacy Verilog-2001 patterns identified
- [ ] Findings table delivered with priority, location, and idiomatic fix
- [ ] Overall assessment table delivered
- [ ] All P0 findings include complete replacement code

</success_criteria>
