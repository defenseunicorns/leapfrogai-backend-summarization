from transformers import LongT5ForConditionalGeneration, T5TokenizerFast

# TODO: try out pszemraj/long-t5-tglobal-base-16384-book-summary instead
model = LongT5ForConditionalGeneration.from_pretrained("google/long-t5-tglobal-large")
tokenizer = T5TokenizerFast.from_pretrained("google/long-t5-tglobal-large")

model.save_pretrained(".model")
tokenizer.save_pretrained(".model")