# Udp server
from Retele.tema2.app import *

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(server_address)
server_seq = make_sequence_number()
client_seq = None



print(f"Server started on {serverAddress}:{serverPort}")


def handshake():
    global server_sock, server_seq, client_seq
    header, client_address = server_sock.recvfrom(Packet_Size)
    clt_seq, la_misto, flags = get_header_info(header)

    print(f"Receiving a syn request from {client_address[0]}:{client_address[1]}, client_seq_num = {clt_seq}")
    # A sync request is made
    if flags & SYN_flag:
        # do a SYN_ACK
        server_ack = next_seq_num(clt_seq)
        client_seq = server_ack
        flags = SYN_flag | ACK_flag
        syn_ack_header = create_header(flags, server_seq, server_ack)
        print(f"Sending a syn_ack request to {client_address[0]}:{client_address[1]} sv_seq_num = {server_seq}")
        sent = server_sock.sendto(syn_ack_header, client_address)

        last_seq, last_ack, last_flags = get_header_info(server_sock.recvfrom(Packet_Size)[0])
        if last_flags & ACK_flag:
            print(f"Receiving ack from {client_address[0]}:{client_address[1]}, client_seq_num = {last_seq}")
            server_seq = last_ack



def terminate_sv(header,client_add):
    global server_sock,server_seq,client_seq

    clt_seq, ack_num, flag = get_header_info(header)
    ack_num = next_seq_num(clt_seq)
    
    #Fin_wait_1
    ack_fin_header = create_header(ACK_flag,server_seq,ack_num)
    sent = server_sock.sendto(ack_fin_header,client_add)

    time.sleep(1.5) #1.5 seconds to sleep until sending fin response

    #Fin_wait_2
    fin2_header = create_header(FIN_flag,server_seq,ack_num)
    sent = server_sock.sendto(fin2_header,client_add)

    time.sleep(1.5)
    #Time_wait
    header, client_add = server_sock.recvfrom(Packet_Size)

    print(f"Successfully terminated connection with {client_add[0]}:{client_add[1]}\n")
    clt_seq = None
    return server_seq+1, clt_seq


if __name__ == "__main__":


    while True:

        while client_seq is None:
            handshake()

        print("Server seq Num ",server_seq)
        print("Client seq Num ",client_seq)

        print("\nWaiting...")
        header, client_address = server_sock.recvfrom(Packet_Size)
        clt_seq, ack_num, flag = get_header_info(header)

        if flag & FIN_flag:
            server_seq,client_seq = terminate_sv(header,client_address)

        if flag & PSH_flag:
            message = get_message(header)
            print(f'Am primit {len(header)} octeti de la {client_address[0]}:{client_address[1]}')

            ack_num = next_seq_num(clt_seq,len(header) - 5)
            server_seq += 1
            ack_header = create_header(ACK_flag,server_seq,ack_num)
            server_sock.sendto(ack_header,client_address)
            client_seq = ack_num
