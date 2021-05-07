# HiddenWave
Embedding secret messages in wave audio file

# What is HiddenWave
Hiddenwave is a python based program for simple audio steganography. You can hide your secret text messages in wave audio file. you can play this audio in any media player and secretly share your private message with any one.

# Requirements
This tool require python3

## Libraries

This tool requires the following libraries installed in order to work:

- [cryptography](https://pypi.org/project/cryptography/)
- [colorama](https://pypi.org/project/colorama/)
- [termcolor](https://pypi.org/project/termcolor/)

Open the links above to know how to install the above libraries

## Installation

```
git clone https://github.com/techchipnet/HiddenWave.git
cd HiddenWave
```
## Usage
<p>Hiddenwave have two python scripts. </p>
<ul>
<li><b>HiddenWave.py :</b> for hide secret information.</li>
<li><b>ExWave.py :</b> for extract secret information for wave audio file.</li>
</ul>

### Hide Secret Information in Audio file

```
python3 HiddenWave.py -f Demo.wav -m "Secret Msg" -o output.wav
```
IF you want to encrypt your message, use the -e argument with the letter "Y". Here's how:

``` 
python3 HiddenWave.py -f Demo.wav -m "Secret Message" -e Y -o Output.wav
```

### Extract Secret Information from Audio file

```
python3 ExWave.py -f output.wav
```

IF the message was encrypted, you will need to use the -e argument along with a "Y". Here's how:

```
python3 ExWave.py -e Y -f Output.wav
```

### More information about Encryption:

#### When Encrypting:

When you encrypt the message using "HiddenWave.py", you will be provided with three options asking if you want to use a pre-made key, random key or create a password based key. All the options are pretty self explanatory but here's a little explanation:

| Selection          | What it does                                                 |
| ------------------ | ------------------------------------------------------------ |
| Pre-Made Key       | Asks you to type the path to the key and then encrypts the message. |
| Random Key         | Creates a random key for you and saves it in the current directory. Also, uses the same key to encrypt and embed data to the audio file. |
| Password Based Key | Asks you a password and if you want to use a custom salt or random salt. In any case, it will save the Salt and Key with the names you specify in the Current Directory. And embeds the encrypted message in the audio file. |

#### When Decrypting:

When you decrypt, the program will ask you if you want to use a key file or create the key on the spot using the salt file. You must have the salt file for the second option to work; and the password too.

| Selection                  | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| Using key file             | Asks you for the path to the key file and decrypts the audio file with the key provided |
| Creating Key from Password | This one requires you to have the salt file and the password you used to create the key while encrypting. It will ask for the password and then the salt file. Then it decrypts and shows the message. |

If there are any issues, I'll be glad to fix them and if there are any confusions, I'll surely help you out.

### Video Demo

[![How to control android camera](https://img.youtube.com/vi/UPQD7L9FNrk/0.jpg)](https://www.youtube.com/watch?v=UPQD7L9FNrk)

#### For More Video subcribe <a href="http://youtube.com/techchipnet">TechChip YouTube Channel</a>
