Robot
100
easy
Are you a robot?

Note: This is NOT a reversing or pwn challenge. Don't reverse the binary. It is for local testing only. You will actually get the flag after answering all the questions. You can practice locally by running ./robot AIS3{fake_flag} 127.0.0.1 1234 and it will run the service on localhost:1234.

Author: toxicpie

nc chals1.ais3.org 12348

WP:

If you use eval, you'll stuck since once you're too fast, it'll give you `{*iter(int,1)}` to stuck you.

So disgusting.

`AIS3{don't_eval_unknown_code_or_pipe_curl_to_sh}`