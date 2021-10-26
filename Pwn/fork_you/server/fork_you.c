#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/types.h>
#include <signal.h>

// gcc -fstack-protector fork_you.c -o fork_you

// i assure you this is necessary
int client_fd;

void handle_client() {
    // we don't pass arguments around here, i'm a global individual
    char name[128];

    send(client_fd, "Welcome to forks anonymous, what's your name?: ", sizeof("Welcome to forks anonymous, what's your name?: "), 0);
    if (recv(client_fd, name, 0x128, 0) == 0) {
        // they closed the socket, literally how dare they
        return;
    }
    send(client_fd, "Actually I changed my mind, fork is awesome lmao get owned\n", sizeof("Actually I changed my mind, fork is awesome lmao get owned\n"), 0);

}



int main() {

    int listen_fd, child, enable=1;
    struct sockaddr_in listen_addr, client_addr;
    size_t sockaddr_len = sizeof(struct sockaddr_in);
    
    // my generosity is unmatched
    dup2(1,2);
    signal(SIGCHLD, SIG_IGN);
    
    puts("The fork syscall is my sleep paralysis demon. On those cold winter evenings where the warmth of my bedsheets does little to stave off the freezing darkness of the night, I see it there at the end of my bed. Its bulging instructions staring into my soul as I stir, unable to move, burrowing into my deepest thoughts looking for any spark of process separation or individuality, ready to stamp it out at the first glint of sandboxing in my eye. It opens its parent-child relationship. A fleeting cold sweat breaks out all over my limp body as I see it move towards me, its evanescent form glowering menacingly. Unable to move or react I summon all my bodily strength and shout the one thing I know will ward it off, the one phrase which will keep me safe from its nefarious clutches, the inescapable force that is the process hierarchy, \"Threading is built into the C standard library\" I scream, as forks pearly-white form starts to dissipate in front of my eyes. Waking up and giving the room a quick once-over to ensure the dread-inducing presence has vacated, I go back to sleep. Forking sleep paralysis man.");
    
    memset(&listen_addr, sizeof(struct sockaddr_in), 0);
    memset(&client_addr, sizeof(struct sockaddr_in), 0);
    
    listen_addr.sin_family = AF_INET;
    listen_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    listen_addr.sin_port = htons(5000);
    
    if ((listen_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        puts("no more socket");
        exit(1);
    }
    
    if (setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int))) {
        puts("no more reuseaddr");
        exit(1);
    }
    
    if (bind(listen_fd, (const struct sockaddr *)(&listen_addr), sizeof(listen_addr))) {
        puts("no more binding");
        exit(1);
    }
    
    if (listen(listen_fd, 10)) {
        puts("no more listening");
        exit(1);
    }
    
    while (1) {
    
        if ((client_fd = accept(listen_fd, (struct sockaddr *)(&client_addr), (socklen_t *)(&sockaddr_len))) < 0) {
            puts("no more accepting");
            exit(1);
        }
    
        child = fork();
    
        if (child == -1) {
            puts("cope child fail cope");
            exit(1);
        }
        
        else if (child == 0) {
            // this is the child
            handle_client();
            send(client_fd, "Get out\n", sizeof("Get out\n"), 0);
            printf("1\n");
            close(client_fd);
            printf("2\n");
            exit(0);            
        }
        
        else {
            // this is the parent, close connection so child can have it
            close(client_fd);
            continue;

        }
    
    }

}

