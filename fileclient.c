#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

int main(int argc, char **argv){
    alarm(10);
    char *addr  = argv[1], *filepath = argv[2];
    char buf[4096];
    int port = 1268;
    struct sockaddr_in servaddr;
    int sockfd, n, connected = 0;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(addr);
    servaddr.sin_port = htons(port);
    for(int iter = 0; iter < 5; iter++) {
        n = connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr));
        if (n != -1)  {
            connected = 1;
            break;
        }
        puts("connection error");
        sleep(1);
    }
    if(!connected)
        exit(1);
    puts("connected");
    send(sockfd, filepath, strlen(filepath), 0);
    int ffd = open(filepath, O_RDONLY);
    while( (n = read(ffd, buf, sizeof(buf))) > 0 ) {
        send(sockfd, buf, n, 0);
    }
    return 0;
}
