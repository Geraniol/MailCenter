def main() -> None:
    import imbox
    import json
    import time
    import threading

    global print

    POLLING = 30
    HEADLESS = False

    MAIL_ACCOUNT_FILE = "mail_account.json"
    MAIL_IGNORE_FILE = "mail_ignore.txt"
    MAIL_DELETE_FILE = "mail_delete.txt"

    _print = print

    def print(*args, **kwargs):
        if HEADLESS:
            return None
        else:
            _print(time.strftime("\033[92m[%Y/%m/%d %H:%M:%S UTC%z]\033[0m", time.localtime()), end=" ")
            return _print(*args, **kwargs)

    event = threading.Event()

    try:
        with open(MAIL_ACCOUNT_FILE, "rt") as f:
            mail_account_list = json.load(f)
    except:
        mail_account_list = []
        print(f"\033[91m[Warning]\033[0m Empty mail_account_list at [{MAIL_ACCOUNT_FILE}]")

    try:
        while True:

            try:
                with open(MAIL_IGNORE_FILE, "rt") as f:
                    mail_ignore_list = f.read().splitlines()
            except:
                mail_ignore_list = []

            try:
                with open(MAIL_DELETE_FILE, "rt") as f:
                    mail_delete_list = f.read().splitlines()
            except:
                mail_delete_list = []

            for mail_account in mail_account_list:
                mail_type = mail_account["type"]
                mail_usr = mail_account["usr"]
                mail_pwd = mail_account["pwd"]
                try:
                    if mail_type == "imap.qq.com":
                        with imbox.Imbox(mail_type, mail_usr, mail_pwd) as mail_box:
                            mail_unread_list = mail_box.messages(unread=True)
                            for mail_uid, mail_msg in mail_unread_list:
                                mail_from = mail_msg.sent_from[0]["email"]
                                mail_subject = mail_msg.subject
                                if mail_from in mail_ignore_list:
                                    mail_box.mark_seen(mail_uid)
                                    print(f"[{mail_usr}] \033[94m[IGNORE]\033[0m [{mail_from}] \033[90m[{mail_subject}]\033[0m")
                                elif mail_from in mail_delete_list:
                                    mail_box.delete(mail_uid)
                                    print(f"[{mail_usr}] \033[91m[DELETE]\033[0m [{mail_from}] \033[90m[{mail_subject}]\033[0m")
                    else:
                        print(f"\033[91m[Warning]\033[0m Unknown mailbox type [{mail_type}]")
                except:
                    print(f"\033[93m[Warning]\033[0m Cannot login as [{mail_usr}]")

            event.wait(POLLING)

    except:
        print(f"\033[91m[Warning]\033[0m Program exit")

if __name__ == "__main__":
    main()
