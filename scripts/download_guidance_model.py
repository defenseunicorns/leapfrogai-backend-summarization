from transformers import LongT5ForConditionalGeneration

# TODO: try out pszemraj/long-t5-tglobal-base-16384-book-summary instead
model = LongT5ForConditionalGeneration.from_pretrained("google/long-t5-tglobal-large")

model.save_pretrained(".model")
