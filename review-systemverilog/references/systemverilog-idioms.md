<overview>
Idiomatic SystemVerilog (IEEE 1800-2017) patterns and anti-patterns for reviewing hand-written code targeting AMD Vivado and Altera Quartus Prime. Organized by review category. Each section defines what idiomatic code looks like, the legacy Verilog-2001 equivalent to flag, and common mistakes.

</overview>

<type_system>

**logic is the default type.** It replaces both `wire` and `reg`:

```systemverilog
// Idiomatic
logic        valid;
logic [7:0]  data;
logic [31:0] addr;

// Legacy (flag as P2)
wire        valid;
reg  [7:0]  data;
wire [31:0] addr;
```

Only use `wire` when multi-driver resolution is required (tri-state buses). The `logic` type works as both a continuous assignment target and a procedural assignment target — the tool infers wire or register from context.

**enum for FSM states and named constants**:

```systemverilog
typedef enum logic [1:0] {
  IDLE       = 2'b00,
  LOADING    = 2'b01,
  PROCESSING = 2'b10,
  DONE       = 2'b11
} state_e;

state_e state, next_state;
```

Key rules:

- Always `typedef` the enum so it can be reused
- Specify the underlying type (`logic [N:0]`) for synthesis control
- Use `_e` suffix for enum types
- Explicit encoding is optional — omit it to let the synthesizer choose

**struct packed for structured data**:

```systemverilog
typedef struct packed {
  logic [31:0] addr;
  logic [31:0] data;
  logic        valid;
  logic        ready;
} axi_req_t;

axi_req_t req;
assign req.valid = 1'b1;
```

Key rules:

- Always `packed` for synthesis (maps to contiguous bits)
- Use `_t` suffix for struct types
- `typedef` so it can be shared via packages

**Parameterized widths**:

```systemverilog
module fifo #(
  parameter int DATA_WIDTH = 8,
  parameter int DEPTH      = 16,
  localparam int ADDR_WIDTH = $clog2(DEPTH)
)(
  input  logic                  clk,
  input  logic                  rst_n,
  input  logic [DATA_WIDTH-1:0] wr_data,
  output logic [DATA_WIDTH-1:0] rd_data
);
```

Key rules:

- Use `parameter` for user-configurable values
- Use `localparam` for derived constants (not overridable)
- `$clog2()` is synthesizable — use it for bit-width calculations
- `int` is acceptable for parameters (32-bit, synthesizable)

**Anti-patterns**:

| Legacy Pattern               | Idiomatic SystemVerilog    | Priority |
| ---------------------------- | -------------------------- | -------- |
| `reg [7:0] data;`            | `logic [7:0] data;`        | P2       |
| `wire valid;`                | `logic valid;`             | P2       |
| `integer i;`                 | `int i;` or `int unsigned` | P2       |
| `parameter N = 8;`           | `parameter int N = 8`      | P2       |
| `` `define WIDTH 8 ``        | `localparam int WIDTH = 8` | P1       |
| Manual bit-width calculation | `$clog2(DEPTH)`            | P1       |

</type_system>

<always_blocks>

**always_ff for sequential logic (registered)**:

```systemverilog
always_ff @(posedge clk or negedge rst_n) begin
  if (!rst_n) begin
    count <= '0;
  end else begin
    count <= count + 1'b1;
  end
end
```

Key rules:

- Non-blocking assignments (`<=`) only
- The tool enforces this — using `=` in `always_ff` is an error
- Active-low async reset: `or negedge rst_n` in sensitivity, `if (!rst_n)` as outer condition
- Synchronous reset: omit reset from sensitivity, check inside `posedge clk`

**always_comb for combinational logic**:

```systemverilog
always_comb begin
  next_state = state;  // default prevents latches
  ready      = 1'b0;

  unique case (state)
    IDLE: begin
      ready = 1'b1;
      if (start) next_state = LOADING;
    end
    LOADING: begin
      if (data_valid) next_state = PROCESSING;
    end
    PROCESSING: begin
      if (done) next_state = DONE;
    end
    DONE: begin
      next_state = IDLE;
    end
  endcase
end
```

Key rules:

- Blocking assignments (`=`) only
- No sensitivity list — the tool infers it automatically
- The tool warns if a latch is inferred (unlike `always @(*)`)
- Default assignments at top prevent latches

**always_latch for intentional latches**:

```systemverilog
always_latch begin
  if (enable) data_out = data_in;
end
```

Use only when a latch is the intended hardware. The tool confirms latch behavior rather than warning.

**Legacy patterns to flag**:

```systemverilog
// Legacy — flag as P2
always @(posedge clk) begin  // Use always_ff
  count <= count + 1;
end

always @(*) begin             // Use always_comb
  out = a & b;
end

always @(a or b) begin        // Use always_comb (incomplete sensitivity is a bug)
  out = a & b | c;            // 'c' missing from sensitivity list!
end
```

**Blocking vs non-blocking — the cardinal rule**:

| Context        | Assignment | Rationale                                       |
| -------------- | ---------- | ----------------------------------------------- |
| `always_ff`    | `<=`       | Non-blocking: models register behavior          |
| `always_comb`  | `=`        | Blocking: models combinational wire propagation |
| `always_latch` | `=`        | Blocking: models transparent latch              |

Mixing `=` in `always_ff` or `<=` in `always_comb` is **P0** — it causes simulation/synthesis mismatch.

</always_blocks>

<fsm_coding>

**Two-always-block FSM** (most idiomatic):

```systemverilog
typedef enum logic [1:0] {
  IDLE, LOADING, PROCESSING, DONE
} state_e;

state_e state, next_state;

// Sequential: state register
always_ff @(posedge clk or negedge rst_n) begin
  if (!rst_n) state <= IDLE;
  else        state <= next_state;
end

// Combinational: next-state + outputs
always_comb begin
  next_state = state;
  busy       = 1'b1;

  unique case (state)
    IDLE: begin
      busy = 1'b0;
      if (start) next_state = LOADING;
    end
    LOADING: begin
      if (data_ready) next_state = PROCESSING;
    end
    PROCESSING: begin
      if (compute_done) next_state = DONE;
    end
    DONE: begin
      next_state = IDLE;
    end
  endcase
end
```

**One-always-block FSM** (simpler, all outputs registered):

```systemverilog
always_ff @(posedge clk or negedge rst_n) begin
  if (!rst_n) begin
    state <= IDLE;
    busy  <= 1'b0;
  end else begin
    unique case (state)
      IDLE: begin
        busy <= 1'b0;
        if (start) begin
          state <= LOADING;
          busy  <= 1'b1;
        end
      end
      // ...
    endcase
  end
end
```

**Three-always-block FSM** — generally avoid (same rationale as VHDL: the output process can merge with next-state logic).

**State type rules**:

- Always use `typedef enum` with explicit underlying logic type
- `_e` suffix for the enum type
- Descriptive state names: `WAIT_FOR_ACK`, not `S3`
- Use `unique case` — synthesizer verifies completeness and mutual exclusivity

</fsm_coding>

<case_statements>

**unique case** — all cases covered, mutually exclusive:

```systemverilog
unique case (opcode)
  ADD:  result = a + b;
  SUB:  result = a - b;
  AND:  result = a & b;
  OR:   result = a | b;
endcase
// Synthesizer warns if cases aren't exhaustive or overlap
```

**priority case** — first match wins, like an if-else chain:

```systemverilog
priority case (1'b1)
  irq[3]: isr_addr = ISR_3;
  irq[2]: isr_addr = ISR_2;
  irq[1]: isr_addr = ISR_1;
  irq[0]: isr_addr = ISR_0;
  default: isr_addr = ISR_DEFAULT;
endcase
```

**unique0 case** — like unique but no-match is legal (no warning if nothing matches):

```systemverilog
unique0 case (addr[7:4])
  4'hA: sel = periph_a;
  4'hB: sel = periph_b;
  // No default needed — no match is intentional
endcase
```

**Bare case** — legacy, communicates no intent:

```systemverilog
// Legacy — flag as P2
case (state)
  IDLE: ...
  RUNNING: ...
endcase
// Does the designer intend all cases covered? Unknown.
```

**unique if / priority if** — same semantics for if-else chains:

```systemverilog
unique if (sel == 2'b00)      out = a;
else if (sel == 2'b01)        out = b;
else if (sel == 2'b10)        out = c;
else                          out = d;
```

</case_statements>

<port_declarations>

**ANSI-style port declarations** (in the module header):

```systemverilog
// Idiomatic: ANSI-style
module uart_tx #(
  parameter int BAUD_RATE = 115200,
  parameter int DATA_BITS = 8
)(
  input  logic                  clk,
  input  logic                  rst_n,
  input  logic [DATA_BITS-1:0]  tx_data,
  input  logic                  tx_valid,
  output logic                  tx_ready,
  output logic                  tx
);
```

```systemverilog
// Legacy: non-ANSI — flag as P2
module uart_tx(clk, rst_n, tx_data, tx_valid, tx_ready, tx);
  parameter BAUD_RATE = 115200;
  input        clk;
  input        rst_n;
  input  [7:0] tx_data;
  // ...
endmodule
```

**Named port connections**:

```systemverilog
// Idiomatic: named connections
uart_tx #(
  .BAUD_RATE (115200),
  .DATA_BITS (8)
) u_uart_tx (
  .clk      (clk),
  .rst_n    (rst_n),
  .tx_data  (tx_data),
  .tx_valid (tx_start),
  .tx_ready (tx_ready),
  .tx       (uart_tx_pin)
);

// Also acceptable: implicit named connections when names match
uart_tx u_uart_tx (
  .clk,           // connects to local 'clk'
  .rst_n,         // connects to local 'rst_n'
  .tx_data,       // connects to local 'tx_data'
  .tx_valid (tx_start),  // different name — explicit
  .tx_ready,
  .tx       (uart_tx_pin)
);

// Legacy — flag as P1
uart_tx u_uart_tx (clk, rst_n, tx_data, tx_start, tx_ready, uart_tx_pin);
```

**Unconnected ports**:

```systemverilog
// Explicit unconnected (preferred)
.unused_output ()

// Never leave ports silently unconnected via positional mapping
```

</port_declarations>

<packages_and_imports>

**Package for shared definitions**:

```systemverilog
package bus_pkg;
  typedef enum logic [1:0] {
    READ, WRITE, IDLE
  } cmd_e;

  typedef struct packed {
    logic [31:0] addr;
    logic [31:0] data;
    cmd_e        cmd;
  } bus_req_t;

  localparam int TIMEOUT_CYCLES = 1000;

  function automatic int clog2_safe(int value);
    return (value <= 1) ? 1 : $clog2(value);
  endfunction
endpackage
```

**Import patterns**:

```systemverilog
// Preferred: wildcard import (in module scope)
module controller
  import bus_pkg::*;
#(
  // parameters
)(
  // ports
);

// Also acceptable: specific imports
import bus_pkg::bus_req_t;
import bus_pkg::cmd_e;
```

**Anti-patterns**:

| Pattern                        | Problem                    | Fix                                 |
| ------------------------------ | -------------------------- | ----------------------------------- |
| `` `define CMD_READ 2'b00 ``   | Global namespace pollution | `enum` in a `package`               |
| `` `include "types.vh" ``      | Fragile, order-dependent   | `package` + `import`                |
| Duplicate typedef across files | Maintenance drift          | Single `package`, import everywhere |
| `function` outside a package   | Not reusable               | Move to `package`                   |

</packages_and_imports>

<interfaces>

**Interface for complex bus protocols**:

```systemverilog
interface axi_lite_if #(
  parameter int ADDR_WIDTH = 32,
  parameter int DATA_WIDTH = 32
)(
  input logic clk,
  input logic rst_n
);
  logic [ADDR_WIDTH-1:0] awaddr;
  logic                  awvalid;
  logic                  awready;
  logic [DATA_WIDTH-1:0] wdata;
  logic                  wvalid;
  logic                  wready;
  // ...

  modport master (
    output awaddr, awvalid, wdata, wvalid,
    input  awready, wready
  );

  modport slave (
    input  awaddr, awvalid, wdata, wvalid,
    output awready, wready
  );
endinterface
```

**Using interfaces**:

```systemverilog
module axi_master (
  axi_lite_if.master bus
);
  always_comb begin
    bus.awaddr  = addr_reg;
    bus.awvalid = valid_reg;
  end
endmodule
```

**When to use interfaces**:

- Bus protocols with many signals (AXI, Wishbone, SPI)
- Signals that always travel together
- Reduces port list clutter

**When NOT to use interfaces**:

- Simple point-to-point signals (clock, reset, single data)
- When both Vivado and Quartus need full support (interface support varies at boundaries — test with both tools)

</interfaces>

<naming_conventions>

| Element         | Convention           | Examples                                |
| --------------- | -------------------- | --------------------------------------- |
| Signals         | `snake_case`         | `data_valid`, `byte_count`              |
| Modules         | `snake_case`         | `uart_tx`, `fifo_sync`                  |
| Instances       | `u_` prefix          | `u_uart_tx`, `u_fifo`                   |
| Parameters      | `UPPER_SNAKE_CASE`   | `DATA_WIDTH`, `DEPTH`                   |
| Localparams     | `UPPER_SNAKE_CASE`   | `ADDR_BITS`, `TIMEOUT`                  |
| Enum types      | `_e` suffix          | `state_e`, `cmd_e`                      |
| Struct types    | `_t` suffix          | `bus_req_t`, `pixel_t`                  |
| Typedef types   | `_t` suffix          | `addr_t`, `data_t`                      |
| Interfaces      | `_if` suffix         | `axi_lite_if`, `spi_if`                 |
| Packages        | `_pkg` suffix        | `bus_pkg`, `alu_pkg`                    |
| Clocks          | `clk` or `clk_<dom>` | `clk`, `clk_sys`, `clk_pixel`           |
| Resets          | `rst_n`              | `rst_n` (active-low, industry standard) |
| Active-low      | `_n` suffix          | `cs_n`, `oe_n`, `we_n`                  |
| Enables         | `_en` suffix         | `count_en`, `tx_en`                     |
| Register stage  | `_d` / `_q`          | `data_d` (input), `data_q` (output)     |
| Next-state      | `next_` prefix       | `next_state`, `next_count`              |
| Generate blocks | `gen_` prefix        | `gen_pipeline`, `gen_mux`               |

**Active-low reset convention**: SystemVerilog FPGA designs conventionally use `rst_n` (active-low). This aligns with most FPGA reset infrastructure.

**Avoid**:

- Hungarian notation (`w_data`, `r_valid`)
- Single-letter names except `i`, `j`, `k` for generate indices
- CamelCase for signals or modules
- `` `define `` for constants (use `localparam`)

</naming_conventions>

<generate_blocks>

**for-generate**:

```systemverilog
// Always label generate blocks
for (genvar i = 0; i < NUM_STAGES; i++) begin : gen_pipeline
  pipe_stage u_stage (
    .clk    (clk),
    .d_in   (pipe[i]),
    .d_out  (pipe[i+1])
  );
end
```

**if-generate**:

```systemverilog
if (USE_ASYNC_RESET) begin : gen_async_rst
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) q <= '0;
    else        q <= d;
  end
end else begin : gen_sync_rst
  always_ff @(posedge clk) begin
    if (!rst_n) q <= '0;
    else        q <= d;
  end
end
```

Key rules:

- Always label generate blocks (`: gen_name`)
- Use `genvar` for loop variables
- `generate`/`endgenerate` keywords are optional in SystemVerilog (omit them)
- Each branch of if-generate needs its own label

</generate_blocks>

<synthesizability>

**Latch prevention** — same principle as VHDL:

```systemverilog
// LATCH: missing else
always_comb begin
  if (enable) data_out = data_in;
  // What when enable == 0? Latch!
  // always_comb will warn, but always @(*) won't
end

// FIXED: default assignment
always_comb begin
  data_out = '0;  // default prevents latch
  if (enable) data_out = data_in;
end
```

**Width matching** — explicit sizing prevents bugs:

```systemverilog
// Idiomatic: explicit widths
logic [7:0] count;
count <= count + 8'd1;   // sized literal
count <= '0;              // fill with zeros (width-agnostic)
count <= '1;              // fill with ones

// Risky: implicit width
count <= count + 1;       // 1 is 32-bit — works but intent unclear
count <= 0;               // 32-bit zero assigned to 8-bit — tool truncates
```

**Sized literals**:

| Literal  | Meaning                       |
| -------- | ----------------------------- |
| `8'd255` | 8-bit decimal 255             |
| `4'hF`   | 4-bit hex F                   |
| `1'b1`   | 1-bit binary 1                |
| `'0`     | All zeros (context-width)     |
| `'1`     | All ones (context-width)      |
| `'x`     | All X (simulation don't-care) |

**Constructs to avoid in synthesizable code**:

| Construct            | Problem                        | Alternative                      |
| -------------------- | ------------------------------ | -------------------------------- |
| `#10 clk = ~clk;`    | Simulation-only delay          | Remove; use testbench for clocks |
| `initial begin`      | Not synthesizable (most tools) | Use reset logic                  |
| `force` / `release`  | Simulation-only                | Testbench only                   |
| `$display`, `$write` | Simulation-only                | Testbench only                   |
| `real`               | Not synthesizable              | Fixed-point with `logic`         |
| `dynamic array`      | Not synthesizable              | Fixed-size arrays                |

**Vivado + Quartus compatibility notes**:

- Both support the synthesizable subset of IEEE 1800-2017 well
- `interface` at top-level ports: Quartus may require flattening — test if used at boundaries
- `$clog2()`: fully supported by both
- `unique case`/`priority case`: both generate appropriate warnings
- `always_ff`/`always_comb`: both enforce correct semantics
- Assertion synthesis: limited — use for simulation, not synthesis-critical paths

</synthesizability>

<testbench_idioms>

**Testbench structure**:

```systemverilog
module tb_module_name;
  localparam int CLK_PERIOD = 10;  // ns

  logic clk = 1'b0;
  logic rst_n = 1'b0;

  // Clock generation
  always #(CLK_PERIOD/2) clk = ~clk;

  // DUT
  module_name u_dut (
    .clk,
    .rst_n,
    // ...
  );

  // Stimulus
  initial begin
    // Hold reset
    repeat (5) @(posedge clk);
    rst_n = 1'b1;
    @(posedge clk);

    // Test vectors
    // ...

    // End simulation
    $display("Test passed");
    $finish;
  end
endmodule
```

**Testbench-specific rules**:

- `initial` blocks are fine (testbench is not synthesized)
- `#delay` is fine for clock generation and stimulus timing
- Use `$display` / `$error` / `$fatal` for messages
- Name testbench module `tb_<module_name>`
- Use `$finish` or `$stop` to end simulation
- Prefer `@(posedge clk)` for synchronous timing rather than absolute `#` delays in stimulus
- Assertions (`assert`, `assume`, `cover`) are for testbenches

</testbench_idioms>

<legacy_verilog_patterns>

Patterns from Verilog-2001 (IEEE 1364-2001) to flag when reviewing SystemVerilog code:

| Legacy Verilog-2001             | Idiomatic SystemVerilog             | Priority | Why                                         |
| ------------------------------- | ----------------------------------- | -------- | ------------------------------------------- |
| `reg [7:0] data;`               | `logic [7:0] data;`                 | P2       | `logic` is the unified type                 |
| `wire valid;`                   | `logic valid;`                      | P2       | `logic` unless multi-driver                 |
| `always @(posedge clk)`         | `always_ff @(posedge clk)`          | P2       | Enforces non-blocking, catches mistakes     |
| `always @(*)`                   | `always_comb`                       | P2       | Auto-sensitivity, warns on latches          |
| `case (state)` (bare)           | `unique case (state)`               | P2       | Communicates intent, tool checks coverage   |
| Non-ANSI port declarations      | ANSI-style (ports in module header) | P2       | Cleaner, less error-prone                   |
| Positional port connections     | Named `.port(signal)` connections   | P1       | Fragile — breaks silently on reorder        |
| `` `define CONST 8 ``           | `localparam int CONST = 8`          | P1       | Scoped, typed, not global preprocessor      |
| `` `include "types.vh" ``       | `package` + `import`                | P1       | Order-independent, no duplicate definitions |
| `integer i;`                    | `int i;`                            | P2       | Shorter, same semantics for synthesis       |
| Manual `2**N` or bit-width calc | `$clog2(N)`                         | P1       | Correct, readable, synthesizable            |

**When NOT to flag legacy patterns**:

- File is explicitly Verilog-2001 (`.v` extension, product standard says Verilog)
- Legacy IP core that cannot be modified
- Vendor-provided primitives or wrappers

</legacy_verilog_patterns>
