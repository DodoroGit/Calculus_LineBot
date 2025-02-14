from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackEvent #功能
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction
from linebot.models import QuickReply, QuickReplyButton, MessageAction #快速選單需求

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uag49rgqvn1uvp:pb4fe20041055965267a7ed1167757a15d64b4e03a040366b1a80dffb0485710a@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dcgtm5lu6i86hk'
db = SQLAlchemy( app )

line_bot_api = LineBotApi('60+HwfpVRnTQL4/jNH4OfufuSttOqLjzpHv6I7zBspIIF4z08wsKcdTDBUqBUMY0BOfbmBS86tPuE4ea4TQJZO+qJI9Z3LOORjwl+Mt6tc9iMHkJrxVtO9Td+RC3prkLcKeD1ThBQhwzLMr0/IzB9AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cf1c33192308594d2b1ccd92ec6e26e0')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
liffid_1 = "2000558142-nkjxYLLE"   #登入介面
liffid_2 = "2000558142-RA5mNOOk"   #極限測驗
liffid_3 = "2000558142-Zk39166Y"   #連續測驗
liffid_4 = "2000558142-Vw8ZbWWP"   #微分測驗1
liffid_5 = "2000558142-7RPBwggW"   #微分測驗2
liffid_11= "2000558142-XxK8PMMz"   #微分應用測驗
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#極限﹐連續、微分重點整理
liffid_6 = "2000558142-OkMRNddp"  #極限重點整理
liffid_7 = "2000558142-5mx6d44Y"  #連續重點整理S
liffid_8 = "2000558142-rxGpbMM3"  #微分重點整理1
liffid_9 = "2000558142-gBy47GGB"  #微分重點整理2
liffid_10 ="2000558142-dzLyq99l"  #微分應用重點整理
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#登入介面
@app.route('/login')
def page1():
	return render_template('login.html', liffid = liffid_1 )
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#極限測驗目錄
@app.route('/limtest')
def limtest():
	return render_template('lim_test.html', liffid = liffid_2 )

#連續測驗目錄
@app.route('/conttest')
def conttest():
	return render_template('cont_test.html', liffid = liffid_3 )

#微分測驗目錄
@app.route('/difftest1')
def difftest1() :
    return render_template('diff_test1.html', liffid = liffid_4 )

@app.route('/difftest2')
def difftest2() :
    return render_template('diff_test2.html', liffid = liffid_5 )

@app.route('/diffApplytest')
def diffApplytest() :
    return render_template('diffapply_test.html', liffid = liffid_11 )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#重點整體
@app.route('/limPoint')
def limPoint():
    return render_template('lim_def.html', liffid = liffid_6 )
@app.route('/contPoint')
def contPoint():
    return render_template('cont_def.html', liffid = liffid_7 )
@app.route('/diffPoint1')
def diffPoint1():
    return render_template('diff_def1.html', liffid = liffid_8 )
@app.route('/diffPoint2')
def diffPoint2():
    return render_template('diff_def2.html', liffid = liffid_9 )
@app.route('/diffApply')
def diffApply():
    return render_template('diffapply_def.html', liffid = liffid_10)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route("/createdb")
def createdb():
    sql = """
    drop table if exists line_user, student_data, important_record, test_record, register_user ; 
    
    create table important_record( lineid varchar(100) not null, studentid varchar(50) not null, clicktype varchar(20) not null, readtime varchar(20) not null, readsequence varchar(20) not null ) ;
    create table test_record( lineid varchar(100) not null, studentid varchar(50) not null, Qnumber varchar(20) not null, answer varchar(20) not null, TF varchar(10) not null, usetime varchar(20) not null ) ;    
    create table register_user( lineid varchar(100) not null, studentid varchar(50) not null, studentclass varchar(20) not null, studentname varchar(20) not null, isregister varchar(10) not null ) ;
    """
    db.engine.execute( sql )
    
    return "資料表重建成功"

@app.route("/callback", methods=['POST', 'GET'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data( as_text = True ) 
    try :
        handler.handle( body, signature ) 
    except InvalidSignatureError :
        abort( 400 )
    return "OK"


@handler.add( MessageEvent, message = TextMessage )
def handle_message( event ):
    
    lineid  = event.source.user_id
    prompt = event.message.text
    
    if ( prompt == "@登入" ) :
        Login( event, lineid )
    elif ( prompt == "@重點整理" ) :
        Important( event, lineid )
    elif ( prompt == "@測驗區" ) :
        Test( event, lineid ) 
    elif ( prompt == "@查詢作答狀況" ) :
        Query( event, lineid )
    elif ( prompt[:5] == "登入資訊:" ) :  
        Login_Liff( event, prompt, lineid )
    elif ( prompt[:7] == "本次作答紀錄:" ) :  
         manageForm_test( event, prompt, lineid )
    elif ( prompt[2:6] == "重點整理" ) :
        ImportantChoice( event, prompt, lineid )
    elif ( prompt[4:8] == "重點整理" ) :
        ImportantChoice( event, prompt, lineid )
    elif ( prompt[2:5] == "測驗區" ) :
        TestChoice( event, prompt, lineid )
    elif ( prompt[4:7] == "測驗區" ) :
        TestChoice( event, prompt, lineid ) 
    elif ( prompt[:4] == "閱讀重點" ) :
        ImportantReadTime( event, prompt, lineid )
    elif ( prompt[:21] == "rick871218.userappend" ) :
        Append_User( event, prompt, lineid ) #rick871218.userappend.班級.姓名.學號


@handler.add( PostbackEvent )
def Login( event, lineid ) :
    try :
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            if ( isregister == "True" ) :
                message = TextSendMessage( text = "您已登入!" )
            
            cursor.close()
        except :
            message = TemplateSendMessage( 
                alt_text = "登入", 
                template = ButtonsTemplate( 
                    thumbnail_image_url = "https://i.imgur.com/NWOujQR.png",
                    title = "登入",
                    text = "請輸入班級、學號、姓名",
                    actions = [ URITemplateAction( label = "個人資料", uri="https://liff.line.me/" + liffid_1) ]
                    )
            )
            
        line_bot_api.reply_message( event.reply_token, message )

        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text="發生錯誤 !" ) )

def Login_Liff( event, prompt, lineid ) :
    try :
        flist     = prompt[5:].split('/')
        username  = flist[0]
        userid    = flist[1]
        userclass = flist[2]
        
        try :
            sql = "select isregister from register_user where studentid = '{}'".format( userid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
        
            if ( isregister == "False" ) :
                
                sql = "select lineid from register_user where studentid = '{}'".format( userid )
                cursor2 = db.engine.execute( sql ) 
                useridfindlineid = cursor2.fetchone()[0]
                
                sql = "select lineid from register_user where studentname = '{}'".format( username )
                cursor4 = db.engine.execute( sql )
                usernamefindlineid = cursor4.fetchone()[0]
                
                if ( useridfindlineid != "temp" or usernamefindlineid != "temp" ) :
                    line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "您已經登入過系統，如有問題，請聯繫助教!" ) )
                
                try : 
                    sql = "select isregister from register_user where lineid = '{}'".format( lineid )
                    cursor5 = db.engine.execute( sql )
                    lineidfindisregister = cursor5.fetchone()[0]
                    
                    if ( lineidfindisregister == "True" ) :
                        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "您已經登入過系統，如有問題，請聯繫助教!" ) )
                except :
                    sql = "update register_user set lineid = '{}', isregister = '{}' where studentid = '{}' ".format( lineid, "True", userid )
                    db.engine.execute( sql )
            
                    turnback = "您已成功登入，身份如下 ! \n如有錯誤請聯絡助教"
                    turnback = turnback + "\n姓名 : " + username + "\n學號 : " + userid + "\n系級 : " + userclass
                
                    line_bot_api.reply_message( event.reply_token, TextSendMessage( text = turnback ) )
                
            else :
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "您已經登入過系統，如有問題，請聯繫助教!" ) )
                
            cursor.close()
            cursor2.close()
            cursor4.close()
            cursor5.close()
        except :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( "您未加選本學期課程!" ) )
        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤 !") ) 

def Important( event , lineid ) :
    try :
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            if( isregister == "True" ) :
                message = TextSendMessage(
                    text="請選擇想閱讀重點的章節",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="極限重點整理", text="極限重點整理")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="連續重點整理", text="連續重點整理")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分重點整理1", text="微分重點整理1")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分重點整理2", text="微分重點整理2")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分應用重點整理", text="微分應用重點整理")
                            ),
                        ]
                    )
                )
                
            
            cursor.close()
            
        except :
            message = [ TextSendMessage( text = "請先登入，並輸入基本資訊!" ) ]
        
        line_bot_api.reply_message( event.reply_token, message )
        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤！" ) )

def Test( event, lineid ):  
    try:
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            
            if( isregister == "True" ) :
                message = TextSendMessage(
                    text="請選擇測驗章節",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="極限測驗區", text="極限測驗區")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="連續測驗區", text="連續測驗區")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分測驗區1", text="微分測驗區1")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分測驗區2", text="微分測驗區2")
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="微分應用測驗區", text="微分應用測驗區")
                            ),
                        ]
                    ) 
                )
            
        except :
            message = [ TextSendMessage( text = "請先登入，並輸入基本資訊!" ) ]
            
        line_bot_api.reply_message( event.reply_token, message )
    except:
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤!" ))
        
def manageForm_test( event, prompt, lineid ): 
    try:
        flist    = prompt.split('\n')  
        Q_number = flist[1][5:]
        answer   = flist[2][8:]
        T_F      = flist[3][8:]
        usetime  = flist[4][7:]
            
        
        sql = "select studentid from register_user where lineid = '{}' ".format( lineid )
        cursor = db.engine.execute( sql )
        userid = cursor.fetchone()[0]
        
        sql = "insert into test_record ( lineid, studentid, qnumber, answer, tf, usetime ) values ( '{}', '{}', '{}', '{}', '{}', '{}' )".format( lineid, userid, Q_number, answer, T_F, usetime )
        db.engine.execute( sql )
        
        cursor.close()
        message = [ TextSendMessage( text = "您已成功繳交答案" ) ]
        
        line_bot_api.reply_message( event.reply_token,message )
    except:
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = '發生錯誤！' ) )

def Append_User( event, prompt, lineid ) :
    
    try :
        flist         = prompt.split('.')
        userclass     = flist[2]
        username      = flist[3]
        userstudentid = flist[4]
        
        temp = "temp"
        isregister = "False"
        
        sql = "insert into register_user ( lineid, studentid, studentclass, studentname, isregister ) values ( '{}', '{}', '{}', '{}', '{}' )".format( temp, userstudentid, userclass, username, isregister )
        db.engine.execute( sql )
        
        message = [ TextSendMessage( text = "已成功新增學生" ) ]
        
        line_bot_api.reply_message( event.reply_token,message )
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = '發生錯誤！' ) )

def Query( event, lineid ):
    
    try :
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            if( isregister == "True" ) :
                sql = "select qnumber from test_record where lineid = '{}'".format( lineid )
                cursor = db.engine.execute( sql )
                answer = cursor.fetchall()  
                history = list()
                answer.sort()
                text1 = "測驗區題目總數為\n-----------------------\n極限 : 14題\n連續 : 10題\n微分1: 15題\n微分2: 13題\n微分的應用: 8題\n-----------------------\n您已完成的題目為\n-----------------------\n"   
                for i in range( len( answer ) ) :
                    if ( answer[i][0] not in history ) :
                        text1 = text1 + answer[i][0] + "\n"
                        history.append( answer[i][0] ) 
                        
                text1 = text1 + "-----------------------"
                    
                line_bot_api.reply_message( event.reply_token, TextSendMessage( text = text1 ) )
                
            
            cursor.close()
            
        except :
            line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "請先登入，並輸入基本資訊!" ) )
        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤！" ) )


def ImportantChoice( event, prompt, lineid ) :
    try :
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            
            sql = "select studentid from register_user where lineid = '{}'".format( lineid )
            db.engine.execute( sql )
            
            if( isregister == "True" ) :
                if ( prompt[:2] == "極限" ) :
                    message = TemplateSendMessage(
                        alt_text = "極限重點整理",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/5FAqvTB.png",
                            title = "極限重點整理",
                            text = "極限重點整理",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_6 ) ]
                        )
                    )
                elif ( prompt[:2] == "連續" ) :   
                    message = TemplateSendMessage(
                        alt_text = "連續重點整理",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/DgclgDc.png",
                            title = "連續重點整理",
                            text = "連續重點整理",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_7 ) ]
                        )
                    )
                elif ( prompt[:2] == "微分" ) :
                    
                    
                    if( prompt == "微分重點整理1" ) :
                        message = TemplateSendMessage(
                            alt_text = "微分重點整理1",
                            template = ButtonsTemplate(
                                thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                                title = "微分重點整理1",
                                text = "微分重點整理1",
                                actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_8 ) ]
                            )
                        )
                    elif( prompt == "微分重點整理2" ) :
                        message = TemplateSendMessage(
                            alt_text = "微分重點整理2",
                            template = ButtonsTemplate(
                                thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                                title = "微分重點整理2",
                                text = "微分重點整理2",
                                actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_9 ) ]
                            )
                        )
                    elif( prompt == "微分應用重點整理" ) :
                        message = TemplateSendMessage(
                            alt_text = "微分應用重點整理",
                            template = ButtonsTemplate(
                                thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                                title = "微分應用重點整理",
                                text = "微分應用重點整理",
                                actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_10 ) ]
                            )
                        )
            
            cursor.close()
            
        except :
            message = [ TextSendMessage( text = "請先登入，並輸入基本資訊!" ) ]
        
        line_bot_api.reply_message( event.reply_token, message )
        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤！" ) )
        
def TestChoice( event, prompt, lineid ) :
    try :
        try :
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            cursor = db.engine.execute( sql )
            isregister = cursor.fetchone()[0]
            
            if( isregister == "True" ) :
                if ( prompt[:2] == "極限" ) :
                    message = TemplateSendMessage(
                        alt_text = "極限測驗區",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/5FAqvTB.png",
                            title = "極限測驗區",
                            text = "極限測驗區",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_2 ) ]
                        )
                    )
                elif ( prompt[:2] == "連續" ) :   
                    message = TemplateSendMessage(
                        alt_text = "連續測驗區",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/DgclgDc.png",
                            title = "連續測驗區",
                            text = "連續測驗區",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_3 ) ]
                        )
                    )
                elif ( prompt == "微分測驗區1" ) :
                    message = TemplateSendMessage(
                        alt_text = "微分測驗區1",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                            title = "微分測驗區1",
                            text = "微分測驗區1",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_4 ) ]
                        )
                    )
                elif ( prompt == "微分測驗區2" ) :
                    message = TemplateSendMessage(
                        alt_text = "微分測驗區2",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                            title = "微分測驗區2",
                            text = "微分測驗區2",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_5 ) ]
                        )
                    )
                elif ( prompt == "微分應用測驗區" ) :
                    message = TemplateSendMessage(
                        alt_text = "微分應用測驗區",
                        template = ButtonsTemplate(
                            thumbnail_image_url = "https://i.imgur.com/EC3eZ4z.png",
                            title = "微分應用測驗區",
                            text = "微分應用測驗區",
                            actions = [ URITemplateAction( label = "前往", uri = "https://liff.line.me/" + liffid_11 ) ]
                        )
                    )
            
            cursor.close()
        except :
            message = [ TextSendMessage( text = "請先登入，並輸入基本資訊!" ) ]
            
        line_bot_api.reply_message( event.reply_token, message )
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤！" ) )
        
    
def ImportantReadTime( event, prompt, lineid ) :
    
    flist    = prompt.split('\n')
    chapter  = flist[0] 
    time     = flist[1][7:]
    sequence = flist[2][7:]
    
    
    try :
        try :
            
            sql = "select isregister from register_user where lineid = '{}'".format( lineid )
            db.engine.execute( sql )
            
            sql = "select studentid from register_user where lineid = '{}'".format( lineid )
            cursor2 = db.engine.execute( sql )
            studentid = cursor2.fetchone()[0]
            
            if ( chapter[5:7] == "極限" ) :
                try :
                    IsFinish = "False"
                    sql = "select readsequence from important_record where lineid = '{}'".format( lineid )
                    cursor3 = db.engine.execute( sql ) 
                    readsequence = cursor3.fetchall()
                    
                    for i in range( len(readsequence) ) :
                        if ( readsequence[i][0] == sequence ) :
                            sql = "update important_record set readtime = '{}' where readsequence = '{}' and lineid = '{}'".format( time, sequence, lineid )
                            db.engine.execute( sql )
                            IsFinish = "True"
                        
                    if ( IsFinish != "True" ) :
                        sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "極限", time, sequence  )
                        db.engine.execute( sql )
                            
                except :
                    sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "極限", time, sequence  )
                    db.engine.execute( sql )
            
            elif ( chapter[5:7] == "連續" ) :
                try :
                    IsFinish = "False"
                    sql = "select readsequence from important_record where lineid = '{}'".format( lineid )
                    cursor3 = db.engine.execute( sql ) 
                    readsequence = cursor3.fetchall()
                    
                    for i in range( len(readsequence) ) :
                        if ( readsequence[i][0] == sequence ) :
                            sql = "update important_record set readtime = '{}' where readsequence = '{}' and lineid = '{}'".format( time, sequence, lineid )
                            db.engine.execute( sql )
                            IsFinish = "True"
                        
                    if ( IsFinish != "True" ) :
                        sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "連續", time, sequence  )
                        db.engine.execute( sql )
                            
                except :
                    sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "連續", time, sequence  )
                    db.engine.execute( sql )
                    
            elif ( chapter[5:8] == "微分1" ) :
                try :
                    IsFinish = "False"
                    sql = "select readsequence from important_record where lineid = '{}'".format( lineid )
                    cursor3 = db.engine.execute( sql ) 
                    readsequence = cursor3.fetchall()
                    
                    for i in range( len(readsequence) ) :
                        if ( readsequence[i][0] == sequence ) :
                            sql = "update important_record set readtime = '{}' where readsequence = '{}' and lineid = '{}'".format( time, sequence, lineid )
                            db.engine.execute( sql )
                            IsFinish = "True"
                        
                    if ( IsFinish != "True" ) :
                        sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分1", time, sequence  )
                        db.engine.execute( sql )
                            
                except :
                    sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分1", time, sequence  )
                    db.engine.execute( sql )
                    
            elif ( chapter[5:8] == "微分2" ) :
                try :
                    IsFinish = "False"
                    sql = "select readsequence from important_record where lineid = '{}'".format( lineid )
                    cursor3 = db.engine.execute( sql ) 
                    readsequence = cursor3.fetchall()
                    
                    for i in range( len(readsequence) ) :
                        if ( readsequence[i][0] == sequence ) :
                            sql = "update important_record set readtime = '{}' where readsequence = '{}' and lineid = '{}'".format( time, sequence, lineid )
                            db.engine.execute( sql )
                            IsFinish = "True"
                        
                    if ( IsFinish != "True" ) :
                        sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分2", time, sequence  )
                        db.engine.execute( sql )
                            
                except :
                    sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分2", time, sequence  )
                    db.engine.execute( sql )
            elif ( chapter[5:9] == "微分應用" ) :
                try :
                    IsFinish = "False"
                    sql = "select readsequence from important_record where lineid = '{}'".format( lineid )
                    cursor3 = db.engine.execute( sql ) 
                    readsequence = cursor3.fetchall()
                    
                    for i in range( len(readsequence) ) :
                        if ( readsequence[i][0] == sequence ) :
                            sql = "update important_record set readtime = '{}' where readsequence = '{}' and lineid = '{}'".format( time, sequence, lineid )
                            db.engine.execute( sql )
                            IsFinish = "True"
                        
                    if ( IsFinish != "True" ) :
                        sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分應用", time, sequence  )
                        db.engine.execute( sql )
                            
                except :
                    sql = "insert into important_record ( lineid, studentid, clicktype, readtime, readsequence ) values ( '{}', '{}', '{}', '{}', '{}' )".format( lineid, studentid, "微分應用", time, sequence  )
                    db.engine.execute( sql )
                
            cursor2.close()
            message = [ TextSendMessage( text = "閱讀紀錄已登錄!" ) ]
        except :
            message = [ TextSendMessage( text = "請先登入，並輸入基本資訊!" ) ]
        
        line_bot_api.reply_message( event.reply_token, message )
        
    except :
        line_bot_api.reply_message( event.reply_token, TextSendMessage( text = "發生錯誤！" ) )
        

    
if __name__ == '__main__':
    app.run()




