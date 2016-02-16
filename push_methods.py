def qpush_send(user, msg):
    print "Qpush"
    print "Send to :" + user.name
    print "msg : {" + msg + "}"

def pushbullet_send(user, msg):
    print "Pushbullet"
    print "Send to :" + user.name
    print "msg : {" + msg + "}"

SEND_METHOD = {"qpush":qpush_send, "pushbullet":pushbullet_send}