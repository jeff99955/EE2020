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
    char addr[128] = "linux8.csie.org";
    char filepath[128], buf[4096];
    int port = 1268;
    struct sockaddr_in servaddr;
    int sockfd;
    int tmp;
    gethostname(addr, sizeof(addr));
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    puts("socket successfully created");
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(port);
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (void *)&tmp, sizeof(tmp));
    if(bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) > 0) {
        puts("bind error");
        exit(-1);
    }
    puts("bind success");
    if (listen(sockfd, 16) != 0){
        puts("listen error");
        exit(1);
    }
    puts("listening");

    struct sockaddr_in cliaddr;
    int clifd, clilen = sizeof(cliaddr),n;
    FILE *fp;
    clifd = accept(sockfd, (struct sockaddr *)&cliaddr, (socklen_t *)&clilen);
    printf("clifd = %d\n", clifd);
    if(recv(clifd, buf, sizeof(buf), 0) == 0)
        exit(1);
    strcpy(filepath, buf);
    printf("filepath is %s\n", filepath);
    fp = fopen(filepath, "wb");
    while(1){    
        if((n = recv(clifd, buf, sizeof(buf), 0)) == 0){
            puts("done");
            exit(0);
        }
        fwrite(buf, n, 1, fp);
    }
}
