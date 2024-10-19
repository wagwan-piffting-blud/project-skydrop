import sys

def decrypt(ciphertext):
    plaintext = ""
    order = [0, 3, 6, 8, 7, 1, 4, 5, 2]
    indices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '!', '@']

    num_cycles = len(ciphertext) // 108

    cipher2 = ""
    
    for myind in indices:
        for idx, letter in enumerate(ciphertext):
            wrapped_index = (ciphertext.index(myind) + idx * 12) % len(ciphertext)
            cipher2 += ciphertext[wrapped_index]
        heartbeat = ''
    
        for idx1 in order:
            heartbeat += cipher2[idx1]
        idx1 = 0
        
        print(''.join(heartbeat).replace('$', '10').replace('!', '11').replace('@', '12'))
        
        cipher2 = ""
    

ciphertext = "8TRI__T__ED__7ARO__CN_GG_F6BNA_ROE_AST_5RKHYLUAL_A_A4SOE$DIE_AL__3RTC!REEC_L__2N_C@NTR_RC_W1U_N9AEIY_T_UKR_R"
plaintext = decrypt(ciphertext)
sys.exit()