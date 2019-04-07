
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## Piet Mondrian (100): Misc

### Proof of flag
>* ECSC{e647c19e4fc7838bf764abbdcb0c1f08adca163cdadfb889bee5201fc4397e5d}

### Summary
>* Extract images > Find interpreter > Run images

### Proof of solving

From the challenge description I immediately searched for "piet esolang" and found the language. Downloaded npiet to run the image but it wouldn't work. I even converted the image to a ".ppm", but still no luck. So after a bit of poking around I ran binwalk on the image.

```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, EXIF standard
12            0xC             TIFF image data, big-endian, offset of first image directory: 8
678           0x2A6           Copyright string: "Copyright (c) 1998 Hewlett-Packard Company"
11115         0x2B6B          Copyright string: "Copyright (c) 1998 Hewlett-Packard Company"
19274         0x4B4A          Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:xmpMM="http
22957         0x59AD          Copyright string: "Copyright (c) 1998 Hewlett-Packard Company"
345743        0x5468F         PNG image, 820 x 820, 8-bit colormap, non-interlaced
346832        0x54AD0         Zlib compressed data, best compression
1020129       0xF90E1         PNG image, 860 x 860, 8-bit colormap, non-interlaced
1021218       0xF9522         Zlib compressed data, best compression
1761760       0x1AE1E0        PNG image, 880 x 880, 8-bit colormap, non-interlaced
1762849       0x1AE621        Zlib compressed data, best compression
```

So I extracted the pngs, but locally it still wouldn't work. Finally I found an [online interpreter](https://www.bertnase.de/npiet/npiet-execute.php) which did work. Each image was a part of the flag, so I ran all three and got the flag.
