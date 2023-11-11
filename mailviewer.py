def main() -> None:
    import imbox
    import json
    import re

    NOCOLOR = False
    SSL = True

    PATH_MAIL_ACCOUNT = "./mail_account.json"

    re_color = re.compile(r"\033\[[0-9]*?m")

    global print
    _print = print

    def print(*args, **kwargs):
        if NOCOLOR:
            return _print(*(re_color.sub("", str(i)) for i in args), **kwargs)
        else:
            return _print(*args, **kwargs)

    OUTPUT_WARNING = f"\033[91m[Warning]\033[0m"

    try:
        with open(PATH_MAIL_ACCOUNT, "rt") as f:
            mail_account_list = json.load(f)
    except:
        mail_account_list = []
        print(OUTPUT_WARNING, f"Empty mail_account_list at [{PATH_MAIL_ACCOUNT}]")

    try:
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
                            print(f"\033[92m[{mail_usr}]\033[0m", f"[{mail_from}]", f"\033[90m[{mail_subject}]\033[0m")
                else:
                    print(OUTPUT_WARNING, f"Unknown mailbox type [{mail_type}]")
            except:
                print(OUTPUT_WARNING, f"Cannot login as [{mail_usr}]")

    except:
        print(OUTPUT_WARNING, f"Program exit")


if __name__ == "__main__":
    main()
