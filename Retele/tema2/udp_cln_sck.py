# Udp client

from Retele.tema2.app import *

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(3)
client_seq = make_sequence_number()
server_seq = None

def handshake_req():
    global client_sock, client_seq,server_seq
    new_header = create_header(SYN_flag, client_seq, ack_num=0)

    print(f"Sending a Syn request to Server {server_address[0]}:{server_address[1]}, client_seq_num = {client_seq}")

    client_sock.sendto(new_header, server_address) #SYN

    server_header, adresa = client_sock.recvfrom(Packet_Size) #Receive SYN-ACK

    sv_seq, sv_ack, flags = get_header_info(server_header)
    print(f'Receiving a syn_ack request from Server {server_address[0]}:{server_address[1]}, sv_seq_num = {sv_seq}')

    if flags & (SYN_flag | ACK_flag):  # last part of a 3-way handshake
        client_seq += 1
        new_flags = ACK_flag
        last_ack = next_seq_num(sv_seq)
        server_seq = last_ack
        last_header = create_header(new_flags,client_seq,last_ack)
        print(f'Sending ack to Server {server_address[0]}:{server_address[1]}, client_seq = {client_seq}')
        client_sock.sendto(last_header,server_address) #Send ACK

def terminate_clt():
    global client_sock,client_seq,server_seq

    #Fin_Wait_1
    ack_header, sv_add = client_sock.recvfrom(Packet_Size)
    sv_seq, ack_num, flag = get_header_info(ack_header)

    if ack_num != client_seq+1:
        print("Error receiving ack_num")
        return -1

    client_seq += 1

    #Fin_Wait_2

    ack_header, sv_add = client_sock.recvfrom(Packet_Size)
    sv_seq, ack_num, flag = get_header_info(ack_header)

    if not flag & FIN_flag:
        print("Error receiving Fin flag")
        return -1

    last_header = create_header(0,client_seq,next_seq_num(sv_seq))
    sent = client_sock.sendto(last_header,server_address)

    server_seq = None
    client_sock.close()


if __name__ == "__main__":

    handshake_req()

    while True:

        print("Server seq Num ",server_seq)
        print("Client seq Num ",client_seq)

        message = input("Enter your message: ")

        if message == "terminate":
            fin_header = create_header(FIN_flag,client_seq)
            client_sock.sendto(fin_header,server_address)
            terminate_clt()
            exit()

        ack_num = 65536
        expected = 0
        while client_seq!=expected:
            message_header = create_header(PSH_flag, client_seq, 0, message)

            sent = client_sock.sendto(message_header, server_address)
            print(f"Trimitem {sent} octeti catre {server_address[0]}:{server_address[1]}")

            expected = next_seq_num(client_seq,len(message))

            ack_header, sv_address = client_sock.recvfrom(Packet_Size)
            sv_seq, ack_num, flags = get_header_info(ack_header)

            print(f'Receptionam cati octeti a primit serverul:')
            print(f'Serverul a primit {ack_num - client_seq + 5} octeti')

            client_seq = ack_num
            server_seq = sv_seq

            if client_seq!=expected:
                print("Serverul nu a primit toata informatia, Retrimitem")
