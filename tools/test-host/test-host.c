#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

/* #define LOCAL_IP "<REMOTE IP>" */
#define LOCAL_PORT 0
#define REMOTE_PORT 80

int main(int argc, char **argv)
{
    int sock;
    struct sockaddr_in local, remote;

    if (argc < 2) {
        printf("Usage: %s REMOTE_HOST [REMOTE_PORT]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    /* Setup args */
    memset(&remote, 0, sizeof(remote));
    remote.sin_family = AF_INET;
    if ( inet_pton(AF_INET, argv[1], &remote.sin_addr) < 0 ) {
        perror("inet_pton()");
        exit(EXIT_FAILURE);
    }
    /* host and port */
    if (argc > 2) {
        remote.sin_port = htons(atoi(argv[2]));
    } else {
        remote.sin_port = htons(REMOTE_PORT);
    }

    memset(&local, 0, sizeof(local));
    local.sin_family = AF_INET;
    local.sin_port = htons(LOCAL_PORT);

    /* Create TCP socket */
    if ( (sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0 ) {
        perror("Cannot create socket");
        exit(EXIT_FAILURE);
    }

    /* Bind to socket */
    if ( inet_pton(AF_INET, LOCAL_IP, &(local.sin_addr)) < 0 ) {
        perror("inet_pton()");
        close(sock);
        exit(EXIT_FAILURE);
    }
    if ( bind(sock, (struct sockaddr *)&local, sizeof(local)) ) {
        perror("bind to socket");
        close(sock);
        exit(EXIT_FAILURE);
    }

    /* Try to connect */
    if ( connect(sock, (struct sockaddr *)&remote, sizeof(remote)) < 0 ) {
        perror("connect()");
        close(sock);
        exit(EXIT_FAILURE);
    }

    /* Shutting down connection */
    if ( shutdown(sock, SHUT_RDWR) < 0 ) {
        perror("shutdown()");
        close(sock);
        exit(EXIT_FAILURE);
    }

    close(sock);
    return 0;
}
