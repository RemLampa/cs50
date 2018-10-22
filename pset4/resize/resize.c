#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize factor infile outfile\n");
        return 1;
    }

    // get resize factor
    float factor = atof(argv[1]);
    if (factor < 0.0 || factor >= 100.0)
    {
        fprintf(stderr, "Resize factor should be positive and less than 100.0");
        return 2;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // generate image and file size headers for outfile
    BITMAPFILEHEADER *out_bf = malloc(sizeof(BITMAPFILEHEADER));
    BITMAPINFOHEADER *out_bi = malloc(sizeof(BITMAPINFOHEADER));

    int out_padding = padding;

    *out_bf = bf;
    *out_bi = bi;

    if (factor != 1.0)
    {
        out_bi->biWidth = (LONG) floor(out_bi->biWidth * factor);
        out_bi->biHeight = (LONG) floor(out_bi->biHeight * factor);

        out_padding = (4 - (out_bi->biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

        out_bi->biSizeImage = ((sizeof(RGBTRIPLE) * out_bi->biWidth) + out_padding) * abs(out_bi->biHeight);

        out_bf->bfSize = out_bi->biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    }

    // write outfile's BITMAPFILEHEADER
    fwrite(out_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(out_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    if (factor < 1.0)
    {
        float width_ratio = (float) bi.biWidth / (float) out_bi->biWidth;
        float height_ratio = (float) abs(bi.biHeight) / (float) abs(out_bi->biHeight);

        // counter for outfile's scanlines
        float out_i = 0.0;

        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            // pick or reject current scanline
            if ((out_i < biHeight) && (i >= out_i || i == biHeight - 1))
            {
                // counter for pixels of in outfile's scanline
                float out_j = 0.0;

                // iterate over pixels in scanline
                for (int j = 0; j < bi.biWidth; j++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    // pick or reject current pixel
                    if ((out_j < bi.biWidth) && (j >= out_j || j == bi.biWidth - 1))
                    {
                        // write RGB triple to outfile
                        fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                        out_j += width_ratio;
                    }
                }

                // skip over infile padding, if any
                fseek(inptr, padding, SEEK_CUR);

                // add resized padding to outfile
                for (int k = 0; k < out_padding; k++)
                {
                    fputc(0x00, outptr);
                }

                out_i += height_ratio;
            }
            else
            {
                // skip current scanline
                fseek(inptr, (sizeof(RGBTRIPLE) * bi.biWidth) + padding, SEEK_CUR);
            }
        }
    }

    if (factor >= 1.0)
    {
        // counter for outfile's scanlines
        int out_i = 0;

        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // repeat pixel
                for (int out_j = 0; out_j < factor; out_j++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // skip over infile padding, if any
            fseek(inptr, padding, SEEK_CUR);

            // add resized padding to outfile
            for (int k = 0; k < out_padding; k++)
            {
                fputc(0x00, outptr);
            }

            out_i++;

            // repeat scanline
            if (out_i < factor)
            {
                fseek(inptr, -(long)((sizeof(RGBTRIPLE) * bi.biWidth) + padding), SEEK_CUR);
                i--;
            }
            else
            {
                out_i = 0;
            }
        }
    }

    // deallocate memory
    free(out_bf);
    free(out_bi);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
