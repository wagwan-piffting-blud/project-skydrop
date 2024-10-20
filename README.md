_What_ is this?
---
This is a repository for hosting [Project Skydrop](https://projectskydrop.com/) code snippets. These code snippets help solve the puzzles found within Project Skydrop. The following files are available and ready for immediate use:

- [decode_12_secret_words.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/decode_12_secret_words.py)
  - Helps decode 12 secret words, in order, into a plaintext message (21 columns long) using the codebook specified. Codebooks are available at both [bounty.htm](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/bounty.htm) and [scroll.htm](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/scroll.htm) for ease of access.
- [decode_base_3.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/decode_base_3.py)
  - Decodes a Base-3 message into an extremely long Decimal number, then to Hexadecimal, then splits the Hexadecimal message and decodes it to ASCII.
  - Triangles are not encoded/separators for messages, "blank" spaces are encoded as 0, circles 1, squares 2.
  - A more "live", online version of this script is available at [Wags' Puzzle Space](https://wagspuzzle.space/tools/skydrop/) for your usage/perusal.
- [decode_linear_a.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/decode_linear_a.py)
  - Decodes a Linear A message into 12 secret words, used in the above decoder to translate to plaintext message (21 columns long).
  - A full alphabet, as well as a visual representation of the cipher, is available courtesy of an [Excel spreadsheet](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/skydrop.xlsx) made by [Bogie](https://github.com/bogiesmalls) (bogie_ on the Project Skydrop Discord).
- [locate_coords.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/locate_coords.py)
  - Locates name/number pairs in the codebook specified.
  - Outputs the final coordinates based on information given.
- [recover.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/recover.py)
  - Recovers a Bitcoin wallet using the 12 secret words specified.
  - Based on a script by [MinightDev](https://github.com/MinightDev/BTC-Wallet-Recover).
- [table_statistics.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/table_statistics.py)
  - Displays statistics on both the mountain name and secret word tables.
- [ProjectSkydropScripts.py](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/ProjectSkydropScripts.py)
  - All of the above scripts in a more easy-to-use format. **This file is the only one that will receive updates in the future, if any updates are needed.**

_How_ do I use this stuff?
---
Generally, usage is as follows:

1. Copy the repository, either by downloading the .ZIP file from GitHub directly, or running `git clone`.
2. Install a copy of [Python 3.12](https://www.python.org/downloads/) for your Operating System (latest available as of writing this is Python 3.13).
3. Install the requirements file using PIP (`pip install -r requirements.txt` in a terminal).
4. Run the script of your choice (`python [file_name].py` in a terminal after step 2).

Or (NEW!):

1. Download the release ProjectSkydropScripts.zip for either Windows or Linux.
2. Unextract the archive.
3. Run the .exe located within.

If you don't trust random executables, that's totally understandable, and in fact, you shouldn't! But, this one is just taken from the ProjectSkydropScripts.py file and run through a tool called `pyinstaller` for ease of use by everyone, even those not as technical as others. If you'd rather go the straight Python route, see instructions above.

_Why_?
---
When I was told about Project Skydrop, initially I was confused as to if I would be able to even help in any way solve it, not being in/from the New England area. However, with some encouragement from others, I am posting this code here so all can view, modify, etc. it. See the [LICENSE file](https://github.com/wagwan-piffting-blud/project-skydrop/blob/main/LICENSE) for more info on what restrictions are in place for this code/repository.

_Who_ am I?
---
I'm Wags, and I make a variety of things for the Internet. You can find my personal website [here](https://wagspuzzle.space/).

_Shoutouts_
---
Shoutouts to various members of the Project Skydrop Community are as follows:

- [Bogie](https://github.com/bogiesmalls)
- heyagbay
- [Vapok](https://github.com/Vapok)