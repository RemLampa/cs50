# Questions

## What's `stdint.h`?

It's a header file that makes exact width integer types available to the program.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

It allows a program to read and write into data structures with pre-determined byte sizes (i.e. file headers).

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

It should state the filetype, which for a BMP file should be "BM".

## What's the difference between `bfSize` and `biSize`?

bfSize describes the file size, in bytes, of the bitmap file itself. While biSize describes the required size, in bytes, of the bitmap file information header.

## What does it mean if `biHeight` is negative?

It means that the bitmap file is read from the top-down, with its origin from the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the given infile and outfile arguments cannot be opened (i.e. non-existing/file-permission issues).

## Why is the third argument to `fread` always `1` in our code?

We only need to read one chunk each for the BITMAPFILEHEADER & BITMAPINFOHEADER.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

It repositions the current location of the file pointer, in our case, it repositions it after the padding.

## What is `SEEK_CUR`?

It is the pointer to the current position of the file pointer.

## Whodunit?

It was Professor Plum with the candlestick in the library.
