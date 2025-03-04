`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02/23/2025 09:01:15 PM
// Design Name: 
// Module Name: state_machine
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module state_machine(
    input wire clk,
    input wire rst,
    input wire [13:0] write_addr,
    input wire core_num,
    output wire[13:0] read_addr,
    output reg start_task,//read
    output reg cic_en,
    output reg load_cic,
    output reg store_cic,
    output wire [7:0] pixel_addr,
    output reg [3:0] cic_sub_addr,
    output reg store_e_data,
    output wire [13:0] temp_read_addr
    
//    output
    );
    parameter idle=0, pixel_load=1, run_cic=2, pix_inc=3,task_cmp=4,cic_load=5,cic_store=6;
   
    reg [3:0] state=0;
    reg task_started=0;
    reg [11:0] cic_counter=0;
    reg[13:0] read_start=0;
    wire [7:0] pixel_offset;
    reg [7:0] pixel_counter=0;
    reg [3:0] block_counter=0;
    
    assign pixel_offset=core_num?128:0;
    assign pixel_addr = pixel_offset+pixel_counter;
    assign temp_read_addr = read_start;
    
    assign read_addr=cic_counter+read_start;
    always @(posedge clk) begin
        if(rst) begin 
            start_task<=0;
            
        end else begin
                   
            if((write_addr==0 ||write_addr==4096||write_addr==8192||write_addr==12288 )&& write_addr-read_start>4096 && !task_started) begin
                start_task<=1;
            end else if (task_started) begin
                start_task<=0;
            end
        end
       
    end
    
    always @(posedge clk or posedge rst) begin
        if(rst) begin
            state<=idle;
            cic_counter<=0;
            read_start<=0;
            cic_en<=0;
            pixel_counter<=0;
            load_cic<=0;
            store_cic<=0;
            cic_sub_addr<=0;
            block_counter<=0;
            store_e_data<=0;
        end else begin 
            case (state)
                    idle: begin
                             if(start_task) begin 
                                state<=pixel_load;
                                pixel_counter<=0;
                                task_started<=1;
                             
                             end
                         end
                         
                    pixel_load: begin
                        store_cic<=0;
                        cic_counter<=0;
                        state<=cic_load;
                        cic_sub_addr<=0;
                        
                        end
                        
                    cic_load: begin 
                        load_cic<=1;
                        if(load_cic) begin 
                            if(cic_sub_addr<15) begin 
                                cic_sub_addr<=cic_sub_addr+1;
                            end else begin 
                                load_cic<=0;
                                cic_sub_addr<=0;
                                state<=run_cic;
                            end
                        
                        end
                        
                    end
                    
                    run_cic: begin
                        cic_en<=1;
//                        load_cic<=0;
                        if(cic_counter<4095) begin
                            cic_counter<=cic_counter+1;
                        end else begin 
                            if(block_counter==15) begin 
                                store_e_data<=1;
                            end
                            cic_counter<=0;
                            state<=cic_store;
                        end
                    
                    
//                         state = three;
                    end
                    cic_store: begin 
                        cic_en<=0;
                        store_cic<=1;
                        store_e_data<=0;
                        if(store_cic) begin 
                            if(cic_sub_addr<15) begin 
                                cic_sub_addr<=cic_sub_addr+1;
                            end else begin 
                                store_cic<=0;
                                cic_sub_addr<=0;
                                state<=pix_inc;
                            end
                        
                        end
                        
                        
                    end
                    pix_inc: begin
                                                
                         if(pixel_counter<255) begin //switch pixels
                             pixel_counter<=pixel_counter+1;                         
                             state<= pixel_load;
                             
                             
                         end else begin 
                            pixel_counter<=0;
                            task_started<=0;
                            state<=task_cmp;
                            read_start<=read_start+4096;
                         end
                         
                     end
                     
                     task_cmp: begin 
                     
                        block_counter<=block_counter+1;

                        state<=idle;
                     
                     end
               endcase
        
        
        
        
        end
    
    end
    
    
    
endmodule



    .clk,
    .rst,
    .in,
    .int_ena,
    .dif_ena,
    .memory_data_out,
    .reg_sel,
    .reg_load_en,
    .memory_data_in,
    .out,
    .debug_out