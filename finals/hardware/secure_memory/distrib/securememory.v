// Code your design here
module regular_synchronous_memory(input clk, input [4:0] address, output reg [7:0] value);
	// memory retrieval
	always @ (posedge clk) begin // 10Hz
		value <= (
            // lmao you think i'll just give you the flag here? go extract it from your catcore.
			0
		);
	end
endmodule

module secure_memory(input clk, input [4:0] address, output [7:0] value);
	wire [4:0] mem_address;
	wire [7:0] mem_value;
	regular_synchronous_memory mem (clk, mem_address, mem_value);
	assign mem_address = address;
    assign value = ( mem_address == 5'd31 ? mem_value : "?" );
endmodule

/* 
At the top module
----------------------
assign chall_secmem_address = interconnect[4:0];
assign pmod_j2 = (
    mode == MODE_CHALL_SECURE_MEM ? chall_secmem_value : 
    8'bzzzzzzzz
);

Pinouts
-----------------------
LOCATE COMP "pmod_j2[0]" SITE "A14";
IOBUF PORT  "pmod_j2[0]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[1]" SITE "A13";
IOBUF PORT  "pmod_j2[1]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[2]" SITE "A12";
IOBUF PORT  "pmod_j2[2]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[3]" SITE "A11";
IOBUF PORT  "pmod_j2[3]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[4]" SITE "B14";
IOBUF PORT  "pmod_j2[4]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[5]" SITE "B13";
IOBUF PORT  "pmod_j2[5]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[6]" SITE "B12";
IOBUF PORT  "pmod_j2[6]" IO_TYPE=LVCMOS25;
LOCATE COMP "pmod_j2[7]" SITE "B11";
IOBUF PORT  "pmod_j2[7]" IO_TYPE=LVCMOS25;
*/
