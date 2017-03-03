#!/bin/bash

### BEGIN INIT INFO
# Provides:          train-semaphore
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Semaphore software for toy railway
### END INIT INFO

SEMAPHORE_DIR=/D/Projects/Idea/Pimaphore
SEMAPHORE_SCRIPT=${SEMAPHORE_DIR}/Main.py
PIDFILE=${SEMAPHORE_DIR}/pid.lock
LOG=${SEMAPHORE_DIR}/log.txt

start() {
        echo -n "Starting semaphore: "
        if [ -f ${PIDFILE} ]; then
            PID=`cat ${PIDFILE}`
            kill -0 ${PID}
            if [ $? == 0 ]; then
                echo "samaphore is already running: $PID"
                exit 2;
            else
                echo "removing stale pid file $PIDFILE"
                rm ${PIDFILE}
            fi
        fi
        cd ${SEMAPHORE_DIR}
        python ${SEMAPHORE_SCRIPT} 2>&1 > ${LOG} &
        RETVAL=$?
        echo $! > ${PIDFILE}
        return $RETVAL
}

stop() {
        echo -n "Shutting down semaphore: "
        if [ -f ${PIDFILE} ]; then
            PID=`cat ${PIDFILE}`
            kill -0 ${PID}
            if [ $? == 0 ]; then
                echo "using pid file to stop pid: $PID"
                kill -SIGKILL ${PID};
                rm ${PIDFILE}
            else
                echo "no process found, removing stale pid file $PIDFILE"
                rm ${PIDFILE}
            fi
        fi
        return 0
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage:  {start|stop|restart}"
        exit 1
        ;;
esac
exit $?
