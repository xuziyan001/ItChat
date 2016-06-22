#coding=utf8
import itchat.out as out
import itchat.log as log
from PluginTest import *

try:
    import plugin.tuling as tuling
    tuling.get_response('Hi', 'LittleCoder')
    TULING = True
except:
    TULING = False

PRINT_ON_CMD = True

def send_msg(client, toUserName, msg):
    if len(msg) > 5:
        if msg[:5] == '@fil@':
            try:
                with open(msg[5:]): pass
                client.send_file(msg[5:], toUserName)
            except:
                log.log('Send file %s failed'%msg[5:], False)
        elif msg[:5] == '@img@':
            try:
                with open(msg[5:]): pass
                client.send_image(msg[5:], toUserName)
            except:
                log.log('Send image %s failed'%msg[5:], False)
        elif msg[:5] == '@msg@':
            client.send_msg(toUserName, msg[:5])
        else:
            client.send_msg(toUserName, msg)
    else:
        client.send_msg(toUserName, msg)

def get_reply(msg, s, client, isGroupChat = False, cmdPrint = PRINT_ON_CMD):
    reply = ''
    if msg['MsgType'] == 'Text':
        if not isGroupChat and cmdPrint:
            out.print_line('%s: %s'%(s.find_nickname(msg['FromUserName']), msg['Content']))
        content = msg['Content']
        out.print_line('I received: %s' % content, True)
        # Plugins should be added in order as ('name', function)
        pluginOrder = [('vote', vote), ('autoreply', autoreply), ('tuling', tuling.get_response)]
        if isGroupChat: pluginOrder = [('autoreply', autoreply), ('tuling', tuling.get_response)]
        getReply = False
        for plugin in pluginOrder:
            if plugin[0] in (pluginList['msgdealers'] + pluginList['systemmodules']):
                r = plugin[1](content, client.storageClass, msg['FromUserName'])
                if r:
                    reply = r
                    getReply = True
                    break
        if not getReply: reply = '么么哒~'
    elif msg['MsgType'] == 'Map':
        return '什么鬼'
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s is at %s'%(s.find_nickname(msg['FromUserName']), msg['Content']))
    elif msg['MsgType'] == 'Picture':
        return '好酷哦!'
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent a picture [%s]'%(s.find_nickname(msg['FromUserName']), msg['Content']))
    elif msg['MsgType'] == 'Recording':
        return '不听不听不听'
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent a recording'%(s.find_nickname(msg['FromUserName'])))
    elif msg['MsgType'] == 'Card':
        return '哈喽, %s!'%msg['Content']
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent a business card of [%s]'%(s.find_nickname(msg['FromUserName']), msg['Content']))
    elif msg['MsgType'] == 'Sharing':
        return '"%s" 好酷!'%msg['Content']
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent a web about [%s]'%(s.find_nickname(msg['FromUserName']), msg['Content']))
    elif msg['MsgType'] == 'Attachment':
        return '"%s" 是啥哦!'%msg['Content']
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent an attachment: [%s]'%(s.find_nickname(msg['FromUserName']), msg['Location']))
    elif msg['MsgType'] == 'Video':
        return '老司机哦'
        #if not isGroupChat and cmdPrint:
        #    out.print_line('%s sent a video [%s]'%(s.find_nickname(msg['FromUserName']), msg['Content']))
    elif msg['MsgType'] == 'Note':
        if not isGroupChat and cmdPrint: out.print_line('通知: %s'%(msg['Content']))
    else:
        pass#out.print_line(str(msg))
    out.print_line('response: %s' % reply)
    return reply

def deal_with_msg(msg, s, client):
    if msg.has_key('FromUserName'):
        out.print_line('FromUserName: %s' % msg['FromUserName'], True)
    if msg.has_key('FromUserName') and msg['FromUserName'][:2] == '@@':
        try:
            r = grouptalking(msg, s, client, get_reply)
            send_msg(client, msg['FromUserName'], r)
        except:
            log.log('Send group chat failed', False)
    else:
        r = get_reply(msg, s, client)
        send_msg(client, msg['FromUserName'], r)
