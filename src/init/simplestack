#! /bin/sh
### BEGIN INIT INFO
# Provides:          /usr/sbin/python-simplestack
# Required-Start:    $remote_fs $network $syslog
# Required-Stop:
# X-Stop-After:      sendsigs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Python Milter
# Description:       Python milter
### END INIT INFO

# Based on default init from Francisco Freire <francisco.freire@locaweb.com.br>

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="python simplestack service"
NAME=simplestack

LOCASTACK=simplestack
LOCASTACK_BIN=/usr/sbin/python-simplestack
LOCASTACK_OPTIONS=""
LOCASTACK_PIDFILE=/var/run/simplestack.pid

SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x "$LOCASTACK_BIN" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Define LSB log_* functions.
. /lib/lsb/init-functions

do_start()
{
    DAEMON="$LOCASTACK_BIN"
    DAEMON_ARGS="$LOCASTACK_OPTIONS"
    PIDFILE="$LOCASTACK_PIDFILE"

    # Return
    #   0 if daemon has been started
    #   1 if daemon was already running
    #   other if daemon could not be started or a failure occured
    start-stop-daemon -b --start --quiet --exec $DAEMON -- $DAEMON_ARGS
}

do_stop()
{
    NAME="$LOCASTACK"
    PIDFILE="$LOCASTACK_PIDFILE"

    # Return
    #   0 if daemon has been stopped
    #   1 if daemon was already stopped
    #   other if daemon could not be stopped or a failure occurred
    start-stop-daemon --stop --quiet --signal KILL --retry=TERM/30/KILL/5 --pidfile $PIDFILE && rm $PIDFILE
}

#
# Tell rsyslogd to reload its configuration
#
do_reload() {
   NAME="$LOCASTACK"
   PIDFILE="$LOCASTACK_PIDFILE"
   start-stop-daemon --stop --signal HUP --quiet --pidfile $PIDFILE --name $NAME
}

create_xconsole() {
   XCONSOLE=/dev/xconsole
   if [ "$(uname -s)" = "GNU/kFreeBSD" ]; then
       XCONSOLE=/var/run/xconsole
       ln -sf $XCONSOLE /dev/xconsole
   fi
   if [ ! -e $XCONSOLE ]; then
       mknod -m 640 $XCONSOLE p
       chown root:adm $XCONSOLE
       [ -x /sbin/restorecon ] && /sbin/restorecon $XCONSOLE
   fi
}

sendsigs_omit() {
   OMITDIR=/lib/init/rw/sendsigs.omit.d
   mkdir -p $OMITDIR
   rm -f $OMITDIR/rsyslog
   ln -s $LOCASTACK_PIDFILE $OMITDIR/rsyslog
}

case "$1" in
 start)
   log_daemon_msg "Starting $DESC" "$LOCASTACK"
   create_xconsole
   do_start
   case "$?" in
       0) sendsigs_omit
          log_end_msg 0 ;;
       1) log_progress_msg "already started"
          log_end_msg 0 ;;
       *) log_end_msg 1 ;;
   esac

   ;;
 stop)
   log_daemon_msg "Stopping $DESC" "$LOCASTACK"
   do_stop
   case "$?" in
       0) log_end_msg 0 ;;
       1) log_progress_msg "already stopped"
          log_end_msg 0 ;;
       *) log_end_msg 1 ;;
   esac

   ;;
 reload|force-reload)
   log_daemon_msg "Reloading $DESC" "$LOCASTACK"
   do_reload
   log_end_msg $?
   ;;
 restart)
   $0 stop
   $0 start
   ;;
 status)
   status_of_proc -p $LOCASTACK_PIDFILE $LOCASTACK_BIN $LOCASTACK && exit 0 || exit $?
   ;;
 *)
   echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload|status}" >&2
   exit 3
   ;;
esac

:
