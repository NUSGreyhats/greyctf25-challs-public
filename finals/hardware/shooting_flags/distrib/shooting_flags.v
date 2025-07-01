module shooting_flags #(
    parameter CLK_FREQ = 48_000_000 // not the actual clock frequency
) (
    input clk, input got_commanding_officer, output [7:0] cats
);
    //// Shooting Rate ////////////////////////////////////////////////////
    // Create a new clock
    reg [31:0] counter_shooting = 0;
    reg clk_shooting = 0;
    always @ (posedge clk) begin
        counter_shooting <= counter_shooting + 1;
        if (counter_shooting == CLK_FREQ/30) begin
            clk_shooting <= ~clk_shooting;
            counter_shooting <= 0;
        end
    end
    
    reg [31:0] counter_wayang = 0;
    reg clk_wayang = 0;
    always @ (posedge clk) begin
        counter_wayang <= counter_wayang + 1;
        if (counter_wayang == CLK_FREQ/4) begin
            clk_wayang <= ~clk_wayang;
            counter_wayang <= 0;
        end
    end
    //// Shooting /////////////////////////////////////////////////////////
    localparam FLAG_LEN = 25;
    reg [7:0] flag[FLAG_LEN];
    always @ (*) begin
        // lmao no flag
    end

    reg [7:0] shooting = 8'b101;
    reg [7:0] shooting_flag = 8'b0;
    reg [$clog2(FLAG_LEN)-1:0] counter_display = 0;
    always @ (posedge clk_shooting) begin
        shooting <= shooting << 1 | shooting[7];
    end
    always @ (posedge clk_wayang) begin
        shooting_flag <= (
            flag[counter_display] << counter_display % 8 | 
            flag[counter_display] >> (8-counter_display%8)
        );
        counter_display <= (counter_display + 1) % FLAG_LEN;
    end
    /// LED output //////////////////////////////////////////////////////
    assign cats = (got_commanding_officer ? shooting_flag : shooting);

endmodule

/* in the top module it is used as such

wire [7:0] chall_shootingflags_leds;
shooting_flags #(.CLK_FREQ(CLK_FREQ)) chall_shootingflags (
    .clk(clk), 
    .got_commanding_officer(~btn[2]),
    .cats(chall_shootingflags_leds)
);

*/