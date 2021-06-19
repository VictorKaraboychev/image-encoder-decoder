# image-encoder-decoder

Encodes arbitrary data in color data for png images, and decodes data from encoded images.

**Encoding**: Takes an arbitrary file type, reads the byte code, and hides the binary information within the color data of a png file. <br/>
**Decoding**: Reads the hidden binary information from a png file with encoded information.<br/>
<hr/>

**DATA STRUCTURE**
- 0-7: 1x encoded, 1 byte responsible for denoting the encoding density
- 8-71: 8 bytes denoting the length of the stored data
- 72-135: 8 bytes denoting the file suffix
- 136+: encoded data
