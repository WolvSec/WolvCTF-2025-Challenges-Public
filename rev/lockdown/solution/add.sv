module add (
    input logic  [31:0] a,
    input logic  [31:0] b,
    input logic  [47:0] password,
    output logic [31:0] c
);

assign c = a + b;

endmodule