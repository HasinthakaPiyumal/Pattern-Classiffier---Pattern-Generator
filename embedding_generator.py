import torch,os
from transformers import AutoTokenizer, AutoModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class EmbeddingGenerator:
    def __init__(self,model_name:str="microsoft/codebert-base", chunk_size:int=128, stride:int=68):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.chunk_size = chunk_size
        self.stride = stride

    def generate_embedding(self,code:str):
        all_tokens = self.tokenizer.encode(code, add_special_tokens=False)
        total_length = len(all_tokens)

        if total_length <= self.chunk_size:
            inputs = self.tokenizer(code,return_tensors='pt')
        else:
            chunks = []
            for i in range(0,total_length,self.stride):
                chunk = all_tokens[i:i+self.chunk_size]
                chunks.append(chunk)
            input_ids = [self.tokenizer.build_inputs_with_special_tokens(chunk) for chunk in chunks]
            max_len = max(len(ids) for ids in input_ids)
            attention_masks = []
            padded_input_ids = []
            for chunk in input_ids:
                padding_length = max_len - len(chunk)
                padded_input_ids.append(chunk+[self.tokenizer.pad_token_id]*padding_length)
                attention_masks.append([1]*len(chunk)+[0]*padding_length)
            inputs = {'input_ids': torch.tensor(padded_input_ids), 'attention_mask': torch.tensor(attention_masks)}

        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        code_embedding1 = torch.mean(outputs.pooler_output,0)

        expanded_attention_mask = inputs['attention_mask'].unsqueeze(-1).expand(outputs.last_hidden_state.shape)
        masked_embeddings = expanded_attention_mask * outputs.last_hidden_state
        code_embedding2 = (masked_embeddings.sum(1)/ expanded_attention_mask.sum(1)).mean(0)

        return {"last_hidden_state_mean": code_embedding2, "pooler_output_mean": code_embedding1}
    
    

if __name__ == "__main__":
    from utils import get_all_python_files, load_code_from_file,get_folders
    import pandas as pd
    repo_path = "/home/hasinthaka/Documents/Projects/AI/AI Pattern Mining/Pattern Validator/reposistories/test"
    repo_path = "/home/hasinthaka/Documents/Projects/AI/AI Pattern Mining/Pattern Validator/reposistories/model_testing"
    repo_path = "/home/hasinthaka/Documents/Projects/AI/AI Pattern Mining/Pattern Validator/reposistories/AI Patterns"

    embedding_generator = EmbeddingGenerator(model_name="FacebookAI/roberta-base")
    patterns = get_folders(repo_path)

    embedding_size = embedding_generator.model.config.hidden_size
    print("Embedding size:", embedding_size)

    columns = ["pattern"]+[f'dim_{i}' for i in range(embedding_size)]
    embeddings_lhsm = pd.DataFrame(columns=columns)
    embeddings_pom = pd.DataFrame(columns=columns)

    for pattern in patterns:
        if pattern == "embeddings":
            continue
        print("Processing pattern:", pattern)
        python_files = get_all_python_files(repo_path+"/"+pattern)
        for file in python_files:
            code = load_code_from_file(file)
            embeddings = embedding_generator.generate_embedding(code)
            print("Computed embeddings for file:", file)
            embeddings_lhsm.loc[len(embeddings_lhsm)] = [pattern]+embeddings["last_hidden_state_mean"].tolist()
            embeddings_pom.loc[len(embeddings_pom)] = [pattern]+embeddings["pooler_output_mean"].tolist()

    os.makedirs(f"{repo_path}/embeddings",exist_ok=True)

    embeddings_lhsm.to_csv(f"{repo_path}/embeddings/embeddings_roberta_base_last_hidden_state_mean.csv",index=False)
    embeddings_pom.to_csv(f"{repo_path}/embeddings/embeddings_roberta_base_pooler_output_mean.csv",index=False)