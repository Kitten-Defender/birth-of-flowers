from time import sleep

# Type out text
def write(text):
    for x in text:
        sleep(0.03)
        print(x, end="", flush=True)
        
def ask(text):
    for x in text:
        sleep(0.03)
        print(x, end="", flush=True)
    x = input("\n")
    return x
    