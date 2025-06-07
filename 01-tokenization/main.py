import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "hello how are you !"

token = enc.encode(text)

print("tokennnnnnn",token)