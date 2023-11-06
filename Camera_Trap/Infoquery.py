#!/usr/bin/env python3

""" This program sends a response whenever it receives the "INF" """

import time
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD2 as BOARD
import sqlite3

BOARD.setup()
BOARD.reset()
#parser = LoRaArgumentParser("Lora tester")


class mylora(LoRa2):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        #print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True )# Receive INF
        print ("Receive: ")
        mens=bytes(payload).decode("utf-8",'ignore')
        mens=mens[2:-1] #to discard \x00\x00 and \x00 at the end
        print(mens)
        BOARD.led_off()
        

        #----------------------Vuyisa -------------
        if mens == 'bite':
            people= 'shit' # rest of the code is comming
        
        else:
            #----------------------Vuyisa-------------------
            # Connect to the SQLite database (or create it if it doesn't exist)
            conn = sqlite3.connect('CameraTrapRecords.db')
            # Create a cursor object to interact with the database
            cursor = conn.cursor()
            try:
                # Execute the user's SQL query
                cursor.execute(mens+'ORDER BY RANDOM() LIMIT 10')

                # Fetch and print the results (if any)
                results = cursor.fetchall()
                #for row in results:
                #    print(row)

                # Commit the transaction
                conn.commit()

            except Exception as e:
                print("Error:", str(e))
                conn.rollback()  # Rollback the transaction in case of an error

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print("Received data request INF")
            time.sleep(2)
            print ("Send mens: DATA RASPBERRY PI")
            for row in results:
                results_bytes = results[row].encode("ascii")
                payload_list = [255, 255, 0, 0] + list(results_bytes) + [0]
                self.write_payload(payload_list)
                #self.write_payload([255, 255, 0, 0, 68, 65, 84, 65, 32, 82, 65, 83, 80, 66, 69, 82, 82, 89, 32, 80, 73, 0]) # Send DATA RASPBERRY PI
                self.set_mode(MODE.TX)
                time.sleep(0.2)
        time.sleep(2)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):          
        while True:
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            while True:
                pass;
            
# 
# lora = mylora(verbose=False)
# #args = parser.parse_args(lora) # configs in LoRaArgumentParser.py
# 
# #     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
# lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
# lora.set_bw(BW.BW125)
# lora.set_coding_rate(CODING_RATE.CR4_8)
# lora.set_spreading_factor(12)
# lora.set_rx_crc(True)
# #lora.set_lna_gain(GAIN.G1)
# #lora.set_implicit_header_mode(False)
# lora.set_low_data_rate_optim(True)
# 
# #  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
# #lora.set_pa_config(pa_select=1)
# 
# 
# 
# assert(lora.get_agc_auto_on() == 1)
# 
# try:
#     print("START")
#     lora.start()
# except KeyboardInterrupt:
#     sys.stdout.flush()
#     print("Exit")
#     sys.stderr.write("KeyboardInterrupt\n")
# finally:
#     sys.stdout.flush()
#     print("Exit")
#     lora.set_mode(MODE.SLEEP)
# BOARD.teardown()
