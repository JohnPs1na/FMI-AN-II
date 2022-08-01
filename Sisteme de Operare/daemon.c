#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <string.h>

#include "da_variables.h"

#define MAX_TASKS 10

int activeWorkers = 0;
int active[MAX_TASKS+1];
int priorities[MAX_TASKS+1];
int jobPid[MAX_TASKS+1];
char previousStatus[MAX_TASKS+1];
char* paths[MAX_TASKS+1];


FILE* logfp;
int workerShmFd;
void* workerData;
// 1b[status]1b[percent]4b[doneFiles]4b[totalDirs] | next job | ...

char** status; 
char** progress;
int** doneFiles;
int** doneDirectories;
// job statuses
// i -> preparing / initialization stage
// r -> in progress / running
// d -> done
// s -> suspended

void becomeDaemon() {
    pid_t pid;

    // fork off the parent process
    pid = fork();

    // error check
    if (pid < 0)
        exit(EXIT_FAILURE);

    // success: Let the parent terminate
    if (pid > 0)
        exit(EXIT_SUCCESS);

    // on success: The child process becomes session leader
    if (setsid() < 0)
        exit(EXIT_FAILURE);

    // fork off for the second time
    pid = fork();

    // an error occurred
    if (pid < 0)
        exit(EXIT_FAILURE);

    // success: Let the parent terminate
    if (pid > 0)
        exit(EXIT_SUCCESS);

    // set new file permissions
    umask(0);

    // change the working directory to the root directory
    chdir("/");

    // close all open file descriptors
    int x;
    for (x = sysconf(_SC_OPEN_MAX); x >= 0; x--) {
        close (x);
    }
    
    
}

void makeDirectories() {

    struct stat st;    
    if (stat("/tmp/dad", &st) == -1) {
        mkdir("/tmp/dad", 0700);
        mkdir("/tmp/dad/jobs", 0700);
        mkdir("/tmp/dad/status", 0700);
    }

}

void printPid() {
    FILE* fp = fopen(DAEMON_PID_PATH, "w");

    fprintf(fp, "%d\n", getpid());

    fclose(fp);
}

void openLogs() {

    int errfd = open(ERROR_LOG_PATH, O_RDWR | O_CREAT | O_APPEND | O_TRUNC, 0600);
    dup2(errfd, fileno(stderr));
    close(errfd);

    logfp = fopen(LOG_PATH, "w");
}

void stop(int signal) {

    fclose(logfp);

    munmap(workerData, getpagesize());
    close(workerShmFd);
    shm_unlink(WORKER_SHM_NAME);

    exit(0);
}

void setupSharedMem() {
    workerShmFd = shm_open(WORKER_SHM_NAME, O_CREAT | O_RDWR | O_TRUNC, S_IRUSR | S_IWUSR);

    if (workerShmFd < 0) {
        fprintf(stderr, "Error: Failed to open shared memory");
        stop(0);
    }

    if(ftruncate(workerShmFd, getpagesize()) == -1) {
        fprintf(stderr, "Error: Failed to resize shared memory");
        stop(0); 
    } 

    void* workerData = mmap(0, getpagesize(), PROT_READ | PROT_WRITE, MAP_SHARED, workerShmFd, 0);

    if(workerData == MAP_FAILED){
        fprintf(stderr, "Error: Failed to get memory map of worker data");
        stop(0);
    }

    status = malloc(sizeof(char*) * (MAX_TASKS+1));
    progress = malloc(sizeof(char*) * (MAX_TASKS+1));
    doneFiles = malloc(sizeof(int*) * (MAX_TASKS+1));
    doneDirectories = malloc(sizeof(char*) * (MAX_TASKS+1)); 


    for(int i = 1; i <= MAX_TASKS; ++i) {
        status[i] = (char*) (workerData + (i-1)*10);
        progress[i] = (char*) (workerData + (i-1)*10 +1);
        doneFiles[i] = (int*) (workerData + (i-1)*10 + 2);
        doneDirectories[i] = (int*) (workerData + (i-1)*10 + 6);
         
    }
}



int firstFreeId() {

    for(int i = 1; i <= MAX_TASKS; ++i) {
        if(!active[i]) {
            return i; 
        }
    }

    return -1;
}

int checkPath(char* path) {

    int newPathSize = strlen(path); 
    int existingSize;
    for(int i = 1; i <= MAX_TASKS; ++i) {

        if(active[i] == 0) continue;
        existingSize = strlen(paths[i]);
        int match = 1;
        
        if(newPathSize >= existingSize) {

            for(int j = 0; j < existingSize; ++j) {
                if(paths[i][j] != path[j]) {
                    match = 0;
                    break;
                }
            }
            
            if (match) {
                return i;
            }
        }
        
    }

    return 0;
}

void commandHandler(int signal) {

    FILE* fpi = fopen(INSTRUCTION_PATH, "r");
    FILE* outfp;

    int code;
    fscanf(fpi, "%d", &code);
    
    char id[3];
    char path[512];
    int callerPid;
    int processId;
    char statusWord[16];
    char currentStatus;

    switch(code) {

        case ADD: 

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");

            char prio[3];
            int pr;

            int newId = firstFreeId();

            sprintf(id, "%d", newId);
            fscanf(fpi, "%d", &pr);
            sprintf(prio, "%d", pr);
            fscanf(fpi, "%s", path);
            fscanf(fpi, "%d", &callerPid);

            if(newId == -1) {
                fprintf(outfp, "0\nError: Couldn't start new job.\nReason: Maximum amount(%d) of jobs reached.\nUse -r to remove jobs.", MAX_TASKS);
                break;
            }


            int result = checkPath(path);
            if(result) {
                fprintf(outfp, "0\nError: Couldn't start new job.\nReason: Directory already included in job with id %d on %s\n", result, paths[result]);
                break;
            } 

            ++activeWorkers;
            active[newId] = 1;
            priorities[newId] = pr;
            *status[newId] = 'i';
            *progress[newId] = 0;
            *doneFiles[newId] = 0;
            *doneDirectories[newId] = 0;     
			
            paths[newId] = malloc(sizeof(char)*strlen(path));
			strcpy(paths[newId], path);

			
            char* argv[] = {"diskanalyzer_job", path, id, prio, NULL};
            int pid = fork();

            if(pid == 0) {
                execve(DISKANALYZER_JOB_PATH, argv, NULL);
            } else {
                jobPid[newId] = pid;
            }

            fprintf(outfp, "0\nStarted new analysis job\nID = %d\nDirectory = %s\n", newId, path);
            

        break;

        case SUSPEND: 

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");
            
            fscanf(fpi, "%d", &processId);
        	fscanf(fpi, "%d", &callerPid);


            if(processId > MAX_TASKS || active[processId] == 0){
                fprintf(outfp, "0\nError: The job doesn't exist\n");
               
                break;
            }

            if(*status[processId] == 's'){
                fprintf(outfp, "0\nError: The job is already suspended\n");

                break;
            }

            if(*status[processId] == 'd'){
                fprintf(outfp, "0\nError: The job is already done\n");

                break;
            }

            previousStatus[processId] = *status[processId];
            *status[processId] = 's';
            kill(jobPid[processId], SIGSTOP);
            fprintf(outfp, "0\nJob suspended successfully\nID = %d\nDirectory = %s\n", processId, paths[processId]);
            
        break;
        
        case RESUME: 

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");

            fscanf(fpi, "%d", &processId);
        	fscanf(fpi, "%d", &callerPid);

            if(processId > MAX_TASKS || active[processId] == 0){
                fprintf(outfp, "0\nError: The job doesn't exist\n");
               
                break;
            }

            if(*status[processId] != 's'){
                fprintf(outfp, "0\nError: The job is already executing\n");

                break;
            }
            
            *status[processId] = previousStatus[processId];
            kill(jobPid[processId], SIGCONT);
            fprintf(outfp, "0\nJob resumed successfully\nID = %d\nDirectory = %s\n", processId, paths[processId]);

        break;
        
        case REMOVE:

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");

            fscanf(fpi, "%d", &processId);
        	fscanf(fpi, "%d", &callerPid);

            if(processId > MAX_TASKS || active[processId] == 0){
                fprintf(outfp, "0\nError: The job doesn't exist\n");
               
                break;
            }
            
            int switchFail = 0;
            statusWord[16];
            currentStatus = *status[processId];

            switch (currentStatus){
                case 'i': strcpy(statusWord, "PREPARING"); break;
                case 'r': strcpy(statusWord, "IN PROGRESS"); break;
                case 'd': strcpy(statusWord, "DONE"); break;
                case 's': strcpy(statusWord, "SUSPENDED"); break;
                default: 
                    fprintf(outfp, "0\nError: Unknown job status.\n");
                    switchFail = 1;
                break;
            }

            if(switchFail) {
                break;
            }

            active[processId] = 0;
            kill(jobPid[processId], SIGTERM);
            fprintf(outfp, "0\nJob removed successfully\nID = %d\nDirectory = %s\nStatus = %s\n", processId, paths[processId], statusWord);
            
        break;

        case INFO: 

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");

            fscanf(fpi, "%d", &processId);
        	fscanf(fpi, "%d", &callerPid);

            if(processId > MAX_TASKS || active[processId] == 0){
                fprintf(outfp, "0\nError: The job doesn't exist.\n");
                break;
            }

            currentStatus = *status[processId];
            statusWord[16];
            char priority[4];
            char percentage = *progress[processId];
            int fileNumber = *doneFiles[processId];
            int dirNumber = *doneDirectories[processId];
            
            int switchFail = 0;

            switch(priorities[processId]) {
                case 1: strcpy(priority,"*"); break;
                case 2: strcpy(priority,"**"); break;
                case 3: strcpy(priority,"***"); break;
                default: break;
            }

            switch (currentStatus){

                case 'i': strcpy(statusWord, "PREPARING"); break;
                case 'r': strcpy(statusWord, "IN PROGRESS"); break;
                case 'd': strcpy(statusWord, "DONE"); break;
                case 's': strcpy(statusWord, "SUSPENDED"); break;
                default: 
                    fprintf(outfp, "0\nError: Unknown job status.\n");
                    switchFail = 1;

                break;
            }

            if(switchFail) {
                break;
            }

            fprintf(outfp,"0\nJob %d | %s | %s -> %d%%", processId, priority, paths[processId], percentage); 
            fprintf(outfp," %s \t %d files %d directories\n", statusWord, fileNumber, dirNumber);


        break;

        case PRINT: 

            outfp = fopen(DAEMON_OUTPUT_PATH, "w");
            
            fscanf(fpi, "%d", &processId);
        	fscanf(fpi, "%d", &callerPid);

            if(processId > MAX_TASKS || active[processId] == 0){
                fprintf(outfp, "0\nError: The job doesn't exist\n");
               
                break;
            }

            if(*status[processId] != 'd'){
                fprintf(outfp, "0\nError: The job isn't done\n");

                break;
            }

            fprintf(outfp, "%d", processId);

        break;
        
        case LIST_ALL: 
        	outfp = fopen(DAEMON_OUTPUT_PATH, "w");

        	fscanf(fpi, "%d", &callerPid);

            int noJobs = 1;
            for(int i = 1; i <= MAX_TASKS; ++i) {
                if (active[i]) {
                    noJobs = 0;
                    break;
                } 
            }

            if(noJobs) {
                fprintf(outfp, "0\nError: There are no jobs\n");
                break;
            }

            fprintf(outfp,"0\n- Job | Prio |  Path  | Done% | Status |    \t \t Details -\n");
            
            for(processId = 1; processId <= MAX_TASKS; ++processId) {
                
                if(active[processId] == 0){
                    continue;
                }


                currentStatus = *status[processId];
                statusWord[16];
                char priority[4];
                char percentage = *progress[processId];
                int fileNumber = *doneFiles[processId];
                int dirNumber = *doneDirectories[processId];
                
                int switchFail = 0;

                switch(priorities[processId]) {
                    case 1: strcpy(priority,"*"); break;
                    case 2: strcpy(priority,"**"); break;
                    case 3: strcpy(priority,"***"); break;
                    default: break;
                }

                switch (currentStatus){

                    case 'i': strcpy(statusWord, "PREPARING"); break;
                    case 'r': strcpy(statusWord, "IN PROGRESS"); break;
                    case 'd': strcpy(statusWord, "DONE"); break;
                    case 's': strcpy(statusWord, "SUSPENDED"); break;
                    default: 
                        fprintf(outfp, "Error: Unknown job status.\n");
                        switchFail = 1;

                    break;
                }

                if(switchFail) {
                    break;
                }

                fprintf(outfp,"Job %d | %s | %s -> %d%%", processId, priority, paths[processId], percentage); 
                fprintf(outfp," %s \t %d files %d directories\n", statusWord, fileNumber, dirNumber);
                fprintf(outfp,"\n");
            }

        break;
        
        default: 
            fprintf(stderr,"Error: received unknown command code\n"); 
            
        break;
    } 

    fclose(outfp);
    kill(callerPid, SIGUSR1);
    fclose(fpi);
}


void setupSignals() {

    signal(SIGTERM, stop);   
    signal(SIGUSR1, commandHandler);
}


void initialize() {
    
    becomeDaemon();
    openLogs();
    setupSignals();
    setupSharedMem();
    makeDirectories();
    printPid();

}



void run() {

    while(1) {
        
        sleep(1);
    }
}

int main()
{
    initialize();

    run();

    return 0;
}


