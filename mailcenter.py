def main() -> None:
    import imbox
    import json
    import time
    import threading
    import re

    POLLING = 30
    QUIET = False
    NOCOLOR = False
    TIMESTAMP = True
    SSL = True

    MAIL_ACCOUNT_FILE = "mail_account.json"
    MAIL_IGNORE_FILE = "mail_ignore.txt"
    MAIL_DELETE_FILE = "mail_delete.txt"

    re_color = re.compile(r"\033\[[0-9]*?m")

    global print
    _print = print

    def print(*args, **kwargs):
        if QUIET:
            return None
        if TIMESTAMP:
            args = (time.strftime("\033[92m[%Y/%m/%d %H:%M:%S UTC%z]\033[0m", time.localtime()),) + args
        if NOCOLOR:
            return _print(*(re_color.sub("", str(i)) for i in args), **kwargs)
        else:
            return _print(*args, **kwargs)

    OUTPUT_WARNING = f"\033[91m[Warning]\033[0m"
    OUTPUT_IGNORE = "\033[94m[IGNORE]\033[0m"
    OUTPUT_DELETE = "\033[91m[DELETE]\033[0m"

    event = threading.Event()

    try:
        with open(MAIL_ACCOUNT_FILE, "rt") as f:
            mail_account_list = json.load(f)
    except:
        mail_account_list = []
        print(OUTPUT_WARNING, f"Empty mail_account_list at [{MAIL_ACCOUNT_FILE}]")

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
                        with imbox.Imbox(mail_type, mail_usr, mail_pwd, SSL) as mail_box:
                            mail_unread_list = mail_box.messages(unread=True)
                            for mail_uid, mail_msg in mail_unread_list:
                                mail_from = mail_msg.sent_from[0]["email"]
                                mail_subject = mail_msg.subject
                                if mail_from in mail_ignore_list:
                                    mail_box.mark_seen(mail_uid)
                                    print(f"[{mail_usr}]", OUTPUT_IGNORE, f"[{mail_from}]", f"\033[90m[{mail_subject}]\033[0m")
                                elif mail_from in mail_delete_list:
                                    mail_box.delete(mail_uid)
                                    print(f"[{mail_usr}]", OUTPUT_DELETE, f"[{mail_from}]", f"\033[90m[{mail_subject}]\033[0m")
                    else:
                        print(OUTPUT_WARNING, f"Unknown mailbox type [{mail_type}]")
                except:
                    print(OUTPUT_WARNING, f"Cannot login as [{mail_usr}]")

            event.wait(POLLING)

    except:
        print(OUTPUT_WARNING, f"Program exit")


if __name__ == "__main__":
    main()
