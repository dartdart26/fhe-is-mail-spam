# FHE Based Mail Spam Detection
Fully homomorphic encryption based mail spam detection. Essentially, a client encrypts
an email with its private key and sends it (encrypted) over to a server. The server,
without decrypting the email, checks if it classifies as spam and returns an encrypted
response to the client. Only the client with its private key can decrypt the response.

Spam classification at that stage just means checking if certain spam strings are part
of the email message. If that is the case, we report spam. Otherwise, the message is
good and it is not spam.

Works via Google FHE: https://github.com/google/fully-homomorphic-encryption.
It is based on the TFHE library: https://tfhe.github.io/tfhe/

I got the idea from Vitalik Buterin's post on FHE:
https://vitalik.ca/general/2020/07/20/homomorphic.html

This example is a topic of a playlist on my YouTube channel:
https://www.youtube.com/playlist?list=PLNEYVOFMCyfMGBz31YjrYKtuYXtceSCeg

# Usage
1. Install and compile Google's FHE library by following its README file.
2. The [is_mail_spam](is_mail_spam) directory contains a working example that is meant to be
put in Google's FHE library `transpiler/examples` directory. Just copy or symlink the
[is_mail_spam](is_mail_spam) directory.
3. Edit the [spam.txt](is_mail_spam/data/spam.txt) file so that it includes strings that are classified
as spam.
4. Execute the [generate_spam_detection_code.py](is_mail_spam/generate_spam_detection_code.py) Python
script to generate C++ code.
5. Execute the unit test to make sure all is good:
```
bazelisk run //transpiler/examples/is_mail_spam:is_mail_spam_test 
```
6. Execute the testbench too. It simulates a client-server interaction:
```
bazelisk run //transpiler/examples/is_mail_spam:is_mail_spam_interpreted_tfhe_testbench "evil.url3"
...
[Client] Mail encryption done

                                        [Server] Computing
                                        [Server] Computation done
[Client] Decrypted result: 1
[Client] Mail is spam!
```

# Spam Strings
Spam strings are strings that we look for in emails. If an email contains one of them, the email is
classified as spam. The [spam.txt](is_mail_spam/data/spam.txt) file contains one entry per line. The
new line character is `\n`.

If a new line must be present, quoting can be used via the `"` character.
```
"new
line"
```

If the `"` character needs to be part of the spam string, it can be escaped via the `\` character:
```
"contains \""
```

# C++ Code Generation
As Google's FHE library (and supposedly TFHE) has a limitation that doesn't allow dynamic arrays,
we need to provide the spam strings at compile time. We do that by generating C++ code via Python.
We have a number of C++ code templates that we just replace code in based on configuration and spam
input. Then we pass the generated code to Google's FHE library and it compiles it to FHE code. That
way we achieve "dynamic" array support.

# TODO
 - Implement and actual client and a server. Use HTTP with JSON-RPC.