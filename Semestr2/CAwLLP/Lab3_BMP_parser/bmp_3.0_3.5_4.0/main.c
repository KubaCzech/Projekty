#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

struct {
    char *char_array;
    int size;
} typedef str;

struct {
    int width;
    int height;
    str value;
} typedef item;

struct {
    item *item_array;
    int size;
} typedef dynamic_byte_array;

str char_to_hex (char c){
    str hexadecimal;
    hexadecimal.size=3;
    hexadecimal.char_array = malloc(sizeof(char) * hexadecimal.size);
    hexadecimal.char_array[2]='\0';
    int a=(int)(c);
    if(c == ' '){
        hexadecimal.char_array[0]='0';
        hexadecimal.char_array[1]='0';
    }
    else{
        if(a<0)
            a+=256;
        if (a/16==0)
            hexadecimal.char_array[0]='0';
        else if(a/16>9)
            hexadecimal.char_array[0]=(char)(a / 16 - 9 + 64);
        else
            hexadecimal.char_array[0]=(char)(a / 16 + 48);
        if(a%16 == 0)
            hexadecimal.char_array[1]='0';
        else if(a%16>9)
            hexadecimal.char_array[1]=(char)(a % 16 - 9 + 64);
        else
            hexadecimal.char_array[1]=(char)(a % 16 + 48);
    }
    //printf("%s \n", hexadecimal.char_array);
    return hexadecimal;

}

str hex_to_binary_digit(char number){
    int a;
    str binary_nr;
    binary_nr.size=5;
    binary_nr.char_array = malloc(sizeof(char) * binary_nr.size);
    binary_nr.char_array[4]='\0';
    if((int)(number)>=48 && (int)(number)<58)
        a=(int)(number)-48;
    else
        a=(int)(number-55);
    for (int i=3; i>=0; i--)
    {
        binary_nr.char_array[i] = (char) (a % 2);
        a=a/2;
    }
    return (binary_nr);
}

str hex_to_binary_number(str hex_number){
    str binary_nr, number;
    binary_nr.size=(hex_number.size-1)*4 + 1;
    binary_nr.char_array = malloc(sizeof(char) * binary_nr.size);
    binary_nr.char_array[binary_nr.size-1]='\0';
    number.size=5;
    number.char_array = malloc(sizeof(char) * number.size);
    number.char_array[4]='\0';
    for (int i=0; i<binary_nr.size; i++){
        number=hex_to_binary_digit(hex_number.char_array[i]);
        binary_nr.char_array[i]=number.char_array[0];
        binary_nr.char_array[i+1]=number.char_array[1];
        binary_nr.char_array[i+2]=number.char_array[2];
        binary_nr.char_array[i+3]=number.char_array[3];
    }
    return (binary_nr);
}

str decimal_to_binary(int number){
    str binary_nr;
    binary_nr.size=9;
    binary_nr.char_array = malloc(sizeof(char) * binary_nr.size);
    binary_nr.char_array[8]='\0';
    for (int i=0; i<8; i++){
        binary_nr.char_array[i]=number/power(2, 7-i);
        if(binary_nr.char_array[i]>0)
            number=number/power(2, 7-i);
    }
    return binary_nr;
}

str extract_str(str s, int a, int b){
    str extraction;
    extraction.size= b - a + 1 + 1;
    extraction.char_array = malloc(sizeof(char) * extraction.size);
    extraction.char_array[extraction.size-1]='\0';
    for (int i=a; i<=b; i++)
        extraction.char_array[i-a]=s.char_array[i];
    return extraction;
}

int power(int a, int b){
    int number=a;
    if(b==0)
        return 1;
    for (int i=0; i<b-1; i++)
        number=number*a;
    return number;
}

int hexi_to_decimal(str s){
    int a=0;
    for (int i=0; i<s.size-1; i++){
        if(s.char_array[i]<=57)
            a=a+((int)(s.char_array[i])-48)*power(16, s.size-2-i);
        else
            a=a+((int)(s.char_array[i])-55)*power(16, s.size-2-i);
    }
    //printf("%d", a);
    return a;
}

int calculate_bits(str number){
    str mirror;
    mirror.size=number.size;
    mirror.char_array = malloc(sizeof(char) * mirror.size);
    mirror.char_array[mirror.size-1]='\0';
    for (int i=0; i<mirror.size-2; i=i+2){
        mirror.char_array[i]=number.char_array[number.size-3-i];
        mirror.char_array[i+1]=number.char_array[number.size-2-i];
    }
    return (hexi_to_decimal(mirror));
}

void print_bitmap_file_header(str line){
    printf("BITMAPFILEHEADER \n");
    printf("bfType: 0x%s\n", extract_str(line, 0, 3).char_array);
    //printf("%s \n", extract_str(line, 4, 11).char_array);
    printf("bfSize: %d\n", calculate_bits(extract_str(line, 4, 11)));
    printf("bfReserved1: 0x%s\n", (extract_str(line, 12, 15).char_array));
    printf("bfReserved2: 0x%s\n", (extract_str(line, 16, 19).char_array));
    printf("bfOffBits: %d\n", calculate_bits(extract_str(line, 20, 27)));

    printf("\n");
}

void print_bit_map_info_header(str line){
    printf("BITMAPINFOHEADER\n");
    printf("biSize: %d\n", calculate_bits(extract_str(line, 0, 7)));
    printf("biWidth: %d\n", calculate_bits(extract_str(line, 8, 15)));
    printf("biHeight: %d\n", calculate_bits(extract_str(line, 16, 23)));
    printf("biPlanes: %d\n", calculate_bits(extract_str(line, 24, 27)));
    printf("biBitCount: %d\n", calculate_bits(extract_str(line, 28, 31)));
    printf("biCompression: %d\n", calculate_bits(extract_str(line, 32, 39)));
    printf("biSizeImage: %d\n", calculate_bits(extract_str(line, 40, 47)));
    printf("biXPelsPerMeter: %d\n", calculate_bits(extract_str(line, 48, 55)));
    printf("biYPelsPerMeter: %d\n", calculate_bits(extract_str(line, 56, 63)));
    printf("biClrUsed: %d\n", calculate_bits(extract_str(line, 64, 71)));
    printf("biClrImportant: %d\n", calculate_bits(extract_str(line, 72, 79)));

    printf("\n");
}

//declaring arrays for RGB
    int red[17]={0};
    int green[17]={0};
    int blue[17]={0};

void increment_shade(int arr[17], str byte){
    char category=byte.char_array[0];
    int a;
    if((int)(category)>57)
        a=(int)(category)-55;
    else
        a=(int)(category)-48;
    arr[a]++;
    arr[16]++;
}

void print_histogram(const int arr[17], int x){
    printf("Histogram\n");
    if (x == 1)
        printf("Blue: \n");
    else if (x == 2)
        printf("Green: \n");
    else if (x == 3)
        printf("Red: \n");
    else {
        printf("Wrong color specifier: %i not in [1,2,3]", x);
    }
    for (int i=0; i<16; i++){
        float c= 100*((float)(arr[i])/(float)(arr[16]));
        printf("%d-%d: %.2f%%\n", i*16, (i+1)*16 - 1, c);
    }
    printf("\n");
}

int main(int argc, char *argv[])
{
    const short allowed_argument_number = 2 + 1;
    if (argc > allowed_argument_number) {
        printf("Too many arguments: %i is more than maximum %i allowed.", argc, allowed_argument_number);
        return 1;
    }
    //some variables
    char c;
    int off_bits;
    item current_line_item;

    //declaring database
    dynamic_byte_array database;
    database.item_array = malloc(sizeof(item));
    database.size = 0;

    //opening file
    FILE *file;
    file = fopen(argv[1], "rb");

    //file header info
    str file_header;
    file_header.size=29;
    file_header.char_array = malloc(sizeof(char) * 29);
    file_header.char_array[28]='\0';

    //variable size info:
    str header_of_var_size_info;
    header_of_var_size_info.size=9;
    header_of_var_size_info.char_array = malloc(sizeof(char) * 9);
    header_of_var_size_info.char_array[8]='\0';
    str var_size_info;
    var_size_info.size=0;

    if (file == NULL) {
        printf("Error occurred when opening a file: %s", argv[1]);
        return 1;
    }

    int biCompression, biBitCount, biWidth, biHeight, bytes_to_read, bytes_to_interpret;
    int number_of_bytes=0;

    //while loop to iterate over all lines
    for (int i=0; i<14; i++){
        c = (char) fgetc(file);
        str hexadecimal = char_to_hex(c);
        //printf("%c%c ", hexadecimal.char_array[0], hexadecimal.char_array[1]);
        if (number_of_bytes < 14) {
            file_header.char_array[2 * number_of_bytes]=hexadecimal.char_array[0];
            file_header.char_array[2 * number_of_bytes + 1]=hexadecimal.char_array[1];
            }
        number_of_bytes++;
    }
    off_bits=calculate_bits(extract_str(file_header, 20, 27));
    for(int i=14; i<calculate_bits(extract_str(file_header, 4, 11)); i++){
        c = (char) fgetc(file);
        str hexadecimal = char_to_hex(c);
        //printf("%c%c ", hexadecimal.char_array[0], hexadecimal.char_array[1]);
        if(number_of_bytes > 13 && number_of_bytes < 18) {
            header_of_var_size_info.char_array[2*(number_of_bytes - 13) - 2]=hexadecimal.char_array[0];
            header_of_var_size_info.char_array[2*(number_of_bytes - 13) - 1]=hexadecimal.char_array[1];
        }

        else if (number_of_bytes == 18) {
            var_size_info.size=2*calculate_bits(header_of_var_size_info)+1;
            var_size_info.char_array = malloc(sizeof(char) * var_size_info.size);
            var_size_info.char_array[var_size_info.size-1]='\0';
            for (int j=0; j < 8; j++)
                var_size_info.char_array[j]=header_of_var_size_info.char_array[j];
        }

        if (number_of_bytes >= 18 && number_of_bytes < off_bits){
            var_size_info.char_array[2*(number_of_bytes - 18 + 4)]=hexadecimal.char_array[0];
            var_size_info.char_array[2*(number_of_bytes - 18 + 4) + 1]=hexadecimal.char_array[1];
        }

        else if (number_of_bytes == off_bits){
            // TODO: biCompression
            biCompression=calculate_bits(extract_str(var_size_info, 32, 39));
            if (biCompression != 0) {
                printf("Not implemented compression: %i only 0 is allowed.", biCompression);
                return 1;
            }
            biBitCount=calculate_bits(extract_str(var_size_info, 28, 31));
            if (biBitCount != 24) {
                printf("Not implemented bit count: %i only 24 is allowed.", biBitCount);
                return 1;
            }
            //printf("\n%s\n", var_size_info.char_array);
            biWidth=calculate_bits(extract_str(var_size_info, 8, 15));
            //printf("%d", biWidth);
            bytes_to_read=((biBitCount*biWidth + 31)/32)*4;
            bytes_to_interpret=3*biWidth;
            off_bits=calculate_bits(extract_str(file_header, 20, 27));
        }

        if (number_of_bytes >= off_bits){
            current_line_item.height= (number_of_bytes - off_bits - 1) / bytes_to_read;
            current_line_item.width= (number_of_bytes - off_bits - 1) % bytes_to_read;
            current_line_item.value=hexadecimal;
            database.item_array = realloc(database.item_array, sizeof(item) * ++database.size);
            database.item_array[database.size - 1] = current_line_item;
            if(((number_of_bytes - off_bits - 1) % bytes_to_read) % 3 == 0 && ((number_of_bytes - off_bits - 1) % bytes_to_read <= bytes_to_interpret - 1)) //Blue
                increment_shade(blue, hexadecimal);
            if(((number_of_bytes - off_bits - 1) % bytes_to_read) % 3 == 1 && (number_of_bytes - off_bits - 1) % bytes_to_read <= bytes_to_interpret - 1) //Green
                increment_shade(green, hexadecimal);
            if(((number_of_bytes - off_bits - 1) % bytes_to_read) % 3 == 2 && (number_of_bytes - off_bits - 1) % bytes_to_read <= bytes_to_interpret - 1) //Red
                increment_shade(red, hexadecimal);
        }
        number_of_bytes++;
    }
    printf("Number of bytes: %d\n", number_of_bytes);
    fclose(file);
    //Ex. 3.0
    print_bitmap_file_header(file_header);
    print_bit_map_info_header(var_size_info);
    //Ex. 3.5
    print_histogram(blue, 1);
    print_histogram(green, 2);
    print_histogram(red, 3);
    //Ex. 4.0
    int grey;
    int b_val, g_val, r_val;
    str b, g, r;
    FILE *file_w;
    file_w = fopen(argv[2], "wb");
    if (file_w == NULL)
        printf("Error occurred when opening a file: %s\n", argv[2]);
    // TODO: add to a structure (automatic conversion from 16 bit to char) ?
    else{
    for (int i=0; i<off_bits; i++){
        str s;
        if(i<14) {
            s = extract_str(file_header, 2*i, 2*i+1);
            int ascii_number=hexi_to_decimal(s);
            fwrite(&ascii_number, sizeof(int)/4, 1, file_w);
        }
        else {
            s = extract_str(var_size_info, 2*(i-14), 2*(i-14)+1);
            int ascii_number=hexi_to_decimal(s);
            fwrite(&ascii_number, sizeof(int)/4, 1, file_w);
            //printf("%d", i);
        }

    }
    //printf("\nfinish of part 1 and 2\n");
    biWidth=calculate_bits(extract_str(var_size_info, 8, 15));
    biHeight=calculate_bits(extract_str(var_size_info, 16, 23));
    for (int i=0; i<biHeight; i++){
        for (int j=0; j<bytes_to_read; j=j+3){
            if(j<bytes_to_interpret-1){
                b=database.item_array[i*bytes_to_read + j].value;
                b_val=hexi_to_decimal(b);
                g=database.item_array[i*bytes_to_read + j+1].value;
                g_val=hexi_to_decimal(g);
                r=database.item_array[i*bytes_to_read + j+2].value;
                r_val=hexi_to_decimal(r);
                grey=(b_val+g_val+r_val)/3;
                for (int k=0; k<3; k++)
                    fwrite(&grey, sizeof(int)/4, 1, file_w);
            }
            else {
                if(bytes_to_read-bytes_to_interpret == 1){
                    int ascii_number=hexi_to_decimal(database.item_array[i*bytes_to_read + j].value);
                    fwrite(&ascii_number, sizeof(int)/4, 1, file_w);
                }
                else if (bytes_to_read-bytes_to_interpret == 2){
                    for (int k=0; k<2; k++){
                        int ascii_number=hexi_to_decimal(database.item_array[i*bytes_to_read + j+k].value);
                        fwrite(&ascii_number, sizeof(int)/4, 1, file_w);
                    }
                }
            }
        }
    }
    }
    return 0;
}
