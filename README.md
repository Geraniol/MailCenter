# Mail Center <br /> 邮件中心  

## **依赖**  
- `imbox` 库  
  - 建议通过 `python3 -m venv` 创建虚拟环境  
  - 通过 `pip3 install imbox` 安装  

## **功能/使用说明**  
- 安装/运行  
  - 克隆本存储库：`git clone https://github.com/Geraniol/MailCenter.git`  
  - 运行：`python3 mailcenter.py`  
- 自动标记邮件为已读  
  - 编辑/创建 `./mail_ignore.txt`，将需要标记为已读的邮件地址按行写入  
- 自动删除邮件  
  - 编辑/创建 `./mail_delete.txt`，将需要删除的邮件地址按行写入  
- 程序 `mailcenter.py` 中可自定义参数：  
  - 内部参数  
    - `POLLING` 邮件轮询间隔（秒）  
    - `QUIET` 不打印输出  
    - `NOCOLOR` 关闭彩色输出  
    - `TIMESTAMP` 打印时间戳  
    - `SSL` 开启 ssl 认证  
  - 外部参数  
    - `MAIL_ACCOUNT_FILE` 账户信息之文件路径  
    - `MAIL_IGNORE_FILE` 需要标记为已读的邮箱之文件路径  
    - `MAIL_DELETE_FILE` 需要删除的邮箱之文件路径  
- 目前仅支持 `imap` 协议邮箱  
- 支持热更新邮箱列表，无需重启程序  

## **问题**  
- 无法登陆邮箱  
  - 检查 `./mail_account.json` 中的账户信息是否正确  
  - 在 `./mailcenter.py` 中关闭 ssl 认证：`SSL = False`  

## **运行预览**  
<img src="./lib/sample.png" width="100%">  
