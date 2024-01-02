text = input("Text: ").strip(" ")

print(text)
hello_fucker = {}
for some in text:
    if some in hello_fucker:
        hello_fucker[some] = hello_fucker[some] + 1
    else:
        hello_fucker[some] = 1
for x,y in hello_fucker.items():
    hello_fucker[x] = [y, y/len(text) * 100]
print(hello_fucker)
p = 0

new_text = ""

for i in text:
    if i != " ":
        new_text += i
print(new_text)
while (True):
    hah = input("Replace: ")
    with_ = input("With: ")
    stop = input("Stop?:")
    if stop == "Yes":
        break
    temp_text = ""
    apu = 0
    for i in new_text:
        if i == hah:
            temp_text += with_
            new_text[apu] = with_
        else:
            temp_text += i
        temp_text += " "
        apu += 1

    print(hello_fucker)
    print(temp_text)
