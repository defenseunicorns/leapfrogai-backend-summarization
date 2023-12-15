from transformers import AutoModelForCausalLM, AutoTokenizer

# TODO: try out other models
model = AutoModelForCausalLM.from_pretrained("ainize/bart-base-cnn")
tokenizer = AutoTokenizer.from_pretrained("ainize/bart-base-cnn")

model.save_pretrained(".model")
tokenizer.save_pretrained(".model")
