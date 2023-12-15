from transformers import AutoModelForCausalLM, AutoTokenizer

# TODO: try out other models
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

model.save_pretrained(".model")
tokenizer.save_pretrained(".model")
