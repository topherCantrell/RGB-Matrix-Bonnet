# Binary movie file format

4-byte values are little-endian (LSB first)

## List of movies

File header -- 512 bytes

- '2' '0' '1' '8' 0 0 0 0 0 0 0 0 0 0 0 1

Followed by list of movies
'

15 movie description slots, 16 bytes each

- 'n' 'a' 'm' 'e'  0 0 0 0 0 0 0 0  d c b a  (start sector abcd)

## Movie

Each movie:

512 byte header

Frame count, delay between frames, goto-next (use 0 for next movie)

- c c c c  d d d d  g g g g     0's out to 512

1024 bytes of color data (256 colors * 4 bytes each)

2048 bytes of pixels per frame

Put a blank header on the end to force a repeat to beginning of disk