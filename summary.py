import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import pipeline
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader, TextLoader

FILE_LOADER_MAPPING = {
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "pdf": (PyPDFLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
}

class Summary:

    def __init__(self):
        self.model, self.tokenizer = self.pre_doc_summary()
        self.device = "cuda"
    # def pre_img_summary():
    #     MODEL = "deepseek-ai/Janus-1.3B"
    #     vl_chat_processor: VLChatProcessor = VLChatProcessor.from_pretrained(MODEL)
    #     tokenizer = vl_chat_processor.tokenizer

    #     vl_gpt: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(
    #         MODEL, trust_remote_code=True
    #     )
    #     return vl_gpt, vl_chat_processor, tokenizer

    def pre_doc_summary(self):
        # MODEL = "lianghsun/Llama-3.2-Taiwan-3B"
        MODEL ="meta-llama/Llama-3.2-1B-Instruct"
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForCausalLM.from_pretrained(MODEL)
        return model, tokenizer

    def summarize(self, path, filetype, doctype):
        summary = ""
        if filetype == "image": 
            summary = 'summary'
        elif filetype =="text": summary = self.summarize_doc(self.model, path, doctype)
        print(path)
        return summary

    # def summarize_image(model, vl_chat_processor, tokenizer, path):
    #     conversation = [
    #         {
    #             "role": "User",
    #             "content": "<image_placeholder>\n Summarize the image in one sentence.",
    #             "images": [path],
    #         },
    #         {"role": "Assistant", "content": ""},
    #     ]
    #     # load images and prepare for inputs
    #     pil_images = load_pil_images(conversation)
    #     prepare_inputs = vl_chat_processor(
    #         conversations=conversation, images=pil_images, force_batchify=True
    #     ).to(model.device)

    #     # # run image encoder to get the image embeddings
    #     inputs_embeds = model.prepare_inputs_embeds(**prepare_inputs)

    #     # # run the model to get the response
    #     outputs = model.language_model.generate(
    #         inputs_embeds=inputs_embeds,
    #         attention_mask=prepare_inputs.attention_mask,
    #         pad_token_id=tokenizer.eos_token_id,
    #         bos_token_id=tokenizer.bos_token_id,
    #         eos_token_id=tokenizer.eos_token_id,
    #         max_new_tokens=512,
    #         do_sample=False,
    #         use_cache=True,
    #     )

    #     answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    #     print(answer)
    #     return answer


    def summarize_doc(self, pipe, path, filetype):
        loader_class, loader_args = FILE_LOADER_MAPPING[filetype]
        loader = loader_class(path, **loader_args)

        prompt = f"請使用繁體中文摘要上述文字內容，盡量不要超過100個字:{loader.load()}"
        messages = [
                        {
                    "role": "system",
                    "content": "你是個文書助理，你接下來會摘要一個文件，請將文件的內容簡潔且扼要的摘錄到回答當中，內容請務必要精確，請跳過看起來像代碼的部分",
                    },
                        {
                    "role": "user", 
                    "content": prompt
                    }
                ]

        encodeds = self.tokenizer.apply_chat_template(messages, return_tensors="pt")
        model_inputs = encodeds.to(self.device)
        self.model.to(self.device)

        generated_ids = self.model.generate(model_inputs, max_new_tokens=100, do_sample=True)
        decoded = self.tokenizer.batch_decode(generated_ids)
        pos = decoded[0].find("page_content=")

        return decoded[0][pos+13:]+f" source: {path}"
        
