module AND (
    input A,
    input B,
    output Y
);
    assign Y = A & B;
endmodule

module OR (
    input A,
    input B,
    output Y
);
    assign Y = A | B;
endmodule

module XOR (
    input A,
    input B,
    output Y
);
    assign Y = A ^ B;
endmodule

module NOT (
    input A,
    output Y
);
    assign Y = ~A;
endmodule

module NAND (
    input A,
    input B,
    output Y
);
    assign Y = ~(A & B);
endmodule

module NOR (
    input A,
    input B,
    output Y
);
    assign Y = ~(A | B);
endmodule

module XNOR (
    input A,
    input B,
    output Y
);
    assign Y = ~(A ^ B);
endmodule

module BUF (
    input A,
    output Y
);
    assign Y = A;
endmodule