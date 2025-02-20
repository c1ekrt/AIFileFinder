import transformers
import torch
from transformers import pipeline
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader, PyPDFLoader, TextLoader

from janus.models import MultiModalityCausalLM, VLChatProcessor
from janus.utils.io import load_pil_images


FILE_LOADER_MAPPING = {
    "doc": (UnstructuredWordDocumentLoader, {}),
    "docx": (UnstructuredWordDocumentLoader, {}),
    "md": (UnstructuredMarkdownLoader, {}),
    "pdf": (PyPDFLoader, {}),
    "txt": (TextLoader, {"encoding": "utf8"}),
}

class Summary:

    def __init__(self):
        self.model = self.pre_doc_summary()

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
        MODEL ="meta-llama/Llama-3.2-3B-Instruct"
        pipe = pipeline(
            "text-generation",
            model=MODEL,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        return pipe

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
        print(path) 
        loader_class, loader_args = FILE_LOADER_MAPPING[filetype]
        loader = loader_class(path, **loader_args)

        prompt = f"請你摘要上述文字內容，請不要超過100個字:{loader.load()}"
        message = [
                        {
                    "role": "system",
                    "content": "你是個文書助理，你接下來會摘要一個文件，請將文件的內容簡潔且扼要的摘錄到回答當中，內容請務必要精確，請跳過看起來像代碼的部分",
                    },
                        {
                    "role": "user", 
                    "content": prompt
                    }
                ]

        outputs = pipe(
            message,
            max_new_tokens=128,
        )
        print(outputs[0]["generated_text"][-1]['content'])
        return outputs[0]["generated_text"][-1]['content']
        
