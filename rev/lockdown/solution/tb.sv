`include "synth.v"

module tb;

    logic [31:0] a, b;
    wire  [31:0] c;
    logic [47:0] p;
    add asfd(.a(a), .b(b), .password(p), .c(c));

    initial begin


        p = 48'b011101010110111001001100001100000110001101001011;
        a = 2;
        b = 3;
        #10;
        $display("a = %d, b = %d, c = %d \n", a, b, c);
        a = 4;
        b = 7;
        #10;
        $display("a = %d, b = %d, c = %d \n", a, b, c);


    end

endmodule