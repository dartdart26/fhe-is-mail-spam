# FHE Based Mail Spam Detection
Fully homomorphic encryption based mail spam detection.

Works via Google's FHE library: https://github.com/google/fully-homomorphic-encryption

I got the idea from Vitalik Buterin's post on FHE:
https://vitalik.ca/general/2020/07/20/homomorphic.html

# Usage
1. Install and compile Google's FHE library by following its README file.
2. The [is_mail_spam](is_mail_spam) directory contains a working example that is meant to be
put in Google's FHE library `transpiler/examples` directory. Just copy or symlink the
[is_mail_spam](is_mail_spam) directory.
3. Edit the [spam.txt](is_mail_spam/data/spam.txt) file so that it includes strings that are classified
as spam.
4. Execute the [generate_spam_detection_code.py](is_mail_spam/generate_spam_detection_code.py) script
to generate C++ code.
5. Execute the unit test to make sure all is good:
```
bazelisk run //transpiler/examples/is_mail_spam:is_mail_spam_test 
```
6. Execute the testbench too:
```
bazelisk run //transpiler/examples/is_mail_spam:is_mail_spam_interpreted_tfhe_testbench "evil.url3"
...
[Client] Mail encryption done

                                        [Server] Computing
                                        [Server] Computation done
[Client] Decrypted result: 1
[Client] Mail is spam!
```
