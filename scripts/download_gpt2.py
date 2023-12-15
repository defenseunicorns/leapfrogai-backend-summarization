from transformers import GPT2Model, GPT2Tokenizer

model = GPT2Model.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

model.save_pretrained(".")
tokenizer.save_pretrained(".")
