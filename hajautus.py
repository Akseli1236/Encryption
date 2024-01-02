def y(x, buckets):
    result = 0
    while x != 0:
        # Kerro x:n ensimmäinen ja viimeinen numero keskenään ja lisää tulos muuttujaan result.
        result += (x % 10) * (int(str(x)[:1]))
        # Poista ensimmäinen ja viimeinen numero
        x = int(str(x)[1:])
        x //= 10
        print(x)


    return result % buckets

# Testi avaimella 12345678 ja ämpäreillä 100
result = y(12345678, 100)
print(result)