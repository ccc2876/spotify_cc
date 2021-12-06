# spotify_cc
# Requirements
1. Two spotify accounts (free or premium)
2. spotify-buddylist downloaded https://github.com/valeriangalliat/spotify-buddylist
3. Geckodriver downloaded in path


# Steps
## Creating the configuration file
1. The configuration file should contain the following lines
```
[account]
user=
password=
encoding_token=
decoding_token=
type=
```

2. Fill in the user with the email/username of the sender's Spotify account
3. Fill in the password with the password of the sender's Spotify account
4. The encoding token is the sender's API token

    API tokens can be generated here https://developer.spotify.com/console/get-current-user/ using the `Get Token` option
5. The decoding token is the receiver's API token
6. The type field should be filled with either premium or free for what type of account the sender has 
  
    Currently the tool only supports filling this line with `free` - but this will still work with a premium account
    
## Running the Program
### Encoding
1. Choose the method of encoding - either binary or album
2. Run the chosen method using either `python3 album_encoding.py` or `python3 binary_encoder.py`
3. Enter the message to send when prompted
4. Open the Spotify desktop app or the mobile app and start the playlist for it to appear in the Friend Feed

### Decoding
1. Run the correct decoding program based on how the messsage was encoded using either `python3 album_decoder.py` or `python3 binary_decoder.py`
2. The message will be outputted to the console when the user appears in the Friend Feed.


# Contents
**binary_encoder.py**

This file runs the encoding of a message using the binary explicit tag method.

**binary_decoder.py**

This file decodes messages that were uploaded using the binary method.

**album_enconding.py**

This file runs the encoding using the album name method.

**album_decoder.py**

This file will decode messages that were created using the album name method.

**utils.py**

This file contains functions that are used across both methods

